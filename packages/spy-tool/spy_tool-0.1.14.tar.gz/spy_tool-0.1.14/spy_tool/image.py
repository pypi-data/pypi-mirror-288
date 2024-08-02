import os
import cv2
import uuid
import httpx
import base64
import numpy as np
from typing import Optional, Tuple
from spy_tool.url import is_valid


def get_top_bottom_image_base64(top_image_base64: str, bottom_image_base64: str,
                                top_image_render_size: Tuple[int, int] = (290, 179),
                                bottom_image_render_size: Tuple[int, int] = (290, 19),
                                image_filedir: Optional[str] = None) -> str:
    """

    :param top_image_base64:
    :param bottom_image_base64:
    :param top_image_render_size: 上面图片 (渲染宽度)
    :param bottom_image_render_size: 下面图片 (渲染宽度)
    :param image_filedir:
    :return:
    """
    name = str(uuid.uuid1()).replace('-', '')

    # 文件名不加文件扩展名
    top_image_filename = f'top-image-{name}'
    bottom_image_filename = f'bottom-image-{name}'
    top_bottom_image_filename = f'top_bottom-image-{name}'

    top_image_filepath = os.path.join(image_filedir, top_image_filename) if image_filedir else None
    bottom_image_filepath = os.path.join(image_filedir, bottom_image_filename) if image_filedir else None
    top_bottom_image_filepath = os.path.join(image_filedir, top_bottom_image_filename) if image_filedir else None

    top_image_bytes = base64_to_bytes(top_image_base64, top_image_filepath)
    bottom_image_bytes = base64_to_bytes(bottom_image_base64, bottom_image_filepath)

    def bytes_to_image(image_bytes, image_render_size):
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_UNCHANGED)
        if image.shape[-1] == 4:
            # 提取 alpha 通道数据
            b_channel, g_channel, r_channel, alpha_channel = cv2.split(image)
            alpha_channel_inv = cv2.bitwise_not(alpha_channel)  # 反转
            image = cv2.merge((alpha_channel_inv, alpha_channel_inv, alpha_channel_inv))
        image = cv2.resize(image, image_render_size)
        return image

    # 缩放到渲染后的固定尺寸
    top_image = bytes_to_image(top_image_bytes, top_image_render_size)
    bottom_image = bytes_to_image(bottom_image_bytes, bottom_image_render_size)

    # 创建空白图片
    top_new_w, top_new_h = top_image_render_size
    bottom_new_w, bottom_new_h = bottom_image_render_size  # top_new_w >= bottom_new_w
    h, w = top_new_h + 10 + bottom_new_h + 10, top_new_w  # 留出两个 10 来区分上下图片
    blank_image = np.ones((h, w, 3), dtype=np.uint8) * 255

    # 填充 top bottom 到空白图片上
    blank_image[:top_new_h, :top_new_w, :] = top_image
    blank_image[top_new_h + 10:top_new_h + 10 + bottom_new_h, :bottom_new_w, :] = bottom_image
    _, buffer = cv2.imencode('.jpg', blank_image)
    top_bottom_image_base64 = base64.b64encode(buffer).decode()

    _top_bottom_image_bytes = base64_to_bytes(top_bottom_image_base64, top_bottom_image_filepath)

    return top_bottom_image_base64


def base64_to_base64(image_base64: str) -> str:
    if ',' in image_base64:
        image_type, image_base64 = image_base64.split(',')  # data:image/png;base64,...
    return image_base64


def base64_to_bytes(image_base64: str, image_filepath: Optional[str]) -> bytes:
    image_ext = 'png'
    if ',' in image_base64:
        image_type, image_base64 = image_base64.split(',')  # data:image/png;base64,...
        image_ext = image_type.split(';')[0].split('/')[-1]  # png
    image_bytes = base64.b64decode(image_base64)

    if image_filepath is not None:
        if not isinstance(image_filepath, str):
            raise ValueError('Unsupported image_filepath!')

        if not os.path.splitext(os.path.basename(image_filepath))[-1]:
            image_filepath += f'.{image_ext}'

        image_filedir = os.path.dirname(image_filepath)  # noqa
        os.makedirs(image_filedir, exist_ok=True)

        with open(image_filepath, 'wb') as file:
            file.write(image_bytes)

    return image_bytes


def bytes_to_base64(image_bytes: bytes) -> str:
    image_base64 = base64.b64encode(image_bytes).decode()
    return image_base64


def url_to_base64(url: str) -> Optional[str]:
    image_base64 = None

    if is_valid(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
        response = httpx.get(url, headers=headers)
        content = response.content
        image_base64 = bytes_to_base64(content)

    return image_base64
