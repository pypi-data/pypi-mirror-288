import json
import logging
import math
import uuid
from typing import Optional

import requests
from tencentcloud.common import credential
from zyjj_client_sdk.flow.base import FlowBase
from zyjj_client_sdk.flow.node.common import get_val_or_default, tool_check_point, tool_cost_point, FileSourceType


# 获取云端配置
def node_get_config(base: FlowBase, data: dict, extra: Optional[dict]) -> dict:
    name = get_val_or_default("name", data, extra)
    is_json = extra.get("is_json", False)
    val = base.api.get_config(name)
    if is_json:
        val = json.loads(val)
    return {"val": val}


# 检查积分
def node_check_point(base: FlowBase, data: dict, extra: Optional[dict]) -> dict:
    point = get_val_or_default('point', data, extra, 0)
    tool_check_point(base, point)
    return {"point": point, "pass": data.get("pass")}


# 扣除积分
def node_cost_point(base: FlowBase, data: dict, extra: Optional[dict]) -> dict:
    name = get_val_or_default("name", data, extra, "")
    desc = get_val_or_default("desc", data, extra, "")
    point = get_val_or_default('point', data, extra, 0)
    tool_cost_point(base, name, desc, point)
    return {"pass": data.get("pass")}


# 下载文件返回二进制数据
def _download_file(url: str, referer: str) -> bytes:
    return requests.get(url, headers={"referer": referer}).content


# 上传文件
def node_upload_file(base: FlowBase, data: dict, extra: Optional[dict]) -> dict:
    # 输入和输出参数
    in_file_source = FileSourceType(get_val_or_default("in_file_source", data, extra, 0))
    out_file_source = FileSourceType(get_val_or_default("out_file_source", data, extra, 0))
    # 上传来源
    cloud_source = get_val_or_default("cloud_source", data, extra, 0)
    # 是否批量
    is_batch = get_val_or_default("is_batch", data, extra, False)
    oss = base.new_oss()
    # 最后得出的云端路径
    cloud_path_list = []
    output = {}
    # 不同文件来源走不同的方式，最后统一拿到一个云端路径列表
    if in_file_source == FileSourceType.CloudPath:  # 云端路径
        path = data.get("cloud_path")
        source = data.get("cloud_source")  # 先暂时不管
        cloud_path_list = path if is_batch else [path]
    elif in_file_source == FileSourceType.CloudFile:
        cloud_file = data.get("cloud_file")
        cloud_file_fields = extra.get("cloud_file_fields", [])
        cloud_file_list = cloud_file if is_batch else [cloud_file]
        output = _parse_file(cloud_file_list[0], cloud_file_fields)
        cloud_path_list = [_parse_file(file)["path"] for file in cloud_file_list]
    elif in_file_source == FileSourceType.CloudLink:  # 云端链接
        referer = get_val_or_default("referer", data, extra, "")
        ext = get_val_or_default("ext", data, extra, "")
        cloud_url = data.get("cloud_url")
        url_list = cloud_url if is_batch else [cloud_url]
        cloud_path_list = [oss.tencent_upload_by_bytes(base.uid, _download_file(url, referer), ext) for url in url_list]
    elif in_file_source == FileSourceType.LocalPath:  # 本地路径
        local_path = data.get("local_path")
        local_path_list = local_path if is_batch else [local_path]
        cloud_path_list = [oss.tencent_upload_by_local_path(base.uid, path) for path in local_path_list]
    elif in_file_source == FileSourceType.Bytes:  # 字节数据
        bytes_data = data.get("bytes_data")
        ext = get_val_or_default("ext", data, extra, "")
        bytes_list = bytes_data if is_batch else [bytes_data]
        cloud_path_list = [oss.tencent_upload_by_bytes(base.uid, b, ext) for b in bytes_list]
    # 根据输出类型执行不同的操作
    if out_file_source == FileSourceType.CloudPath:  # 云端路径
        output["cloud_path"] = cloud_path_list if is_batch else cloud_path_list[0]
        output["cloud_source"] = cloud_source
    elif out_file_source == FileSourceType.CloudLink:  # 云端链接
        url_list = [oss.tencent_get_url_by_key(path) for path in cloud_path_list]
        output["cloud_url"] = url_list if is_batch else url_list[0]
    elif out_file_source == FileSourceType.CloudFile:  # 云端文件
        cloud_file_list = [_parse_file({"path": path, "source": cloud_source}) for path in cloud_path_list]
        output["cloud_file"] = cloud_file_list if is_batch else cloud_file_list[0]

    return output


