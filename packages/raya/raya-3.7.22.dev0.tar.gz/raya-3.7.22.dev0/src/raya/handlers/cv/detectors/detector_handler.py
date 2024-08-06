import typing
from rclpy.node import Node
from raya.handlers.cv.model_handler import ModelHandler


class DetectorHandler(ModelHandler):

    def __init__(self, node: Node, topic: str, source: str, model_id: int,
                 model_info: dict, continues_msg: bool, cli_cmd, cmd_call):
        pass

    async def get_detections_once(self, as_dict=False, get_timestamp=False):
        return

    def get_current_detections(self, as_dict=False, get_timestamp=False):
        return

    def set_detections_callback(self,
                                callback: typing.Callable = None,
                                callback_async: typing.Callable = None,
                                as_dict: bool = False,
                                call_without_detections: bool = False):
        return

    def set_img_detections_callback(
            self,
            callback: typing.Callable = None,
            callback_async: typing.Callable = None,
            as_dict: bool = False,
            call_without_detections: bool = False,
            cameras_controller: typing.Callable = None):
        return
