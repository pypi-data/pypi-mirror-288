import typing
from rclpy.node import Node
from raya.handlers.cv.classifiers.classifier_handler import ClassifierHandler


class ObjectsClassifierHandler(ClassifierHandler):

    def __init__(self, node: Node, topic: str, source: str, model_id: int,
                 model_info: dict, continues_msg: bool, cli_cmd, cmd_call):
        pass

    async def find_objects(self,
                           objects: list,
                           callback: typing.Callable = None,
                           callback_async: typing.Callable = None,
                           wait: bool = False,
                           timeout: float = 0.0,
                           as_dict: bool = False):
        return

    def cancel_find_objects(self):
        pass

    def get_objects_names(self):
        return
