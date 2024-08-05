import requests
import json
import os

from dotenv import load_dotenv

load_dotenv()


class DatasetUploader:
    """
    데이터셋을 업로드하는 클래스

    :param
        - project_id: 프로젝트 아이디
        - org_id: 조직 아이디
        - api_key: api key
    :return: None
    """
    def __init__(self, project_id, org_id, api_key):
        self.projectId = project_id
        self.orgId = org_id
        self.api_key = api_key
        self.url = "https://ai.vazil.me/api/ai/dataset"
        self.body = None

    def set_dataset_upload_body(self):
        # ** 수정 필요함 **
        self.body = {
            "projectId": self.projectId,  # p-rkxbu51xz4fs
            "orgId": self.orgId,  # 2f0e2dc9433c46b1b21f81fdc3258fe6
            "train": [],
            "valid": [],
            "test": [],
            "preprocessing": {
                "resize": "Stretch to",
                "width": 380,
                "height": 380,
                "grayscale": False
            },
            "augmentations": {
                "brightness": {
                    "enable": False,
                    "scaleFactor": 1,
                    "offset": 0
                },
                "rotation": {
                    "enable": False,
                    "angle": 0
                },
                "crop": {
                    "enable": False,
                    "cropRate": 0
                },
                "flip": {
                    "enable": False,
                    "flipType": "HORIZONTAL"
                }
            },
            "details": {
                "versionId": 0,
                "name": "111_dataset_2024. 7. 29.",
                "createdAt": "2022-11-16T10:38:00",
                "trainingType": "IMAGE_CLASSIFICATION"
            },
            "labelMap": {
                "1": {
                    "color": "#47c9ad",
                    "count": 30,
                    "num": 1
                },
                "2": {
                    "color": "#008a6c",
                    "count": 42,
                    "num": 0
                }
            },
            "createUser": {
                "id": 1,
                "name": "관리자",
                "email": "admin@vazilcompany.com",
                "avatar": None
            },
            "datasetType": "IMAGE"
        }

    def dataset_upload(self):
        try:
            self.set_dataset_upload_body()
            params = {"api_key": self.api_key}
            headers = {"Content-Type": "application/json"}

            response = requests.post(self.url, params=params, headers=headers, data=json.dumps(self.body)).json()
            if not response["status"]:
                print("Dataset has not been uploaded.")
            print("The dataset has been uploaded successfully.")
        except requests.exceptions.RequestException as e:
            print("Error occurred: ", e)
        except ValueError as e:
            print(f"ValueError: {e}")


if __name__ == "__main__":
    projectId = os.environ.get("projectId")
    orgId = os.environ.get("orgId")
    api_key = os.environ.get("api_key")

    uploader = DatasetUploader(projectId, orgId, api_key)
    uploader.dataset_upload()
