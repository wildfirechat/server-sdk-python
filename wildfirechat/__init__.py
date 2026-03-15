"""
野火IM Server SDK for Python

提供与野火IM服务器交互的完整功能，包括：
- 用户管理
- 群组管理
- 消息管理
- 好友关系管理
- 聊天室管理
- 频道管理
- 机器人功能
"""

__version__ = "1.0.0"

from .admin_config import AdminConfig
from .models import IMResult, ErrorCode
from .user_admin import UserAdmin
from .group_admin import GroupAdmin
from .message_admin import MessageAdmin
from .relation_admin import RelationAdmin
from .chatroom_admin import ChatroomAdmin
from .channel_admin import ChannelAdmin
from .channel_service_api import ChannelServiceApi
from .general_admin import GeneralAdmin
from .sensitive_admin import SensitiveAdmin
from .conference_admin import ConferenceAdmin
from .moments_admin import MomentsAdmin
from .robot_service import RobotService

__all__ = [
    "AdminConfig",
    "IMResult",
    "ErrorCode",
    "UserAdmin",
    "GroupAdmin",
    "MessageAdmin",
    "RelationAdmin",
    "ChatroomAdmin",
    "ChannelAdmin",
    "ChannelServiceApi",
    "GeneralAdmin",
    "SensitiveAdmin",
    "ConferenceAdmin",
    "MomentsAdmin",
    "RobotService",
]
