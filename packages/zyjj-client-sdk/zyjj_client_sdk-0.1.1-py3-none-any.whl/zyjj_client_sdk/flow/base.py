import logging
from enum import Enum
from zyjj_client_sdk.base import Base, ApiService, MqttServer, MqttEventType
from zyjj_client_sdk.base.entity import TaskInfo
from zyjj_client_sdk.lib import FFMpegService, OSSService
from dataclasses import dataclass
from typing import Callable, Optional, Any


class NodeType(Enum):
    BasicStart = 'basic_start'
    BasicEnd = 'basic_end'
    BasicCode = 'basic_code'
    BasicObjectImport = 'basic_object_import'
    BasicObjectExport = 'basic_object_export'
    ToolGetConfig = 'tool_get_config'
    ToolCostPoint = 'tool_cost_point'
    ToolCheckPoint = 'tool_check_point'
    ToolUploadFile = 'tool_upload_file'
    ToolDownloadFile = 'tool_download_file'
    ToolFileParse = 'tool_file_parse'
    ToolFileExport = 'tool_file_export'
    ToolGetTencentToken = 'tool_get_tencent_token'
    ToolGenerateLocalPath = 'tool_generate_local_path'
    ToolFfmpegPoint = 'tool_ffmpeg_point'


# 节点
@dataclass
class FlowNode:
    node_id: str
    node_type: NodeType
    data: str


@dataclass
class FlowRelation:
    from_id: str
    from_output: str
    to_id: str
    to_input: str


@dataclass
class NodeInfo:
    node_id: str = ''
    node_type: str = ''  # 节点类型
    data: str = ''  # 节点的额外参数
    cost: int = 0  # 执行耗时
    status: int = 0  # 执行状态
    msg: str = ''  # 错误信息


# 给flow节点提供的基本方法
class FlowBase:
    def __init__(
            self,
            base: Base,  # 基本信息
            api: ApiService,  # api服务
            mqtt: MqttServer,  # mqtt服务
            global_data: dict,  # 全局数据
            task_info: TaskInfo,  # 任务数据
    ):
        # 一些私有变量，不暴露
        self.__base = base
        self.__ffmpeg = FFMpegService()
        self.__mqtt = mqtt
        self.__global_data = global_data
        self.__task_info = task_info
        self.__node_current: FlowNode | None = None
        self.__node_pre: list[FlowRelation] = []
        self.__node_next: list[FlowRelation] = []
        # 节点的描述信息
        self.__node_desc = {}
        self.__node_log = {}
        # 可以被外部模块使用的变量
        self.api = api
        self.uid = task_info.uid
        self.task_id = task_info.task_id

    # 添加节点描述
    def add_desc(self, desc: str):
        if self.__node_current is not None:
            self.__node_desc[self.__node_current.node_id] = desc

    # 获取节点描述
    def get_desc(self) -> dict:
        return self.__node_desc

    # 添加节点日志
    def add_log(self, key: str, value: Any):
        if self.__node_current is None:
            return
        node_id = self.__node_current.node_id
        if node_id not in self.__node_log:
            self.__node_log[node_id] = {}
        self.__node_log[self.__node_current.node_id][key] = value

    def get_log(self) -> dict:
        return self.__node_log

    # 设置当前节点的关联关系
    def set_flow_relation(self, node: FlowNode, prev: list[FlowRelation], after: list[FlowRelation]):
        self.__node_current = node
        self.__node_pre = prev
        self.__node_next = after

    # 获取输入
    def input_get(self) -> dict:
        return self.__task_info.input

    # 获取当前节点需要哪些输出字段
    def node_output_need(self) -> list[str]:
        return [relation.from_output for relation in self.__node_next]

    # 生成一个本地路径
    def tool_generate_local_path(self, ext: str) -> str:
        return self.__base.generate_local_file(ext)

    # 获取存储服务
    def new_oss(self) -> OSSService:
        return OSSService(self.__base, self.api)

    # 获取文件时长
    def tool_ffmpeg_get_duration(self, path: str) -> float:
        return self.__ffmpeg.get_duration(path)

    # 触发代码节点
    def tiger_code(self, func_id: str, _input: dict, base=None) -> dict:
        # 获取代码信息
        code_info = self.api.get_func_code(func_id)
        logging.info(f"execute code {code_info}")
        self.add_desc(code_info['name'])
        tmp = {
            "inputs": [_input[unique] if unique in _input else None for unique in code_info["inputs"]],
            "base": base
        }
        exec(f"{code_info['code']}\noutput = handle(*inputs)", tmp)
        out = tmp['output']
        if not isinstance(out, tuple):
            out = (out,)
        output = {}
        for idx, unique in enumerate(code_info["outputs"]):
            output[unique] = out[idx]
        return output


# 处理节点定义
node_define = Callable[[FlowBase, dict, Optional[dict]], dict]
