import os
import uuid
import ddddocr
from PIL import Image
from io import BytesIO
from DrissionPage import ChromiumPage
from DrissionPage.common import Actions
from DrissionPage.items import ChromiumElement
from typing import Union, Optional, Literal, List, Tuple
from spy_tool.image import base64_to_bytes
from spy_tool.verify.trajectory import Trajectory


class DoubleImageSlider(object):

    @staticmethod
    def get_distance(
            background_image_base64: str,
            target_image_base64: str,
            background_image_render_width: int,
            image_filedir: Optional[str] = None) -> int:
        """
        获取双图像滑块滑动距离
        :param background_image_base64: 背景图片 base64 字符串
        :param target_image_base64: 目标图片 base64 字符串
        :param background_image_render_width: 背景图片 (渲染宽度)
        :param image_filedir: 图片保存目录
        :return:
        """
        name = str(uuid.uuid1()).replace('-', '')

        # 文件名不加文件扩展名
        background_image_filename = f'background-image-{name}'
        target_image_filename = f'target-image-{name}'

        background_image_filepath = os.path.join(image_filedir, background_image_filename) if image_filedir else None
        target_image_filepath = os.path.join(image_filedir, target_image_filename) if image_filedir else None

        background_image_bytes = base64_to_bytes(background_image_base64, background_image_filepath)  # 背景图片
        target_image_bytes = base64_to_bytes(target_image_base64, target_image_filepath)  # 目标图片

        # ddddocr 识别
        det = ddddocr.DdddOcr(ocr=False, det=False, show_ad=False)
        res = det.slide_match(target_image_bytes, background_image_bytes, simple_target=True)
        x = res['target'][0]  # 目标图片在背景图片上需要移动的距离 (原始图)

        background_image = Image.open(BytesIO(background_image_bytes))
        background_image_original_width = background_image.size[0]  # 背景图片 (原图宽度)
        x *= (background_image_render_width / background_image_original_width)  # 目标图片在背景图片上需要移动的距离 (渲染图)
        distance = round(x)  # 取整

        return distance

    @classmethod
    def slide(cls, cp: ChromiumPage,
              ele_or_loc: Union[str, ChromiumElement],
              distance: int,
              trajectory_mode: Literal['bezier_curve', 'ghost_cursor'] = 'bezier_curve',
              duration: float = .02,
              timeout=None) -> List[Tuple[int, int, float]]:
        ac = Actions(cp)
        ac.move_to(ele_or_loc).hold()
        trajectories = Trajectory.distance_to_trajectories(distance, trajectory_mode=trajectory_mode, duration=duration)
        for trajectory in trajectories:
            ac.move(*trajectory)
        ac.release()
        cp.wait.load_start(timeout)  # 用于等待页面进入加载状态
        return trajectories
