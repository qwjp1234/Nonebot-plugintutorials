# 钩子函数

> Nonebot2官方教程: [钩子函数](https://v2.nonebot.dev/docs/advanced/runtime-hook)

#### 何为钩子函数?

​	在我的理解当中, 钩子函数相当于"监听"到某个事件发生后,将这个事件暂停,然后在其中插入自己想要的函数等,其实有点类似于装饰器

#### 钩子函数有哪些?

​	在nonebot2官方文档中, 钩子函数一共有10个, 如下

| 钩子名             | 调用                      | 说明                       |
| ------------------ | ------------------------- | -------------------------- |
| 启动准备           | @driver.on_startup        | 当bot启动时运行            |
| 终止处理           | @driver.on_shutdown       | 当bot关闭时运行            |
| Bot 连接处理       | @driver.on_bot_connect    | 当bot连接到websocket时运行 |
| bot 断开处理       | @driver.on_bot_disconnect | 当bot与websocket断开时运行 |
| bot api 调用钩子   | @Bot.on_calling_api       | 当bot调用API时运行         |
| bot api 调用后钩子 | @Bot.on_called_api        | 当bot调用API后运行         |
| 事件预处理         | @event_preprocessor       | 在nonebot接收到event时运行 |
| 事件后处理         | @event_postprocessor      | 在nonebot处理event后运行   |
| 运行预处理         | @run_preprocessor         | 在运行matcher前运行        |
| 运行后处理         | @run_postprocessor        | 在运行matcher后运行        |

#### 有什么用?

钩子函数的用处很多, 比如bot启动前的**资源效验和数据库连接**, bot关闭时的**进程终止**(比如playwright或se或数据库连接), 对接收到的event进行**统一处理**而不用分开写rule, event处理结束后的**数据存储**等等

#### 案例

- 资源效验(代码片段, 不可直接运行)

```python
from nonebot import get_driver

from .check_resources import check_res

driver = get_driver()
@driver.on_startup
async def _():
    check_res() #资源效验
```

- 进程终止(代码片段, 不可直接运行)

```python
from nonebot import get_driver

from .brower import shut

driver = get_driver()
@driver.on_shutdown
async def _():
    logger.info("正在关闭playwright...")
    global _playwright, _brower
    try:
        await shut(_brower, _playwright)
    except Exception as e:
        logger.error(e)
        logger.warning("playwright关闭失败!若卡死请直接kill本进程")
```

上述代码均来自[我的仓库](https://github.com/MRSlouzk/nonebot-plugin-azurlane-assistant/blob/master/nonebot-plugin-azurlane-assistant/__init__.py), 可以进行参考
