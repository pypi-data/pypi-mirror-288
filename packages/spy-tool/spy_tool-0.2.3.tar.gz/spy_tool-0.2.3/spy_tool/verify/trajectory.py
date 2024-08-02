import random
from typing import Literal, List, Tuple
from spy_tool.verify.bezier_curve import BezierCurve
from spy_tool.run.js import run_js_by_PyExecJS


class Trajectory(object):

    @staticmethod
    def points_to_trajectories(points: List[Tuple[int, int]], duration: float = .02) -> List[Tuple[int, int, float]]:
        trajectories = []
        cur_x, cur_y = 0, 0
        for point in points:
            x, y = point
            offset_x, offset_y = x - cur_x, y - cur_y
            trajectory = (offset_x, offset_y, duration)
            cur_x, cur_y = x, y
            trajectories.append(trajectory)
        return trajectories

    @classmethod
    def get_points_by_bezier_curve(cls,
                                   distance: int,
                                   numberList=random.randint(25, 45),
                                   le=4,
                                   deviation=10,
                                   bias=0.5,
                                   type=2,
                                   cbb=1,
                                   yhh=5) -> List[Tuple[int, int]]:
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
        result = bc.trackArray([0, 0], [distance, 0],
                               numberList, le=le, deviation=deviation, bias=bias, type=type, cbb=cbb, yhh=yhh)
        result = result['trackArray'].tolist()
        points = [(i[0], i[1]) for i in result]
        return points

    @classmethod
    def get_points_by_ghost_cursor(cls, distance: int) -> List[Tuple[int, int]]:
        js_code = '''function sdk(from,to){const{path}=require('ghost-cursor');return path(from,to)}'''
        result = run_js_by_PyExecJS(js_code, 'sdk', {'x': 0, 'y': 0}, {'x': distance, 'y': 0})
        points = [(i['x'], i['y']) for i in result]
        return points

    @classmethod
    def distance_to_trajectories(cls,
                                 distance: int,
                                 trajectory_mode: Literal['bezier_curve', 'ghost_cursor'] = 'bezier_curve',
                                 duration: float = .02) -> List[Tuple[int, int, float]]:
        if trajectory_mode == 'bezier_curve':
            points = cls.get_points_by_bezier_curve(distance)
        elif trajectory_mode == 'ghost_cursor':
            points = cls.get_points_by_ghost_cursor(distance)
        else:
            raise ValueError(f'Unsupported trajectory_mode!')
        trajectories = cls.points_to_trajectories(points, duration)
        return trajectories
