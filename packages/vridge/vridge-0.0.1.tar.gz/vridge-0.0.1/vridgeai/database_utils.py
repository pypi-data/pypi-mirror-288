import requests
import json
import os

from dotenv import load_dotenv


load_dotenv()


class SaveInformation: # TODO 아직 API 배포가 되지않아 테스트를 해봐야함.
    """
    정보를 저장하는 클래스

    :param api_key: api_key
    :return:
    """
    def __init__(self, api_key):
        self.api_key = api_key

    def statistics(self):
        """
        통계 정보 저장하는 함수

        :return: None
        """
        url = "https://ai.vazil.me/api/ai/point-statistics"
        body = {
            "edgeId": "test-edge-id",
            "modelId": "test-model-id",
            "orgId": "test-orgId",
            "projectId": "test-projectId",
            "result": "ok",
            "inferenceRate": 0.8343494534492493,
            "inferenceTime": 47
        }

        params = {"api_key": self.api_key}
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(url, params=params, headers=headers, data=json.dumps(body)).json()
            if response["status"] != 201:
                print("Failed to save statistics information storage.")
            print("Your statistics information have been saved successfully.")
        except requests.exceptions.RequestException as e:
            print("Error occurred: ", e)

    def inference(self):
        """
        inference 정보 저장하는 함수

        :return: None
        """
        url = "https://ai.vazil.me/api/ai/inference/info"
        body = {
          "modelId": "ai-test-loso",
          "pointId": "web-test-loso",
          "result": {
            "predict": 0,
            "predicts": [],
            "processTime": 0.5811035633087158,
            "result": "test",
            "detections": {
              "boxes": [],
              "scores": [],
              "classes": []
            },
            "height": 1400,
            "width": 1800
          }
        }

        params = {"api_key": self.api_key}
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(url, params=params, headers=headers, data=json.dumps(body)).json()
            if response["status"] != 200:
                print("Failed to save statistics information storage.")
            print("Your inference information have been saved successfully.")
        except requests.exceptions.RequestException as e:
            print("Error occurred: ", e)


if __name__ == "__main__":
    api_key = os.getenv("api_key")
    saver = SaveInformation(api_key)
    saver.inference()