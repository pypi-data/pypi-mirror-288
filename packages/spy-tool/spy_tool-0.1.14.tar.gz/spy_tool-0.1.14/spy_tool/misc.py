import time
import socket
import inspect
from typing import List, Dict, Union, Coroutine, Any, Literal, Callable, Protocol, Generator, AsyncGenerator
from spy_tool.logger import logger

HOST_TYPE = Literal['local', 'public']


def get_host(host_type: HOST_TYPE = 'local') -> str:
    import httpx

    if host_type == 'local':
        return socket.gethostbyname(socket.gethostname())
    elif host_type == 'public':
        return httpx.get('https://api.ipify.org').text
    else:
        raise ValueError('Unsupported host_type!')


def chunk_data(data: List[Any], chunk_size: int) -> List[List[Any]]:
    return [data[i: i + chunk_size] for i in range(0, len(data), chunk_size)]


async def call_func(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    if not inspect.isroutine(func):
        raise ValueError('Unsupported func!')
    if inspect.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    return func(*args, **kwargs)


async def _sync_gen_func_result(func_result: Generator) -> AsyncGenerator:
    while True:
        try:
            yield next(func_result)
        except StopIteration as e:
            yield e.value
            break


class AsyncReturn(Exception):
    def __init__(self, value):
        self.value = value


async def _async_gen_func_result(func_result: AsyncGenerator) -> AsyncGenerator:
    while True:
        try:
            yield await anext(func_result)
        except AsyncReturn as e:
            yield e.value
            break
        except StopAsyncIteration:
            break


async def sync_async_gen_func_result(func_result: Union[Generator, AsyncGenerator, Coroutine, Any]) -> AsyncGenerator:
    if not inspect.isgenerator(func_result) and not inspect.isasyncgen(func_result):
        if inspect.iscoroutine(func_result):
            yield await func_result
        else:
            yield func_result
    else:
        async for item in _sync_gen_func_result(func_result) if inspect.isgenerator(func_result) \
                else _async_gen_func_result(func_result):
            async for i in sync_async_gen_func_result(item):
                yield i


async def async_gen_func(func: Callable[..., Any], *args: Any, **kwargs: Any) -> AsyncGenerator:
    func_result = await call_func(func, *args, **kwargs)
    async for item in sync_async_gen_func_result(func_result):
        yield item


def find_process_pids_by_process_name(process_name: str) -> List[int]:
    import psutil

    process_pids: List[int] = []
    for proc in psutil.process_iter(['pid', 'name']):
        proc_info: Dict[str, Any] = proc.info  # type: ignore
        try:
            if process_name.lower() in proc_info['name'].lower():
                proc_id = proc_info['pid']
                proc_name = proc_info['name']
                process_pids.append(proc_id)
                logger.success(f'Success find process_pid: {proc_id} proc_name: {proc_name}.')
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as exception:
            logger.success(f'Fail find process_name: {process_name}, exception: {exception}!')
    logger.success(f'Found process_pids: {process_pids}.')
    return process_pids


def kill_process_by_process_pid(process_pid: int) -> None:
    import psutil

    try:
        proc = psutil.Process(process_pid)
        proc.terminate()
        proc.wait(timeout=3)
        logger.success(f'Success kill process_pid: {process_pid}.')
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired) as exception:
        logger.error(f'Fail kill process_pid: {process_pid}, exception: {exception}!')


def kill_process_by_process_name(process_name: str) -> None:
    process_pids = find_process_pids_by_process_name(process_name)
    for process_pid in process_pids:
        kill_process_by_process_pid(process_pid)


class Container(Protocol):
    def __init__(self, database, key):
        self.database = database
        self.key = key

    def __len__(self) -> int:
        pass


def show_progress(container: Container, frequency: float = 1.0) -> None:
    import tqdm

    total_num = len(container)
    desc = f'{container.database} {container.key} consumption speed'
    unit = 'item'

    bar = tqdm.tqdm(desc=desc, total=total_num, leave=True, unit=unit)

    sum_num = 0
    while True:
        now_num = len(container)
        pass_num = total_num - now_num
        update_num = pass_num - sum_num
        sum_num += update_num

        bar.update(update_num)

        if sum_num == total_num:
            break

        time.sleep(frequency)


class Converter(object):
    """
    functions = {
        'a': {'b': self.a_to_b, 'c': self.a_to_c},
        'b': {'a': self.b_to_a, 'c': self.b_to_c},
        'c': {'a': self.c_to_a, 'b': self.c_to_b}
    }
    objects = {'a': a, 'b': b, 'c': c}

    def a_to_b(a):
        return a + 1

    def a_to_c(a):
        return a * 2

    def b_to_a(b):
        return b - 1

    def b_to_c(b):
        return (b - 1) * 2

    def c_to_a(c):
        return c // 2

    def c_to_b(c):
        return (c // 2) + 1

    """
    functions: Dict[str, Dict[str, Callable[..., Any]]]
    objects: Dict[str, Any]

    def convert(self) -> None:
        if all(v is None for v in self.objects.values()):
            raise ValueError(f'At least one of {", ".join(self.objects.keys())} must be provided and not None!')

        source_key, source_value = next((k, v) for k, v in self.objects.items() if v is not None)

        for target_key in self.objects:
            if self.objects[target_key] is not None:
                continue
            self.objects[target_key] = self.functions[source_key][target_key](source_value)
