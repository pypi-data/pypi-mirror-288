from starbear import H
from starbear.core.serve import bear


async def f(x):
    for i in range(x):
        yield i


@bear
async def app(page):
    async for entry in f(10):
        page.print(H.div(entry))
