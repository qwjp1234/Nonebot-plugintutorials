from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
from nonebot import on_command
from nonebot.internal.params import Arg, ArgPlainText
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import CommandArg
from urllib import parse

'''@触发人
http://o0a.cn/BbZCNd    #目标网站
以上是我搜索到的结果
-------------
若链接无法打开请复制
链接到浏览器打开
'''
'''
需求
1.设定关键群
2.关键词”搜“触发指令
3.对目标网站爬虫，截取对应电影的url
'''
"配置项"
qq_qun = [415989402, 985028631]  # 开启的群
url = "https://zjuba.vip/index.php/vod/search.html?wd="  # 目标网站


# "饥荒攻略备份（自用）：415989402"


# 判断是不是设定的关键群
async def user_checker(event: GroupMessageEvent) -> bool:
    # 判定群聊id是不是设定群
    return event.group_id in qq_qun


YiNgs = on_command("搜", rule=user_checker, )


# 开始请求目标网站url
@YiNgs.handle()
async def get_url(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    # 判断 命令后面的参数，有的话进入if
    if plain_text:
        # set_arg设置/覆盖一个 got 接收的参数。
        matcher.set_arg("city", args)  # 如果用户发送了参数则直接赋值


# got 装饰器会中断当前事件处理流程，等待接收一个新的事件got 装饰器用于接收一条消息，并且可以控制是否向用户发送询问 prompt 等，更贴近于对话形式会话。
# Arg获取某次 got 接收的参数。
# ArgPlainText 获取某次 got 接收的参数的纯文本部分。
@YiNgs.got("city", prompt="你想查询什么电影呢？")
async def handle_city(city: Message = Arg(), city_name: str = ArgPlainText("city")):
    city_weather = await get_weather(city_name)
    # finish 向用户回复一条消息（可选），并立即结束当前事件的整个处理流程。
    await YiNgs.finish(city_weather + '\n' + '以上是我搜索到的结果\n-------------\n若链接无法打开请复制\n链接到浏览器打开')


async def get_weather(city: str) -> str:
    return url + parse.quote(city)
