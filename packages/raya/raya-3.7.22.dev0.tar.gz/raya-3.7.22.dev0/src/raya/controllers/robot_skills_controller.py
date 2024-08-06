import enum
import dataclasses
import typing
from rclpy.node import Node
from raya.controllers.base_controller import BaseController


class RobotSkillType(enum.Enum):
    SERVICE = enum.auto()
    ACTION = enum.auto()


@dataclasses.dataclass
class RobotSkillField():
    is_list: bool
    ftype: type
    default_value: typing.Any


@dataclasses.dataclass
class _RobotSkill():
    type_name: str
    ros_type: type
    skill_type: RobotSkillType
    ros_client: typing.Any
    req_goal_fields: dict
    resp_res_fields: dict
    feedback_fields: dict


ROS_PYTHON_CLASSES = {
    'boolean': bool,
    'uint8': int,
    'float': float,
    'double': float,
    'int8': int,
    'uint8': int,
    'int16': int,
    'uint16': int,
    'int32': int,
    'uint32': int,
    'int64': int,
    'uint64': int,
    'string': str
}


class RobotSkillsController(BaseController):

    def __init__(self, name: str, node: Node, interface: RayaInterface,
                 extra_info: dict):
        pass

    def get_skills(self) -> list:
        return

    def get_skill_type(self, skill: str) -> RobotSkillType:
        return

    def get_skill_params_info(self, skill: str) -> dict:
        return

    def get_skill_result_info(self, skill: str) -> dict:
        return

    def get_skill_feedback_info(self, skill: str) -> dict:
        return

    async def execute_skill(self,
                            skill: str,
                            callback_feedback: typing.Callable = None,
                            callback_feedback_async: typing.Callable = None,
                            callback_finish: typing.Callable = None,
                            callback_finish_async: typing.Callable = None,
                            wait: bool = True,
                            **kwargs):
        pass

    async def cancel_skill(self,
                           skill: str,
                           ignore_if_not_cancelable: bool = False):
        return
