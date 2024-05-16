

import base64
import urllib
import requests
import io
import cv2
API_KEY = "dokj4FgwMtwi81nn3KzIX7fb"
SECRET_KEY = "nrptcaIzyrW63urSnAwHfoUCMsZPoDjH"

def ocr(img_path):
    # img_path = "E:/JiChuang/Chinese-chess/detect_cnn/dataset/2-仕/1.png"
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=" + get_access_token()
    b64 = get_image_content_as_base64(img_path, True)
    payload = f'image={b64}&probability=true'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    
    # 发送POST请求
    response = requests.post(url, headers=headers, data=payload)

    # 获取JSON数据
    data = response.json()

    # 提取words_result键的值，它是一个列表
    words_result = data.get('words_result', [])
    # probability = 
    # 遍历列表，提取每个元素的'words'键对应的值
    words = [item['words'] for item in words_result]
    probability = [item['probability'] for item in words_result]
    avg_prob = [item['average'] for item in probability]
    # 打印提取出的词
    # print(words[0])  # 输出: ['仕']
    # print(avg_prob[0])
    # print("response", response.text)
    if words and avg_prob:
        return words[0], avg_prob[0]
    else:
        return
    

# def get_file_content_as_base64(path, urlencoded=False):
#     """
#     获取文件base64编码
#     :param path: 文件路径
#     :param urlencoded: 是否对结果进行urlencoded 
#     :return: base64编码信息
#     """
#     with open(path, "rb") as f:
#         content = base64.b64encode(f.read()).decode("utf8")
#         if urlencoded:
#             content = urllib.parse.quote_plus(content)
#     return content

def get_image_content_as_base64(image, urlencoded=False):
    """
    获取NumPy图像数组的base64编码
    :param image: NumPy图像数组
    :param urlencoded: 是否对结果进行urlencoded
    :return: base64编码信息
    """
    # 将NumPy数组编码为PNG格式的图像
    retval, buffer = cv2.imencode('.png', image)
    if retval:
        # 编码为base64
        content = base64.b64encode(buffer).decode("utf8")
        # 判断是否需要进行URL编码
        if urlencoded:
            content = urllib.parse.quote_plus(content)
        return content
    else:
        raise ValueError("Could not encode image to PNG format")
    
def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == '__main__':
    img = cv2.imread("E:/JiChuang/Chinese-chess/detect_cnn/dataset3/5/1.png")
    print(ocr(img))
