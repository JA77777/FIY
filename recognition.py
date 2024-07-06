import cv2 as cv
import base64
import requests


def recognize_image(img, recognition_type):
    if recognition_type == "动物":
        result = animal_detect(img)
    elif recognition_type == "植物":
        result = plant_detect(img)
    else:
        result = "请先选择识别类型"
    return result


def animal_detect(img):
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/animal"
    _, encoded_image = cv.imencode('.jpg', img)
    base64_image = base64.b64encode(encoded_image).decode('utf-8')
    params = {"image": base64_image}
    access_token = '24.9d21a6a1ac1e23eba5750759480ac700.2592000.1722743778.282335-90923670'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    result = response.json()
    if "result" in result:
        return result["result"][0]["name"]
    else:
        return "未能识别出动物"


def plant_detect(img):
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/plant"
    _, encoded_image = cv.imencode('.jpg', img)
    base64_image = base64.b64encode(encoded_image).decode('utf-8')
    params = {"image": base64_image}
    access_token = '24.9d21a6a1ac1e23eba5750759480ac700.2592000.1722743778.282335-90923670'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    result = response.json()
    if "result" in result:
        return result["result"][0]["name"]
    else:
        return "未能识别出植物"
