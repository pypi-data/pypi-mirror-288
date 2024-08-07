from danila.danila_balka_text_recognize_base import Danila_balka_text_recognize_base
from danila.danila_rama_text_recognize_base import Danila_rama_text_recognize_base


class Danila_balka_text_recognize:
    def __init__(self, yolov5_dir, danila_balka_text_recognize_params):
        self.danila_balka_text_recognize_params = danila_balka_text_recognize_params
        self.danila_balka_text_recognize = Danila_balka_text_recognize_base(yolov5_dir,
                                                                    self.danila_balka_text_recognize_params.balka_text_recognize_version
                                                                    )

    def balka_text_recognize(self, balka_prod, img_cuts, img_text_areas_2_balkas):
        return self.danila_balka_text_recognize.balka_text_recognize(_balka_prod=balka_prod, img_cuts=img_cuts,
                                                                     image_text_areas_2_balkas=img_text_areas_2_balkas)