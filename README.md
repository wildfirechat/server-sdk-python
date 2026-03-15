# 野火IM Server SDK for Python

这是野火IM服务器的Python SDK，实现了与Java SDK完全相同的API接口。

## 功能特性

- 用户管理（创建、查询、更新、封禁等）
- 群组管理（创建、解散、成员管理等）
- 消息管理（发送、撤回、广播等）
- 好友关系管理（添加、删除、黑名单等）
- 聊天室管理
- 频道管理
- 机器人服务
- 会议管理
- 敏感词管理
- 多种消息类型支持（文本、图片、语音、视频、文件、位置、链接、名片等）

## 接口文档

- [Admin API 文档](https://docs.wildfirechat.cn/server/admin_api/) - 服务端管理接口，包括用户、群组、消息、频道等管理功能
- [Robot API 文档](https://docs.wildfirechat.cn/server/robot_api/) - 机器人服务接口，用于开发机器人应用
- [Channel API 文档](https://docs.wildfirechat.cn/server/channel_api/) - 频道服务接口，用于开发公众号/频道应用

## 其他语言 SDK

野火IM 官方提供多语言 SDK 实现：

| 语言 | GitHub                                                           | Gitee(码云) |
|------|------------------------------------------------------------------|-------------|
| Java SDK | [GitHub](https://github.com/wildfirechat/server/tree/master/sdk) | [Gitee](https://gitee.com/wfchat/im-server/tree/wildfirechat/sdk) |
| Go SDK | [GitHub](https://github.com/wildfirechat/server-sdk-go)          | [Gitee](https://gitee.com/wfchat/server-sdk-go) |
| Node.js SDK | [GitHub](https://github.com/wildfirechat/server-sdk.js)          | [Gitee](https://gitee.com/wfchat/server-sdk.js) |

## 安装

```bash
pip install -r requirements.txt
```

## 快速开始

```python
from wildfirechat import AdminConfig, UserAdmin, MessageAdmin
from wildfirechat.models import InputOutputUserInfo, Conversation
from wildfirechat.message_content import TextMessageContent
from wildfirechat.proto_constants import Platform

# 初始化配置
AdminConfig.init_admin("http://localhost:18080", "123456")

# 创建用户
user = InputOutputUserInfo()
user.userId = "user1"
user.name = "user1"
user.displayName = "Test User"
user.mobile = "13800000000"

result = UserAdmin.create_user(user)
if result.is_success():
    print(f"创建用户成功: {result.result.userId}")

# 获取用户Token
token_result = UserAdmin.get_user_token("user1", "client1", Platform.Platform_Android)
if token_result.is_success():
    print(f"Token: {token_result.result.token}")

# 发送消息
conversation = Conversation()
conversation.type = 0  # 私聊
conversation.target = "user2"
conversation.line = 0

text_content = TextMessageContent("Hello, World!")
payload = text_content.encode()

msg_result = MessageAdmin.send_message("user1", conversation, payload)
if msg_result.is_success():
    print(f"消息发送成功，消息ID: {msg_result.result.messageUid}")
```

### Robot 机器人服务

```python
from wildfirechat import RobotService
from wildfirechat.message_content import TextMessageContent

# 初始化机器人服务（使用机器人ID和密钥）
robot = RobotService("http://localhost", "robot1", "123456")

# 发送文本消息
content = TextMessageContent("Hello from robot!")
result = robot.send_message("user1", content)
if result.is_success():
    print("机器人消息发送成功")

# 获取用户信息
user_info = robot.get_user_info("user1")
if user_info.is_success():
    print(f"用户显示名: {user_info.result.display_name}")
```

### Channel 频道服务

```python
from wildfirechat import ChannelService
from wildfirechat.message_content import TextMessageContent

# 初始化频道服务（使用频道ID和密钥）
channel = ChannelService("http://localhost", "channel1", "123456")

# 发送消息给订阅用户
content = TextMessageContent("Channel broadcast message")
result = channel.broadcast_message(content)
if result.is_success():
    print("频道广播消息发送成功")

# 获取频道订阅者列表（专业版功能）
subscribers = channel.get_subscribers()
if subscribers.is_success():
    print(f"订阅者数量: {len(subscribers.result.subscribers)}")
```

## 运行测试

```bash
# 使用默认配置
python main.py

# 使用自定义配置
python main.py http://your-server:18080 your-secret http://your-server false false

# 显示帮助
python main.py --help
```

## 项目结构

```
python_sdk/
├── wildfirechat/           # SDK主模块
│   ├── __init__.py        # 模块导出
│   ├── admin_config.py    # 配置类
│   ├── api_path.py        # API路径定义
│   ├── error_code.py      # 错误码定义
│   ├── proto_constants.py # 协议常量
│   ├── http_utils.py      # HTTP工具类
│   ├── models.py          # 数据模型
│   ├── message_content.py # 消息内容类
│   ├── user_admin.py      # 用户管理
│   ├── group_admin.py     # 群组管理
│   ├── message_admin.py   # 消息管理
│   ├── relation_admin.py  # 好友关系管理
│   ├── chatroom_admin.py  # 聊天室管理
│   ├── channel_admin.py   # 频道管理
│   ├── general_admin.py   # 通用管理
│   ├── sensitive_admin.py # 敏感词管理
│   ├── conference_admin.py# 会议管理
│   └── robot_service.py   # 机器人服务
├── main.py                # 测试主程序
├── requirements.txt       # 依赖包
└── README.md             # 说明文档
```

## 与Java SDK的对应关系

| Java SDK | Python SDK |
|----------|------------|
| cn.wildfirechat.sdk.AdminConfig | wildfirechat.AdminConfig |
| cn.wildfirechat.sdk.UserAdmin | wildfirechat.UserAdmin |
| cn.wildfirechat.sdk.GroupAdmin | wildfirechat.GroupAdmin |
| cn.wildfirechat.sdk.MessageAdmin | wildfirechat.MessageAdmin |
| cn.wildfirechat.sdk.RelationAdmin | wildfirechat.RelationAdmin |
| cn.wildfirechat.sdk.ChatroomAdmin | wildfirechat.ChatroomAdmin |
| cn.wildfirechat.sdk.ChannelAdmin | wildfirechat.ChannelAdmin |
| cn.wildfirechat.sdk.GeneralAdmin | wildfirechat.GeneralAdmin |
| cn.wildfirechat.sdk.SensitiveAdmin | wildfirechat.SensitiveAdmin |
| cn.wildfirechat.sdk.ConferenceAdmin | wildfirechat.ConferenceAdmin |
| cn.wildfirechat.sdk.RobotService | wildfirechat.RobotService |
| cn.wildfirechat.common.ErrorCode | wildfirechat.error_code.ErrorCode |
| cn.wildfirechat.proto.ProtoConstants | wildfirechat.proto_constants |

## 许可证

本项目采用与野火IM相同的许可证。
