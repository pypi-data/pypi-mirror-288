import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import requests
import zipfile
import json
import tensorflow as tf

from pathlib import Path
from dotenv import load_dotenv


load_dotenv()


class ModelDownload:
    """
    모델 다운로드 클래스

    :param
        - key: 모델을 다운로드 받을 키
        - file_name: 설정할 파일 이름
        - remove_zip_file: 다운로드 받고 난후 zip 파일 삭제 여부
            - True: 삭제
            - False: 삭제 안함
    :return: None
    """
    def __init__(self, key, file_name, remove_zip_file):
        self.key = key
        self.file_name = file_name
        self.remove_zip_file = remove_zip_file
        self.model_download()

    @staticmethod
    def check_already_folder_exist():
        """
        download_folder 생성
        모델 다운로드 경로: download_folder
        """
        if not os.path.exists('./download_folder'):
            os.mkdir("./download_folder")
            print("download_folder has been created")
        else:
            print("download_folder already exist")
            print("The model was successfully downloaded.")

    @staticmethod
    # base64 파일을 .zip 파일로 변환
    def base64_convert_to_zipfile(file_name, base64_data):
        with open(f"download_folder/{file_name}.zip", "wb") as file:
            file.write(base64_data)

    def unzip(self):
        # 다운로드 받을 경로에 .zip 파일을 압축 해제
        target_folder = os.path.join('download_folder', self.file_name)
        zip_file_path = os.path.join('download_folder', f'{self.file_name}.zip')

        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(target_folder)

        # .zip 파일을 삭제하고 싶다면 remove_zip_flle = True,
        # 그렇지 않다면 False로 설정
        if self.remove_zip_file:
            os.remove(zip_file_path)

    def model_download(self):
        url = "https://ai.vazil.me/api/storage/file/download"
        params = {"key": self.key}

        """
        If you do not have a download path, create a download folder.
        download path: download_file/
        """
        self.check_already_folder_exist()

        try:
            response = requests.get(url, params=params)
            if response:
                base64_data = response.content
                self.base64_convert_to_zipfile(self.file_name, base64_data)
                self.unzip()
            print("The model was successfully downloaded.")
        except requests.exceptions.RequestException as e:
            print("Error occurred: ", e)
        except Exception as e:
            print(f"Error downloading the model: {e}")


class GroupModelCheck:
    """
    그룹 모델 확인하는 클래스

    :param
        - api_key: api key
        - id:
            projectId 또는 orgId

    for_organization: 조직 모델을 조회할 때
    for_project: 프로젝트 모델을 조회할 때

    :return: None
    """
    def __init__(self, api_key, id):
        self.api_key = api_key
        self.id = id

    @staticmethod
    def request(url, params):
        try:
            response = requests.get(url, params=params).json()
            if response["status"] != 200:
                print("Failed to query model.")
            print(json.dumps(response, ensure_ascii=False, indent=3))
            # return response
        except requests.exceptions.RequestException as e:
            print("Error occurred: ", e)
            # return False

    def for_organization(self):
        url = "https://ai.vazil.me/api/ai/model/org"
        params = {"api_key": self.api_key, "orgId": self.id}
        self.request(url, params)

    def for_project(self):
        url = "https://ai.vazil.me/api/ai/model/project"
        params = {"api_key": self.api_key, "projectId": self.id}
        self.request(url, params)


class Model:
    """
    모델 로드 클래스

    :param
        - model_name: 다운로드 받을 때 설정한 이름
    """
    def __init__(self, model_name):
        self.model_name = model_name
        self.model = None

    def load(self):
        current_path = Path(__file__).parent
        model_data_path = current_path + "\\download_folder\\" + self.model_name
        self.model = tf.keras.models.load_model(model_data_path)

    def summary(self):
        self.model.summary()

    def inference(self, data):
        """
        data: 이미지 데이터 또는 모델에 맞는 데이터
            - 테스트를 진행 중 이라면 더미 데이터
        """
        count = 0
        for i in self.model.predict(data)[0]:
            print(f"{count} Accuracy: {i:.3f}")
            count += 1
        return self.model.predict(data)[0]


if __name__ == "__main__":
    key = os.getenv("key")
    file_name = 'model_version_1'

    ModelDownload(key, file_name, True)