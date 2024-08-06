class RayaException(Exception):

    def get_raya_file(self):
        return


class RayaCodedException(RayaException):

    def __init__(self, error_code=None, error_msg=None):
        pass

    def __str__(self):
        return
