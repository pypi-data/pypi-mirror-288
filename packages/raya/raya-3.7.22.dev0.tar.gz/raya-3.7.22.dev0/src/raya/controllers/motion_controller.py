import typing
from rclpy.node import Node
from raya.controllers.base_controller import BaseController
from raya.logger import DEPRECATION_NEW_METHOD
from raya.enumerations import ANGLE_UNIT


class MotionController(BaseController):

    def __init__(self, name: str, node: Node, app, extra_info={}):
        pass

    @DEPRECATION_NEW_METHOD('get_last_result')
    def get_last_motion_result(self):
        return

    def get_last_result(self):
        return

    @DEPRECATION_NEW_METHOD('check_last_exception')
    def check_last_motion_exception(self):
        pass

    def check_last_exception(self):
        pass

    async def set_velocity(self,
                           x_velocity: float,
                           y_velocity: float,
                           angular_velocity: float,
                           duration: float,
                           enable_obstacles: bool = True,
                           ang_unit: ANGLE_UNIT = ANGLE_UNIT.DEGREES,
                           callback_feedback: typing.Callable = None,
                           callback_feedback_async: typing.Callable = None,
                           callback_finish: typing.Callable = None,
                           callback_finish_async: typing.Callable = None,
                           wait: bool = False):
        pass

    async def move_linear(self,
                          distance: float,
                          x_velocity: float,
                          y_velocity: float = 0.0,
                          callback_feedback: typing.Callable = None,
                          callback_feedback_async: typing.Callable = None,
                          callback_finish: typing.Callable = None,
                          callback_finish_async: typing.Callable = None,
                          enable_obstacles: bool = True,
                          wait: bool = False):
        return

    async def rotate(self,
                     angle: float,
                     angular_speed: float,
                     ang_unit: ANGLE_UNIT = ANGLE_UNIT.DEGREES,
                     callback_feedback: typing.Callable = None,
                     callback_feedback_async: typing.Callable = None,
                     callback_finish: typing.Callable = None,
                     callback_finish_async: typing.Callable = None,
                     enable_obstacles: bool = True,
                     wait: bool = False):
        return

    async def await_until_stop(self):
        pass

    async def cancel_motion(self):
        pass

    def is_moving(self):
        return
