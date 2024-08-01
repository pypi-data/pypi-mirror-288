import numpy as np
import tensorflow as tf
import base64

from io import BytesIO
from PIL import Image

import matplotlib.pyplot as plt


def image_to_byte(image_path):
    # 이미지를 바이트로 변환
    """
    이미지를 바이트로 변환하는 함수

    :param image_path: 이미지 파일 경로
    :return: 이미지를 바이트로 변환한 값
    """
    with Image.open(image_path) as image:
        buffered = BytesIO()
        image.save(buffered, format=image.format)
        img_str = base64.b64encode(buffered.getvalue()).decode()

    img_byte = base64.b64decode(img_str)
    img_byte = BytesIO(img_byte)
    img_byte = Image.open(img_byte)
    return img_byte


def show_image(image_path):
    # 바이트로 변환된 이미지를 tf 배열로 바꿔서 출력
    """
    이미지를 받아 화면에 출력하는 함수

    :param image_path: 이미지 파일 경로
    :return: None
    """
    imgByte = image_to_byte(image_path)
    img = tf.keras.preprocessing.image.img_to_array(imgByte)
    img_org = tf.cast(img, tf.uint8)

    plt.figure(figsize=(6, 6))
    plt.imshow(img_org.numpy())
    plt.axis('off')
    plt.show()


def for_image(image_path):
    """
    이미지를 numpy 배열로 변환 후 반환하는 함수

    :param image_path: 이미지 파일 경로
    :return: 이미지를 numpy 배열로 반환 ( tensor )
    """
    img_byte = image_to_byte(image_path)

    img = tf.keras.preprocessing.image.img_to_array(img_byte)
    img_org = tf.cast(img, tf.uint8)

    height = img_org.shape[0]  # TODO 일단 패스.
    width = img_org.shape[1]

    img_org = tf.image.resize(img_org, [380, 380])

    channel = img_org.shape[2]
    if channel == 1:
        img_org = tf.convert_to_tensor(np.stack((np.reshape(img_org, (380, 380)),) * 3, axis=-1))
    elif channel == 4:
        img_org = tf.convert_to_tensor(img_org[:, :, :3])
    img_org = tf.dtypes.cast(img_org, dtype=tf.uint8)
    tensor = tf.expand_dims(img_org, axis=0)

    return tensor
