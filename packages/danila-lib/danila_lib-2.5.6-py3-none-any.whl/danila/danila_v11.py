from danila.danila_balka import Danila_balka
from danila.danila_balka_classify_params import Danila_balka_classify_params
from danila.danila_balka_params import Danila_balka_params
from danila.danila_balka_text_detect_params import Danila_balka_text_detect_params
from danila.danila_balka_text_recognize_params import Danila_balka_text_recognize_params
from danila.danila_detail import Danila_detail
from danila.danila_detail_params import Danila_detail_params
from danila.danila_rama import Danila_rama
from danila.danila_rama_classify_params import Danila_rama_classify_params
from danila.danila_rama_params import Danila_rama_params
from danila.danila_rama_text_detect_params import Danila_rama_text_detect_params
from danila.danila_rama_text_recognize_params import Danila_rama_text_recognize_params
from danila.danila_vagon import Danila_vagon
from danila.danila_vagon_params import Danila_vagon_params
from danila.danila_vagon_text_detect_params import Danila_vagon_text_detect_params
from danila.danila_vagon_text_recognize_params import Danila_vagon_text_recognize_params
from data.result.Text_cut_recognize_result import Text_cut_recognize_result
from data.result.Text_recognize_result import Text_recognize_result


class Danila_v11:
    def __init__(self, yolov5_dir, detail_classify_version = 1,
                 rama_detect_version = 1, rama_classify_version = 1, rama_text_detect_version = 1, rama_text_recognize_version = 1,
                 vagon_text_detect_version = 1, vagon_text_recognize_version = 1,
                 balka_detect_version = 1, balka_classify_version = 1, balka_text_detect_version = 1, balka_text_recognize_version = 1):

        if detail_classify_version == 1:
            danila_detail_params = Danila_detail_params(1,2)
        elif detail_classify_version == 2:
            danila_detail_params = Danila_detail_params(2, 1)
        else:
            raise ValueError('detail_classify_version - incorrect')
        self.danila_detail = Danila_detail(danila_detail_params, yolo_dir=yolov5_dir)

        if rama_classify_version == 1:
            danila_rama_classify_params = Danila_rama_classify_params(1,1)
        elif rama_classify_version == 2:
            danila_rama_classify_params = Danila_rama_classify_params(1, 2)
        elif rama_classify_version == 3:
            danila_rama_classify_params = Danila_rama_classify_params(1, 3)
        else:
            raise ValueError('rama_classify_version - incorrect')

        if (rama_detect_version == 1) & (rama_text_detect_version == 1):
            danila_rama_text_detect_params = Danila_rama_text_detect_params(1,1)
        else:
            raise ValueError('rama_text_detect_version - incorrect')

        if (rama_text_recognize_version == 1):
            danila_rama_text_recognize_params = Danila_rama_text_recognize_params(1)
        else:
            raise ValueError('rama_text_recognize_version - incorrect')

        danila_rama_params = Danila_rama_params(danila_rama_classify_params, danila_rama_text_detect_params, danila_rama_text_recognize_params)
        self.danila_rama = Danila_rama(yolov5_dir, danila_rama_params)

        if (vagon_text_detect_version == 1) | (vagon_text_detect_version == 2):
            danila_vagon_text_detect_params = Danila_vagon_text_detect_params(vagon_text_detect_version)
        else:
            raise ValueError('vagon_text_detect_version - incorrect')

        if (vagon_text_recognize_version == 1):
            danila_vagon_text_recognize_params = Danila_vagon_text_recognize_params(vagon_text_recognize_version, 320,320)
        elif (vagon_text_recognize_version == 2):
            danila_vagon_text_recognize_params = Danila_vagon_text_recognize_params(vagon_text_recognize_version, 196,196)
        elif (vagon_text_recognize_version == 3):
            danila_vagon_text_recognize_params = Danila_vagon_text_recognize_params(vagon_text_recognize_version, 196,
                                                                                    196)
        elif (vagon_text_recognize_version == 4):
            danila_vagon_text_recognize_params = Danila_vagon_text_recognize_params(vagon_text_recognize_version, 352,
                                                                                    352)
        else:
            raise ValueError('vagon_text_recognize_version - incorrect')
        danila_vagon_params = Danila_vagon_params(danila_vagon_text_detect_params, danila_vagon_text_recognize_params)
        self.danila_vagon = Danila_vagon(yolov5_dir, danila_vagon_params)

        if balka_classify_version == 1:
            danila_balka_classify_params = Danila_balka_classify_params(1,1)
        else:
            raise ValueError('balka_classify_version - incorrect')

        if (balka_detect_version == 1) & (balka_text_detect_version == 1):
            danila_balka_text_detect_params = Danila_balka_text_detect_params(1,1)
        else:
            raise ValueError('balka_text_detect_version - incorrect')

        if (balka_text_recognize_version == 1):
            danila_balka_text_recognize_params = Danila_balka_text_recognize_params(1)
        else:
            raise ValueError('rama_text_recognize_version - incorrect')

        danila_balka_params = Danila_balka_params(danila_balka_classify_params, danila_balka_text_detect_params, danila_balka_text_recognize_params)
        self.danila_balka = Danila_balka(yolov5_dir, danila_balka_params)



    def detail_classify(self, img):
        detail = self.danila_detail.detail_classify(img)
        if detail.detail.text == 'rama':
            detail = self.rama_classify(img, detail)
        elif detail.detail.text == 'balka':
            detail = self.balka_classify(img, detail)
        return detail


    def detail_text_detect(self, img):
        detail = self.danila_detail.detail_classify(img)
        resul_img = img
        if detail.detail.text == 'rama':
            resul_img = self.rama_text_detect_cut(img)
        elif detail.detail.text == 'vagon':
            resul_img = self.vagon_number_detect(img)
        elif detail.detail.text == 'balka':
            resul_img = self.balka_text_detect(img)
        return resul_img

    def detail_text_recognize(self, img):
        detail = self.danila_detail.detail_classify(img)
        if detail.detail.text == 'rama':
            detail = self.rama_text_recognize(img, detail)
        elif detail.detail.text == 'vagon':
            detail = self.vagon_number_recognize(img, detail)
        elif detail.detail.text == 'balka':
            detail = self.balka_text_recognize(img, detail)
        return detail

    def rama_classify(self, img, detail = None):
        """rama_classify(Img : openCv frame): String - returns class of rama using CNN network"""
        """rama_classify uses Rama_classify_class method - classify(Img)"""
        return self.danila_rama.rama_classify(img, detail)


    # returns openCV cut rama with drawn text areas
    def rama_text_detect_cut(self, img):
        """returns openCV cut rama with drawn text areas"""
        return self.danila_rama.rama_text_detect(img)


    # returns dict {'number', 'prod', 'year'} for openCV rama img or 'no_rama'
    def rama_text_recognize(self, img, detail = None):
        """returns dict {'number', 'prod', 'year'} for openCV rama img or 'no_rama'"""
        return self.danila_rama.rama_text_recognize(img, detail)

    # returns openCV img with drawn number areas
    def vagon_number_detect(self, img):
        """returns openCV img with drawn number areas"""
        return self.danila_vagon.vagon_number_detect(
            img
        )

    def vagon_number_recognize(self, img, detail = None):
        return self.danila_vagon.vagon_number_recognize(img, detail)


    def balka_classify(self, img, detail = None):
        return self.danila_balka.balka_classify(img, detail)

    def balka_text_detect(self, img):
        return self.danila_balka.balka_text_detect(img)

    def balka_text_recognize(self, img, detail = None):
        return self.danila_balka.balka_text_recognize(img, detail)