# 如何发送合并转发消息

> 看本教程前请先看完[**gocq-api.md**](https://github.com/MRSlouzk/Nonebot-plugintutorials/blob/main/%E7%9F%A5%E8%AF%86%E7%90%86%E8%AE%BA/gocq-api.md)

本篇教程讲一讲如何进行合并转发消息的发送

根据[Gocq文档](https://docs.go-cqhttp.org/api/#%E5%8F%91%E9%80%81%E5%90%88%E5%B9%B6%E8%BD%AC%E5%8F%91-%E7%BE%A4)的描述，合并转发消息可以看做是一个**由消息节点构成的列表**，要发送合并转发消息必须先**构建消息节点**，消息节点的格式如下

```json
{
    "type": "node",
    "data": {
        "name": name,
        "uin": uin,
        "content": msg
    }
}
```

其中`name`为合并转发消息当中发送消息的人显示的名字，`uin`为发送者QQ(用于显示头像)，`content`为具体消息内容

我们可以通过下面的代码实现消息节点的构建

```python
def to_node(msg: Message):
        return {"type": "node", "data": {"name": "demo-bot", "uin": 1234567, "content": msg}}
```

再来看api的调用

```python
#群聊合并转发消息
await bot.call_api(
            "send_group_forward_msg", group_id=event.group_id, messages=messages
        )
#私人合并转发消息
await bot.call_api(
            "send_private_forward_msg", user_id=event.user_id, messages=messages
        )
```

group_id以及private_id不用多讲，后面的`messages`传入的是消息节点<u>**列表**</u>

------

完整代码如下

```python
async def send_forward_msg(
        bot: Bot,
        event: Event,
        name: str,
        uin: str,
        msgs: List[Message]
):
    """
    :说明: `send_forward_msg`
    > 发送合并转发消息
    :参数:
      * `bot: Bot`: bot 实例
      * `event: GroupMessageEvent`: 群聊事件
      * `name: str`: 名字
      * `uin: str`: qq号
      * `msgs: List[Message]`: 消息列表
    """

    def to_node(msg: Message):
        return {"type": "node", "data": {"name": name, "uin": uin, "content": msg}}

    messages = [to_node(msg) for msg in msgs]
    is_private = isinstance(event, PrivateMessageEvent)
    if(is_private):
        await bot.call_api(
            "send_private_forward_msg", user_id=event.user_id, messages=messages
        )
    else:
        await bot.call_api(
            "send_group_forward_msg", group_id=event.group_id, messages=messages
        )
```

