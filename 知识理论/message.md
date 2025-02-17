# 消息的处理

> [Nonebot2插件编写教程 EP1-关键词触发与消息发送](https://www.bilibili.com/video/BV1KN4y1T7JR) *([MRSlou1](https://space.bilibili.com/634651362))*

### NB平台扮演的角色

> 有做过Web开发的会更好理解

以OneBot适配器举例，机器人后台接收消息时会经过如下流程：首先gocqhttp会从QQ服务器获取消息，然后通过接口将消息传输给Nonebot后端，Nonebot将消息处理的结果再发还给gocqhttp端，最后gocqhttp根据发还的数据向QQ服务器发出消息，这就是消息收发与处理的整个流程。

简单来说gocqhttp就是实现Nonebot和QQ服务器之间通信的桥梁，也就是眼睛耳朵鼻子或者说身体的各个部位，而Nonebot就是相当于"大脑"，负责处理接收到的信息并且发送指令给手、脚这种身体部位让他们行动，这就是形象化的过程。

### 由关键字触发体验简单的消息处理

首先先看一段代码

```python
from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import Message

word=on_keyword({"你是谁"})

@word.handle()
async def _():
    await word.finish(Message("我是bot!"))
```

这段代码实现的功能是：如果有人发送（无论是与机器人的私聊还是群聊里）任一包含"你是谁"这三个关键字的消息的时候，机器人会回复消息：“我是bot”。功能是很简单，但是里面的基础知识点不少，下面逐一分析一下

------

```python
from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import Message
```

这段import代码的是从nonebot库中引入`on_keyword`方法，再从Onebot V11库中引入`Message`类，这两个东西的具体用法我们之后再谈<u>(至于**方法**这个词具体是什么意思请去看《面向对象编程》，在这你可以简单理解为一个函数就行)</u>，接下来要先聊聊这个import。

如同其他第三方库，Nonebot2中的很多功能都需要通过import导入后才能使用，虽然你也可以通过无脑`from nonebot import *`这种办法来一劳永逸，但不保证这样会不会出一些奇奇怪怪的问题，所以我的建议是需要什么方法就导入什么方法。**那么我怎么知道从哪些库里引入我想要的函数呢？**这里我列举了一些常见库里包含的常见函数，可以供大家参考

| 库                          | 常用函数/方法                                                | 说明       |
| --------------------------- | ------------------------------------------------------------ | ---------- |
| nonebot                     | on_message，on_notice，on_request，on_keyword，on_command，on_regex | 基础库     |
| nonebot.config              | Config                                                       | 配置文件库 |
| nonebot.matcher             | Matcher                                                      | 事件响应器 |
| nonebot.params              | Arg，State，CommandArgs，RegexMatched                        | 参数库     |
| nonebot.permission          | SUPERUSER，Permission                                        | 权限库     |
| nonebot.log                 | logger，default_format                                       | 日志库     |
| nonebot.adapters.onebot.v11 | Bot，Message，MessageSegment，Event，PRIVATE，GROUP等        | Onebot库   |

> (注：OneBot V11的库可以从`nonebot.adapters.onebot.v11`直接导入，也可以用诸如`nonebot.adapters.onebot.v11.message`的方式导入，详见[官方文档](https://onebot.adapters.nonebot.dev/docs/api/v11))
>

------

```python
word=on_keyword({"你是谁"})
```

这行代码的含义是“<u>创建一个名为word的变量，其为一个类型为on_keyword的事件响应器</u>”，那么是什么意思呢？

[^事件响应器]: 事件响应器顾名思义，是**在某个特定事件发生的时候会被触发的一段代码**。比如上述的`on_keyword`是当检测到接收到的消息中包含某些特定关键词后触发的。那么接收到之后如何处理？请耐心看下去。

*~~首先是“注册”，注册其实类似于C语言里面的函数声明，函数必须在声明后才可以使用，事件响应器（具体是什么不急着谈）也是如此。简单来说你想建个房子，但你建房子之前必须要指定一块地说我要在这里建房子才行，而不能直接就建房子，响应器注册就是指定一个变量（土地）来建房子（响应器），这个声明也同时指定了该事件响应器的触发条件，即在什么样的条件下才会触发响应器。这里面的`word`是事件响应器的名字，可以在符合Python变量命名法的前提下随便取名，这个名字在之后使用事件响应器时会使用到。~~*

python当中的变量使用前不需要声明，而可以直接赋值。上述代码就相当于先创建一个类型为`on_keyword`的事件响应器，再赋值给一个名为word的变量，使其成为一个事件响应器。

------

接下来是`on_keyword`，前面说过`on_keyword`是NoneBot库中的一个方法，这个方法会创建一个事件响应器，那它能输入什么参数呢？先来看看文档中的说明：

> `on_keyword(keywords, rule=..., *, permission=..., handlers=..., temp=..., priority=..., block=..., state=...)`     *<u>注册一个消息事件响应器，并且当消息纯文本部分包含关键词时响应</u>*
>
> 第一个参数是`keywords`，类型为集合(Set)，传入的是用来触发该响应器工作的关键词集合(用{}包起来的)。
>
> 第二个参数是`rule`，传入的是bool类型规则函数或者Rule类。
>
> 第三个参数是`permission`，传入的是bool类型的权限函数或者Permission类。
>
> 第四个参数是`handlers`，传入的参数是被事件响应器触发的函数列表。
>
> 第五个参数是`temp`，传入的是bool类型参数，若为True则此响应器只会使用一次。
>
> 第六个参数是`priority`，传入的是int型参数，用于设定响应器的优先级。**注意！此参数越大优先级越低**。
>
> 第七个参数是`block`，传入的是bool类型的参数，若为True则不会注册优先级小于此响应器的响应器，相当于消息被阻断在这里了。
>
> 最后一个参数是`state`，传入的是字典类型参数，用于存储响应器状态信息。
>

目前需要了解的只有`keywords`，`permission`，`priority`和`block`这四个参数，其他参数用法较为麻烦，我们之后才会讲到，所以可以先放着。

首先是`keywords`参数，这个参数作用比较简单，就是传入一个元素是字符串的[集合](https://www.runoob.com/python3/python3-set.html)，然后如果接收到的消息包含这个集合内的任一关键字，则触发该事件响应器。

第二个是`permission`参数，这个参数负责传入能触发此事件响应器的消息发送者类型，也就是哪些人能触发这个响应器。一般来说重要的指令都会加上一些权限限制，诸如操作机器人后台的一些指令。常见的permission有SUPERUSER(写在.env文件中的超级用户)，GROUP_ADMIN(群管理员)和GROUP_OWNER(群主)，这些是框架本身提供的。除此以外我们也可以自定义权限组，当然这个内容之后再谈。

第三个参数是`priority`，负责调控响应器触发的优先级，优先级越高，就越早被执行。举个例子，如有以下代码

```python
word=on_keyword({"你是谁"},priority=60)
word_2=on_keyword({"你是谁"},priority=50)
```

两个响应器都以"你是谁"作为触发词，这时候如果接收到了包含"你是谁"的消息后，二者执行顺序就由`priority`值来决定了。注意！`priority`**值越小，优先级越高**！如上面那个例子中word_2就会比word要更早触发。

最后一个介绍的是`block`参数，这个参数一般情况下是和前面那个`priority`参数搭配起来用，用以阻断消息传递。还是以上面那段代码为例

```python
word=on_keyword({"你是谁"},priority=60,block=True)
word_2=on_keyword({"你是谁"},priority=50,block=True)
```

用户输入"你是谁"后并不会触发两个响应器，而是只会触发优先级更高的那个也就是word_2，触发完之后因为`block`值为True，所以消息传到这里就被阻断了，也就没办法触发优先级更低的响应器了。

------

```python
@word.handle()
async def _():
    await word.finish(Message("我是bot!"))
```

接下来这一段代码是响应器最重要的一部分，是核心功能模块，响应器被触发后会执行这段代码的内容，没有这部分事件响应器也只是单纯的一个空壳。

`@word.handle()`，这个是函数的"[装饰器](https://v2.nonebot.dev/docs/tutorial/plugin/create-handler)"，说简单点就是给下面定义的函数标明：<u>这个函数是用来处理事件响应器的！</u>，当然这个装饰器的其它用法目前不用了解，我们之后会慢慢讲到，现在只需要知道必须在处理响应器触发的函数前加上这个就行，格式为`@响应器名.handle()`。

接下面的`async def`意思是定义一个[异步(协程)函数](https://www.jianshu.com/p/0957c30e85bf)，Nonebot的事件响应器处理的主函数应当都是异步函数，而子函数(主函数中包含的函数)视情况而定。`async def _()`即定义一个没有任何参数，也没有函数名字的异步函数。如果懒得给主函数命名，使用`_`代替就行，不过如果为了辨识度高一点的话而命名那随意，之后也会有需要用到函数名字的地方。此外这还是个无参函数，事件响应器处理函数的参数传递(即[依赖注入](https://v2.nonebot.dev/docs/advanced/di/dependency-injection))我们之后再谈，这里的例子只是一个简单的消息触发与回复，并不需要传入任何参数。

`await word.finish(Message("我是bot!"))`，这段代码用来结束名为`word`的事件响应器，同时发送一个消息(Message)<u>"我是bot"</u>。事件响应器中对响应器进行的操作一般都需要加上`await`才能使用，否则会报错，比如此处的`word.finish`。`word.finish`用以执行事件响应器`word`下的`finish`方法，`finish`方法可以结束该事件响应器。`finish`方法可以不传入任何参数，如`word.finish()`，也可以传入**字符串(Str)/消息(Message)/格式化消息模板(MessageTemplate)/消息段(MessageSegment)**这四种类型的参数，在上面的例子中我们传入的是一个消息(Message)类型的参数。

> 此处也可以使用`await word.send("我是bot！")`，因为函数执行完后会自动结束响应器

> 上述的代码我们也可以直接使用`await word.finish("我是bot!")`来替代，原因下面会讲到。

到此就讲完了从消息接收、处理到发送的全部流程，此时大家应该对插件的运行机制有了一些基本的了解，接下来我们会开始更深入的讨论。

### 如何在群里@向我@的人？

> [Nonebot2插件编写教程 EP3-如何@回@我的人](https://www.bilibili.com/video/BV1be4y1Q7Eg) *([MRSlou1](https://space.bilibili.com/634651362))*

标题可能看起来有点绕，详细解释一下的话意思就是我(bot)如何在一个QQ群里@在刚刚向我(bot)发送@消息的人。

首先来分析一下这个问题，要实现上述功能我们需要解决以下三个难题：<u>如何知道TA发送的消息是在@我(bot)</u>，<u>如何知道是谁在给我发送消息@我</u>以及<u>如何@回去</u>。

------

我们先一步一步来解决这个问题，首先是第一个难题：<u>如何知道TA发送的消息是在@我</u>。这里就需要讲到事件响应器的`rule`参数了,上个例子中的`on_keyword`就有这个参数，现在来详细讲一讲。`rule`翻译过来即”规则“，用于规定触发事件响应器的条件，可以理解为在事件响应器外面套了一个if判断，条件满足时才会触发事件响应器，不满足的时候会直接跳过。说了这么多但`rule`参数的本质其实就是一个bool类型的变量或者返回值类型为bool的函数，当`rule`值为`True`时即可以触发事件响应器，反之为`False`时则不会触发，对，就是这么简单，接下来来讲讲如何使用rule以及如何解决我们上面的问题。

> 或许有人会问在响应器处理函数当中判断是否符合条件和rule的功能是不是一样的?虽然作用上两者一样，但是rule相当于从源头上"掐断"该事件响应器，而处理函数是从中途阻止。

```python
from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import Event

def _checker(event: Event) -> bool :
    return event.message_type=="group"

word=on_keyword({"你是谁"},rule=_checker)
```

上面这个例子是个规则函数的简单应用。因为还没有讲到响应器处理函数的参数传递，所以先不细讲，大家只需要知道这个`_checker`函数是用来判断接收到的消息类型是否为群聊消息就行。当消息类型为`group`，即群聊消息时返回`True`，反之返回`False`，之后在消息传递到名为`word`的事件响应器时，首先会根据`rule`参数对应的规则函数`_checker`进行处理然后返回bool值，之后再决定要不要触发事件响应器。其作用相当于下面这段代码**(仅仅只是一个例子，不要这么写!!!)**

```python
if(event.message_type=="group"):
    word=on_keyword({"你是谁"})
#此段是无效代码，请不要这么写!!!
```

嘛，现在回到我们刚刚那个例子，即如何知道TA是在@我？这里有两种方法，一种是自己写规则函数，另一种则是调用Nonebot中内置的`to_me`方法。

**法一**

```python
from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import GroupMessageEvent

def _checker(event: GroupMessageEvent) -> bool :
    return event.to_me

word=on_keyword({"你是谁"},rule=_checker)
```

**法二**

```python
from nonebot import on_keyword
from nonebot.rule import to_me

word=on_keyword({"你是谁"},rule=to_me())
```

法二中的`to_me`是Nonebot框架自带的一个方法，用于检测消息中是否有在@自己(bot)。

------

第二个问题：<u>如何知道是谁在给我发送消息@我</u>。这个要涉及到事件响应器的参数传递，下面我们详细讲讲。

> 参数传递正式的名字应该叫"**依赖注入**"，不过有点讲顺口了，并且参数传递听起来好理解一点所以就这么说了。

事件响应器函数常用的传入参数一般有以下三种：bot(机器人)，event(事件)以及args(参数)，不过除此之外还有state,match等。这里我们先只讲前两个，第三个args参数我们暂时还用不到。

首先是第一种参数：bot，bot类型的传入参数类就只有一个：[Bot](https://v2.nonebot.dev/docs/api/adapters/index#Bot)，下面是使用样例

```python
from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import Bot

word=on_keyword({"你是谁"})

@word.handle()
async def _(bot: Bot):
    await word.finish(str(bot.self_id))
```

在上述代码中可以看到，`Bot`作为一个参数传入事件响应器函数当中使用。`Bot`是Nonebot库提供的一个类，当使用机器人的时候会自动创建一个`Bot`类，然后我们可以通过这个类来调用与机器人交互的各种[属性与方法](https://blog.csdn.net/weixin_46351593/article/details/119892412)。比如上面例子当中的`self_id`就是`Bot`类的一个属性，返回的数据是当前bot的QQ号，类型为int(所以才要转换为str类型，不然会报参数类型不匹配的错误，因为finish方法不支持传入int型参数)。

Bot类有如下的属性

| 属性名  | 返回值类型          | 说明                       |
| ------- | ------------------- | -------------------------- |
| self_id | int(整数型)         | 机器人自己的QQ号           |
| adapter | adapter(协议适配器) | 返回机器人所用的协议适配器 |

还有一些个人认为的Bot中**比较常用的方法**，因为篇幅限制其他方法以及具体的参数传递就不讲了，可以自行翻阅[文档](https://github.com/botuniverse/onebot-11/blob/master/api/public.md)。

| 方法名                 | 作用                   |
| ---------------------- | ---------------------- |
| send_msg               | 发送(群聊/私聊)消息    |
| delete_msg             | 撤回消息               |
| set_group_ban          | 设置群组禁言           |
| set_friend_add_request | 设置好友验证是否通过   |
| set_group_add_request  | 设置加群验证是否通过   |
| get_login_info         | 获取登录信息           |
| get_group_member_info  | 获取指定群成员信息     |
| get_group_honor_info   | 获取群荣誉(龙王等)信息 |

接下来是第二种参数：event事件参数，event类型其实包含很多类：如Event，GroupMessageEvent，PrivateMessageEvent等等。Event类一些方法/属性和Bot类重复，比如`self_id`等，不过由于Event类下的方法/属性相较于Bot类更多，且通用性更好，所以要获取的信息相同时一般常用Event类来代替Bot类。下面列举了一些常见的Event类

| 类名                     | 说明                              |
| ------------------------ | --------------------------------- |
| Event                    | 事件                              |
| GroupMessageEvent        | 群消息事件                        |
| PrivateMessageEvent      | 私聊消息事件                      |
| NoticeEvent              | 通知事件                          |
| GroupUploadNoticeEvent   | 群文件上传事件                    |
| GroupAdminNoticeEvent    | 群管理员变动事件                  |
| GroupDecreaseNoticeEvent | 群人数减少事件                    |
| GroupIncreaseNoticeEvent | 群人数增加事件                    |
| GroupBanNoticeEvent      | 群管理员禁言事件                  |
| FriendAddNoticeEvent     | 好友增加事件                      |
| GroupRecallNoticeEvent   | 群消息撤回事件                    |
| FriendRecallNoticeEvent  | 私聊消息撤回事件                  |
| NotifyEvent              | *<u>提醒事件</u>*(这个文档没翻到) |
| PokeNotifyEvent          | 群戳一戳事件                      |
| HonorNotifyEvent         | 群荣誉变更事件                    |
| LuckyKingNotifyEvent     | 群红包运气王事件                  |
| RequestEvent             | 请求事件                          |
| FriendRequestEvent       | 好友申请事件                      |
| GroupRequestEvent        | 入群申请事件                      |

虽然没全部列举出来，但是这些类目前来说已经完全够用了，如何知道它们下面有哪些属性和方法呢？有两种方法：一是查阅[官方文档](https://github.com/botuniverse/onebot-11/tree/master/event)，二是在支持代码补全的编辑器中输入对应的类名后再加上`.`就可以跳出对应的提示，然后可以根据语法提示选择需要的方法/属性就行了。

最后再附上一个具体例子

```python
from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import Message,GroupMessageEvent

word=on_keyword({"你是谁"})

@word.handle()
async def _(event:GroupMessageEvent):
    if(event.user_id==123456 and event.group_id==654321):
        await word.finish(Message("Done!"))
```

> 此段代码作用：当群聊654321中里有一个QQ号为123456的人发送包含“你是谁”这三个字的句子时，bot会发送“Done”。
>

回到我们最初的问题：<u>如何知道是谁在给我发送消息@我</u>？现在答案就明了了，参见以下代码

```python
from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import Message,GroupMessageEvent
from nonebot.rule import to_me

word=on_keyword({"你是谁"},rule=to_me())

@word.handle()
async def _(event:GroupMessageEvent):
    uid=event.user_id
    await word.finish(Message(str(uid)))
```

事件响应器主函数当中的变量uid即为我们获取到的“**给我们发送消息的人**”的QQ号，类型为int型。

------

最后我们要解决的问题是：<u>如何@回去</u>，在此之前我们需要了解一下Onebot的消息类型。上面我们曾提到`word.finish()`方法可以传入四种参数：**字符串(Str)/消息(Message)/格式化消息模板(MessageTemplate)/消息段(MessageSegment)**，其中[格式化消息模板](https://v2.nonebot.dev/docs/api/adapters/index#MessageTemplate)用法比较特殊，暂且避开不谈，只讲剩下三种。

> 字符串(Str)与消息(Message)大部分情况下可以等价，可以替代Message使用，但是有一种特殊情况：消息内包含CQ码的时候只能使用Message，个人建议还是统一使用Message来进行消息发送。
>

##### 什么是CQ码？

[CQ码](https://docs.go-cqhttp.org/cqcode/#%E8%BD%AC%E4%B9%89)是go-cqhttp协议中的一种特殊的消息字段，用以发送QQ中的特殊消息(如图片、语音、@等等)，常见的CQ码格式为`[CQ:类型,参数=值,参数=值]`，如下面的例子就是CQ码的一种使用

```python
#因为QQ接口的问题，此CQ码现在已经无法正常使用，会报错"消息可能被风控"，可以尝试其他的CQ码。
@word.handle()
async def _():
    await word.finish(Message("[CQ:share,url=https://www.baidu.com,title=百度]"))
```

上述代码发送了一个百度的链接(不是以文字链接的方式)，而是一个可以点击的类似“小程序”的执行框，点击后可以直接跳转。**(因为QQ接口的问题，此CQ码有时候会无法使用，会报错"<u>消息可能被风控</u>"，请尝试其他的CQ码。)**

这里我列举了一些常见的CQ码，全部的CQ码请查阅[go-cqhttp文档](https://docs.go-cqhttp.org/cqcode/#%E8%BD%AC%E4%B9%89)或者[OneBot文档](https://github.com/botuniverse/onebot-11/blob/master/message/segment.md)。

| 类型   | 参数                                                         | 作用                              |
| ------ | ------------------------------------------------------------ | --------------------------------- |
| face   | id=表情ID                                                    | 发送QQ内的表情                    |
| record | file=文件路径/URL                                            | 发送语音(一般为mp3格式)           |
| at     | qq=QQ号，(name=昵称)                                         | @某人(不在群里时可以使用name参数) |
| share  | url=网站链接，name=网站名                                    | 发送网站分享                      |
| music  | type=歌曲平台，id=歌曲ID                                     | 发送音乐                          |
| image  | 参数较多，参见[文档](https://docs.go-cqhttp.org/cqcode/#%E5%9B%BE%E7%89%87) | 发送图片                          |
| reply  | id=回复的消息ID，text=消息内容                               | 发送回复消息                      |

------

回到刚刚的代码，`word.finish(Message("[CQ:share,url=https://www.baidu.com,title=百度]"))`是正确的用法，但如果使用的是`word.finish("[CQ:share,url=https://www.baidu.com,title=百度]")`，虽然不会报错，但是go-cqhttp无法识别到CQ码，这样子输出的内容直接就是CQ码本身的文本内容，这点显然不是我们想要的。

不过CQ码不是唯一实现发送特殊消息的方式，除了CQ码之外还有一种叫**消息段(MessageSegment)**的东西，可以实现与CQ码相同的功能，并且还可以做一些CQ码无法做到的事情。此外**<u>官方推荐使用消息段来替代CQ码</u>**(原因：CQ码不方便+容易被注入)，后续案例也都会使用消息段。用法如下

```python
@word.handle()
async def _():
    await word.finish(MessageSegment.share(url="https://www.baidu.com",title="百度"))
```

这段代码与上面的`[CQ:share,url=https://www.baidu.com,title=百度]`功能是一致的，但是使用MessageSegment方式发送特殊消息更加方便明了(还不用去查文档，打出来IDE就会给语法提示)，减轻了编写与后期维护的压力。

> PS：MessageSegment和Message可以通过"+"直接拼在一起，形成"文字+图片"类型的消息，另外Message之间也可以相互拼接。Message相当于一个数组，可以容纳一定数量的同类(Message)以及MessageSegment

现在相信大家已经能解决我们的最后一个问题：<u>如何@回去</u>。示例代码如下，分别使用了CQ码和消息段形式

**CQ码**

```python
from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import Message,GroupMessageEvent
from nonebot.rule import to_me

word=on_keyword({"你是谁"},rule=to_me())

@word.handle()
async def _(event: GroupMessageEvent):
    await word.finish(Message(f"[CQ:at,qq={event.user_id}],你@我了!"))
```

**消息段(推荐!!!)**

```python
from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import Message,GroupMessageEvent,MessageSegment
from nonebot.rule import to_me

word=on_keyword({"你是谁"},rule=to_me())

@word.handle()
async def _(event: GroupMessageEvent):
    await word.finish(MessageSegment.at(event.user_id))
```

