# 实例1 不要乱戳！

难度：★★

作者：[MRSlouzk](https://github.com/MRSlouzk)

> [Nonebot2插件编写教程 EP4-不要戳啦](https://www.bilibili.com/video/BV16U4y1r7ze) *([MRSlou1](https://space.bilibili.com/634651362))*

### 功能

当bot被戳一戳时，如果对方在允许列表里，则发送蹭蹭的图片，若不在则@戳的人并且让他不要再戳了。

### 要点

- 戳一戳检测
- 判断是否在列表里
- 发送图片

### 实现

##### 戳一戳检测

```python
from nonebot import on_notice
from nonebot.adapters.onebot.v11 import PokeNotifyEvent

def _check(event: PokeNotifyEvent):
    return event.target_id == event.self_id

poke=on_notice(rule=_check)

@poke.handle()
async def _(event: PokeNotifyEvent):
    pass
```

检测“戳一戳”事件调用的是Nonebot中的[on_notice](https://v2.nonebot.dev/docs/api/plugin/on#on_notice)(通知事件)。当bot接收到一个`notice`事件时，会先根据`rule`参数当中的规则函数`_check`判断是否为戳一戳事件*(注：因为规则函数传参已经规定了必须是`PokeNotifyEvent`(戳一戳事件)，所以如果传入的不是这个参数默认判定为False，就相当于传入Event后再使用`if(isinstance(event, PokeNotifyEvent))`)*，然后在函数体里面判断被戳的人是不是bot自己，如果是的话才会返回True。

```python
agree_list=[123,112]

@poke.handle()
async def _(event: PokeNotifyEvent):
    if(event.user_id in agree_list):
        pass
```

这个是最简单的，熟悉Python的列表(List)类型变量的操作就行。`in`关键字用于判断列表中是否有某一变量(必须是同一种类型！比如`1 in ["1"]`就会返回False)。

##### 发送图片

```python
await poke.finish(MessageSegment.image(file=r"file:///E:\Code\plugins\poke\resources\1.png"))
```

发送图片调用的是消息段(MessageSegment)类中的`image`方法，直接读取对应路径下的文件，然后发送出去，MessageSegment支持发送的消息类型详见[Onebot文档](https://github.com/botuniverse/onebot-11/blob/master/message/segment.md)。

#### 完整代码

```python
from nonebot import on_notice
from nonebot.adapters.onebot.v11 import PokeNotifyEvent, Message, MessageSegment

def _check(event: PokeNotifyEvent):
    return event.target_id==event.self_id

agree_list=[3237231778]

poke=on_notice(rule=_check)

@poke.handle()
async def _(event: PokeNotifyEvent):
    if(event.user_id in agree_list):
        await poke.finish(MessageSegment.image(file=r"file:///E:\Code\plugins\poke\resources\1.png"))
    else:
        await poke.finish(Message(f"[CQ:at,qq={event.user_id}]不要再戳了!"))
```

