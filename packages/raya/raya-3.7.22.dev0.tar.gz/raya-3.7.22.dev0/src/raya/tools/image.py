from raya.enumerations import IMAGE_TYPE


def show_image_once(img, title='', scale=1.0):
    pass


def show_image(img,
               title='',
               scale=1.0,
               img_type: IMAGE_TYPE = IMAGE_TYPE.COLOR):
    pass


def save_image(img, path: str):
    pass


def match_image_predictions(last_predictions_timestamp, last_color_frames):
    pass


def draw_on_image(image, last_predictions):
    pass
