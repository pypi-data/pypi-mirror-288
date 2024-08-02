import os
import uuid
import random
import ddddocr
from PIL import Image
from io import BytesIO
from DrissionPage import ChromiumPage
from DrissionPage.common import Actions
from typing import Optional, Literal, List, Tuple
from spy_tool.image import base64_to_bytes
from spy_tool.verify.bezier_curve import BezierCurve
from spy_tool.run.js import run_js_by_PyExecJS

TRACK_MODE_TYPE = Literal['bezier_curve', 'ghost_cursor']


class SlideVerify(object):

    @staticmethod
    def get_distance(background_image_base64: str, target_image_base64: str,
                     background_image_render_width: int,
                     image_filedir: Optional[str] = None) -> int:
        """

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

    @staticmethod
    def points_to_track(points: List[Tuple[int, int]], duration: float = .5) -> List[Tuple[int, int, float]]:
        track = []
        cur_x, cur_y = 0, 0
        for point in points:
            x, y = point
            cur_point = (x - cur_x, y - cur_y, duration)
            track.append(cur_point)
            cur_x, cur_y = x, y
        return track

    @classmethod
    def get_track_by_bezier_curve(cls,
                                  distance,
                                  numberList=random.randint(25, 45),
                                  le=4,
                                  deviation=10,
                                  bias=0.5,
                                  type=2,
                                  cbb=1,
                                  yhh=5) -> List[Tuple[int, int, float]]:
        """

        :param distance:
        :param numberList: 返回的数组的轨迹点的数量 numberList = 150
        :param le: 几阶贝塞尔曲线，越大越复杂 如 le = 4
        :param deviation: 轨迹上下波动的范围 如 deviation = 10
        :param bias: 波动范围的分布位置 如 bias = 0.5
        :param type: 0表示均速滑动，1表示先慢后快，2表示先快后慢，3表示先慢中间快后慢 如 type = 1
        :param cbb: 在终点来回摆动的次数
        :param yhh: 在终点来回摆动的范围
        :return:
        """
        bc = BezierCurve()
        res = bc.trackArray([0, 0], [distance, 0],
                            numberList, le=le, deviation=deviation, bias=bias, type=type, cbb=cbb, yhh=yhh)
        points = list(map(lambda _: (int(_[0]), int(_[1])), res["trackArray"].tolist()))
        track = cls.points_to_track(points)
        return track

    @classmethod
    def get_track_by_ghost_cursor(cls, distance: int) -> List[Tuple[int, int, float]]:
        js_code = '''function sdk(from,to){const{path}=require('ghost-cursor');return path(from,to)}'''
        result = run_js_by_PyExecJS(js_code, 'sdk', {'x': 0, 'y': 0}, {'x': distance, 'y': 0})
        points = [(i['x'], i['y']) for i in result]
        track = cls.points_to_track(points)
        return track

    @classmethod
    def get_track(cls, distance: int, track_mode: TRACK_MODE_TYPE = 'bezier_curve') -> List[Tuple[int, int, float]]:
        track = []
        if track_mode == 'bezier_curve':
            track = cls.get_track_by_bezier_curve(distance)
        elif track_mode == 'ghost_cursor':
            track = cls.get_track_by_ghost_cursor(distance)
        return track

    @classmethod
    def slide(cls, cp: ChromiumPage, ele_or_loc: str,
              background_image_base64: str, target_image_base64: str,
              background_image_render_width: int,
              image_filedir: Optional[str] = None,
              track_mode: TRACK_MODE_TYPE = 'bezier_curve', timeout: Optional[float] = None) -> None:
        distance = cls.get_distance(background_image_base64, target_image_base64,
                                    background_image_render_width=background_image_render_width,
                                    image_filedir=image_filedir)
        ac = Actions(cp)
        ac.move_to(ele_or_loc).hold()
        track = cls.get_track(distance, track_mode=track_mode)
        for i in track:
            ac.move(*i)
        ac.release()
        cp.wait.load_start(timeout)  # 用于等待页面进入加载状态
