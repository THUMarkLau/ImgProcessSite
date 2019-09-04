'''
    用来储存辅助服务器运行的内容
'''

import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image
import io


def byte2Img(byte_img):
    '''
    接受一个 io.BytesIO_object，将其转换成ndarray的形式返回
    :param byte_img: io.BytesIO_object，为图片读取对象
    :return: 该图片对应的ndarray
    '''
    img = Image.open(byte_img)
    return np.array(img)