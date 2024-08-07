from data.neuro.Balka_prod_classify_class import Balka_prod_classify_class
from data.neuro.models import BALKA_CLASSIFY_MODEL_ADDRESS


class Danila_balka_classify_prod:
    def __init__(self, yolov5_dir, balka_classify_model):
        yolo_path = yolov5_dir
        if balka_classify_model == 1:
            balka_prod_classify_model_path = BALKA_CLASSIFY_MODEL_ADDRESS
        print('reading and loading - BALKA_PROD_CLASSIFY_MODEL')
        self.balka_prod_classify_model = Balka_prod_classify_class(balka_prod_classify_model_path, yolo_path)

    def balka_classify(self, img):
        balka_prod_conf = self.balka_prod_classify_model.classify(img)
        return balka_prod_conf