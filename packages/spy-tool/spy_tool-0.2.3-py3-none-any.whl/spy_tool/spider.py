from abc import ABCMeta, ABC, abstractmethod
from spy_tool.mixins.cp_mixin import CpMixin
from spy_tool.project import camel_to_snake
from spy_tool.logger import logger


class SpiderMeta(ABCMeta):

    def __new__(mcs, name, bases, attrs):
        if attrs.get('name') is None:
            attrs['name'] = camel_to_snake(name)
        return super().__new__(mcs, name, bases, attrs)

    def __subclasscheck__(self, subclass):
        require_props = ('name',)
        require_props_check = all(hasattr(subclass, p) for p in require_props)

        required_methods = ('create_instance', 'start_requests', 'save_item')
        required_methods_check = all(hasattr(subclass, m) and callable(getattr(subclass, m)) for m in required_methods)

        return all([require_props_check, required_methods_check])


class Spider(ABC, metaclass=SpiderMeta):
    name: str

    def __repr__(self):
        return f'<Spider name: {self.name}>'

    __str__ = __repr__

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init__args = args
        self.__init__kwargs = kwargs

    @classmethod
    def create_instance(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    @abstractmethod
    def start_requests(self):
        pass

    @abstractmethod
    def save_item(self, item):
        pass


CpObject = type('CpObject', (CpMixin,), {'logger': logger})
CpSpider = type('CpSpider', (Spider, CpMixin), {'logger': logger})