# 下载文件
def node_download_file(base: FlowBase, data: dict, extra: Optional[dict]) -> dict:
    in_file_source = FileSourceType(get_val_or_default("in_file_source", data, extra, 0))
    out_file_source = FileSourceType(get_val_or_default("out_file_source", data, extra, 0))
    is_batch = get_val_or_default("is_batch", data, extra, False)
    oss = base.new_oss()
    output = {}
    if in_file_source == FileSourceType.CloudFile or in_file_source == FileSourceType.CloudPath:  # 云端路径或者云端文件
        # 云端路径统一都是下载到本地（云端文件需要手动解析一下）
        if in_file_source == FileSourceType.CloudPath:
            cloud_path = data.get("cloud_path")
            cloud_source = data.get("cloud_source")  # 先不管
            cloud_path_list = cloud_path if is_batch else [cloud_path]
        else:
            cloud_file = data.get("cloud_file")
            cloud_file_fields = extra.get("cloud_file_fields", [])
            cloud_file_list = cloud_file if is_batch else [cloud_file]
            output = _parse_file(cloud_file_list[0], cloud_file_fields)
            cloud_path_list = [_parse_file(file)['path'] for file in cloud_file_list]
        local_path_list = [oss.tencent_download_file_by_key(path) for path in cloud_path_list]
        # 根据需求返回不同的数据
        if out_file_source == FileSourceType.LocalPath:  # 本地路径
            output["local_path"] = local_path_list if is_batch else local_path_list[0]
        elif out_file_source == FileSourceType.Bytes:  # 字节流
            bytes_list = [open(path, "rb").read() for path in local_path_list]
            output["bytes_data"] = bytes_list if is_batch else bytes_list[0]
    elif in_file_source == FileSourceType.CloudLink:  # 云端链接
        referer = get_val_or_default("referer", data, extra, "")
        ext = get_val_or_default("ext", data, extra, "")
        cloud_url = data.get("cloud_url")
        url_list = cloud_url if is_batch else [cloud_url]
        bytes_list = [_download_file(url, referer) for url in url_list]
        if out_file_source == FileSourceType.LocalPath:  # 本地路径
            local_path_list = [open(base.tool_generate_local_path(ext), "wb").write(b) for b in bytes_list]
            output["local_path"] = local_path_list if is_batch else local_path_list[0]
        elif out_file_source == FileSourceType.Bytes:  # 字节流
            output["bytes_data"] = bytes_list if is_batch else bytes_list[0]
    return output


def _parse_file(file: dict, fields=None) -> dict:
    path = file.get("path", "")
    file = {
        "path": path,
        "source": file.get("source", 0),
        "duration": file.get("duration", 0),
        "size": file.get("size", 0),
        "name": file.get("name", path.split("/")[-1]),
        "ext": file.get("ext", path.split(".")[-1]),
        "uid": file.get("uid", uuid.uuid4().hex)
    }
    return {field: file[field] for field in fields} if fields is not None else file


# 文件解析
def node_file_parse(base: FlowBase, data: dict, extra: Optional[dict]) -> dict:
    fields = get_val_or_default("fields", data, extra, [])
    return _parse_file(data.get("file"), fields)


# 文件组织
def node_file_export(base: FlowBase, data: dict, extra: Optional[dict]) -> dict:
    return _parse_file(data)


# 腾讯云token
def node_get_tencent_token(base: FlowBase, data: dict, extra: Optional[dict]) -> dict:
    token = base.api.could_get_tencent_token()
    return {"token": credential.Credential(token["TmpSecretId"], token["TmpSecretKey"])}


# 生成本地路径
def node_generate_local_path(base: FlowBase, data: dict, extra: Optional[dict]) -> dict:
    ext = get_val_or_default('ext', data, extra)
    return {"path": base.tool_generate_local_path(ext)}


# ffmpeg 积分计算
def node_ffmpeg_point(base: FlowBase, data: dict, extra: Optional[dict]) -> dict:
    path = get_val_or_default("path", data, extra)
    point = get_val_or_default("point", data, extra, default=0)
    duration = get_val_or_default("duration", data, extra, default=0)
    check_point = get_val_or_default("check_point", data, extra, default=False)
    if path is not None:
        duration = base.tool_ffmpeg_get_duration(path)
    final_point = math.ceil(float(point) * (duration / 60))
    base.add_log("duration", duration)
    output = {"point": final_point}
    if check_point:
        tool_check_point(base, final_point)
        output["pass"] = get_val_or_default("pass", data, extra)
    return output
