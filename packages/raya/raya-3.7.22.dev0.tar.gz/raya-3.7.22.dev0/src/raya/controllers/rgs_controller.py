from rclpy.node import Node
from raya.exceptions import *
from raya.constants import *
from raya.exceptions_handler import *
from raya.controllers.base_controller import BaseController
from raya_constants.interfaces import *
from raya.enumerations import ANGLE_UNIT, POSITION_UNIT

TIMEOUT_TOPIC_UNAVAILABLE = 5.0
ERROR_SERVER_DOWN = 'The raya status message was not received'


class RGSController(BaseController):

    def __init__(self, name: str, node: Node, interface: RayaInterface,
                 extra_info):
        pass

    async def send_msg_to_app(self,
                              app_id: str,
                              controller: str,
                              header: dict = {},
                              data: dict = {}) -> None:
        pass

    def set_incoming_msg_callback(self, callback=None, callback_async=None):
        pass

    async def get_id(self):
        return

    async def get_raya_status(self) -> dict:
        return

    async def get_localization_status(self, ang_unit: ANGLE_UNIT,
                                      pos_unit: POSITION_UNIT) -> dict:
        return
