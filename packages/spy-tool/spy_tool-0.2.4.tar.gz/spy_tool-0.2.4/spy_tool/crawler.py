import asyncio
from typing import Type, Any
from spy_tool.spider import Spider
from spy_tool.misc import async_gen_func


def crawl(spider_cls: Type[Spider], *init_args: Any, **init_kwargs: Any) -> None:
    async def _crawl():
        if not issubclass(spider_cls, Spider):
            raise TypeError(f'Spider_cls: {spider_cls} does not fully implemented required interface!')
        spider_ins = spider_cls.create_instance(*init_args, **init_kwargs)
        start_requests = spider_ins.start_requests
        async for item in async_gen_func(start_requests):
            spider_ins.save_item(item)

    asyncio.run(_crawl())
