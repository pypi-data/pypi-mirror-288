import os
# Tensorflow GPU 에러 무시
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf


def is_model_downloaded(model_name):
    # 매개변수로 받은 모델이름과 일치하는 폴더가 있는지 확인하는 함수
    download_folder_path = "download_folder"

    if os.path.isdir(download_folder_path):
        if model_name in os.listdir(download_folder_path):
            pb_file_path = os.getcwd() + "\\" + download_folder_path + "\\" + model_name
            return pb_file_path
        else:
            print("모델 이름을 다시 확인해주세요.")
    else:
        # 다운로드 된 모델이 없다면 아래 함수를 통해 모델을 다운로드 받으라고 출력
        print("아래 명령어를 사용하여 모델을 다운로드 받으세요.")


class ModelUtils:
    """
    ModelUtils 클래스는 Tensorflow 모델을 관리하는 유틸리티 클래스입니다.
    이 클래스를 바탕으로 아래와 같은 일을 수행할 수 있습니다.
    - load_model: 모델을 로드합니다.
    - show_summary: 모델 요약 정보를 출력합니다.
    - inference: 주어진 데이터에 대한 추론을 수행합니다.
    """
    def __init__(self, model_name):
        self.model_name = model_name
        self.model = None

    def load_model(self):
        pb_file_path = is_model_downloaded(self.model_name)
        self.model = tf.keras.models.load_model(pb_file_path)

    def show_summary(self):
        if self.model is not None:
            self.model.summary()

    def inference(self, data):
        count = 0
        for i in self.model.predict(data)[0]:
            print(f"{count} Accuracy: {i:.3f}")
            count += 1
        # TODO inference의 return 값을 어떻게 줄지 정해야 함.
        return self.model.predict(data)[0]


if __name__ == "__main__":
    model_name = "model_version_2"
    test_model = ModelUtils(model_name)
    test_model.load_model()

    image = 'data.jpg'
    data = to_image(image)  # 이미지에 대하여 추론
    test_model.inference(data)
