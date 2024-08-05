class PreventDuplicateExecution(object):
    def __init__(self, method):
        self.method = method
        self.previous_args = None
        self.previous_kwargs = None

    def __get__(self, instance, owner):
        if instance is None:
            return self
        # 返回一个绑定到实例的方法
        return lambda *args, **kwargs: self._execute_if_new(instance, *args, **kwargs)

    def _execute_if_new(self, instance, *args, **kwargs):
        # 检查参数是否与上次调用相同, 如果相同则跳过方法执行
        if args == self.previous_args and kwargs == self.previous_kwargs:
            return
        result = self.method(instance, *args, **kwargs)
        self.previous_args = args
        self.previous_kwargs = kwargs
        return result
