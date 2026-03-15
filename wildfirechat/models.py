"""
数据模型类
对应Java SDK中的POJO类
"""
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from .error_code import ErrorCode, ErrorCode as EC


@dataclass
class IMResult:
    """IM结果类"""
    code: int = 0
    msg: str = ""
    result: Any = None
    
    def get_error_code(self) -> ErrorCode:
        return ErrorCode.from_code(self.code)
    
    def is_success(self) -> bool:
        return self.code == EC.ERROR_CODE_SUCCESS.code


@dataclass
class Conversation:
    """会话类"""
    type: int = 0
    target: str = ""
    line: int = 0
    
    def to_dict(self):
        return {
            "type": self.type,
            "target": self.target,
            "line": self.line
        }


@dataclass
class MessagePayload:
    """消息内容负载类"""
    type: int = 0
    searchableContent: str = ""
    pushContent: str = ""
    pushData: str = ""
    content: str = ""
    base64edData: str = ""
    mediaType: int = 0
    remoteMediaUrl: str = ""
    persistFlag: int = 0
    expireDuration: int = 0
    mentionedType: int = 0
    mentionedTarget: List[str] = field(default_factory=list)
    extra: str = ""
    
    def to_dict(self):
        result = {
            "type": self.type,
            "searchableContent": self.searchableContent,
            "pushContent": self.pushContent,
            "pushData": self.pushData,
            "content": self.content,
            "base64edData": self.base64edData,
            "mediaType": self.mediaType,
            "remoteMediaUrl": self.remoteMediaUrl,
            "persistFlag": self.persistFlag,
            "expireDuration": self.expireDuration,
            "mentionedType": self.mentionedType,
            "mentionedTarget": self.mentionedTarget,
            "extra": self.extra
        }
        # 过滤掉空值
        return {k: v for k, v in result.items() if v or v == 0}


@dataclass
class InputOutputUserInfo:
    """用户信息类"""
    userId: str = ""
    name: str = ""
    password: str = ""
    displayName: str = ""
    portrait: str = ""
    gender: int = 0
    mobile: str = ""
    email: str = ""
    address: str = ""
    company: str = ""
    social: str = ""
    extra: str = ""
    type: int = 0
    deleted: int = 0
    updateDt: int = 0


@dataclass
class OutputCreateUser:
    """创建用户输出类"""
    userId: str = ""
    name: str = ""


@dataclass
class InputCreateRobot:
    """创建机器人输入类"""
    userId: str = ""
    name: str = ""
    displayName: str = ""
    owner: str = ""
    secret: str = ""
    callback: str = ""


@dataclass
class OutputCreateRobot:
    """创建机器人输出类"""
    userId: str = ""
    token: str = ""


@dataclass
class OutputRobot:
    """机器人信息输出类"""
    userId: str = ""
    name: str = ""
    displayName: str = ""
    owner: str = ""
    secret: str = ""
    callback: str = ""


@dataclass
class OutputUserInfoList:
    """用户信息列表输出类"""
    userInfoList: List[InputOutputUserInfo] = field(default_factory=list)


@dataclass
class OutputGetUserList:
    """获取用户列表输出类"""
    userList: List[InputOutputUserInfo] = field(default_factory=list)


@dataclass
class OutputUserStatus:
    """用户状态输出类"""
    status: int = 0


@dataclass
class OutputUserBlockStatus:
    """用户封禁状态输出类"""
    userId: str = ""
    status: int = 0


@dataclass
class OutputUserBlockStatusList:
    """用户封禁状态列表输出类"""
    statusList: List[OutputUserBlockStatus] = field(default_factory=list)


@dataclass
class OutputCheckUserOnline:
    """检查用户在线状态输出类"""
    sessions: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class OutputGetIMTokenData:
    """获取IM Token数据输出类"""
    token: str = ""
    userId: str = ""


@dataclass
class InputGetToken:
    """获取Token输入类"""
    userId: str = ""
    clientId: str = ""
    platform: int = 0


@dataclass
class InputUpdateUserInfo:
    """更新用户信息输入类"""
    flag: int = 0
    userInfo: InputOutputUserInfo = field(default_factory=InputOutputUserInfo)


@dataclass
class PojoGroupInfo:
    """群组信息类"""
    target_id: str = ""
    name: str = ""
    portrait: str = ""
    owner: str = ""
    type: int = 0
    extra: str = ""
    memberCount: int = 0
    memberUpdateDt: int = 0
    updateDt: int = 0


@dataclass
class PojoGroupMember:
    """群组成员类"""
    member_id: str = ""
    alias: str = ""
    type: int = 0
    extra: str = ""
    updateDt: int = 0


@dataclass
class PojoGroup:
    """群组类"""
    group_info: PojoGroupInfo = field(default_factory=PojoGroupInfo)
    members: List[PojoGroupMember] = field(default_factory=list)


@dataclass
class InputCreateGroup:
    """创建群组输入类"""
    group: PojoGroup = field(default_factory=PojoGroup)
    operator: str = ""
    member_extra: str = ""
    to_lines: List[int] = field(default_factory=list)
    notify_message: Optional[MessagePayload] = None


@dataclass
class OutputCreateGroupResult:
    """创建群组结果输出类"""
    groupId: str = ""


@dataclass
class PojoGroupInfoList:
    """群组信息列表类"""
    groupInfoList: List[PojoGroupInfo] = field(default_factory=list)


@dataclass
class OutputGroupMemberList:
    """群组成员列表输出类"""
    members: List[PojoGroupMember] = field(default_factory=list)


@dataclass
class OutputGroupIds:
    """群组ID列表输出类"""
    groupIds: List[str] = field(default_factory=list)


@dataclass
class SendMessageData:
    """发送消息数据类"""
    sender: str = ""
    conv: Optional[Conversation] = None
    payload: Optional[MessagePayload] = None
    toUsers: List[str] = field(default_factory=list)
    userMessage: bool = False
    
    def to_dict(self):
        result = {
            "sender": self.sender,
            "conv": self.conv.to_dict() if self.conv else None,
            "payload": self.payload.to_dict() if self.payload else None,
            "toUsers": self.toUsers,
            "userMessage": self.userMessage
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class SendMessageResult:
    """发送消息结果类"""
    messageUid: int = 0
    timestamp: int = 0


@dataclass
class RecallMessageData:
    """撤回消息数据类"""
    operator: str = ""
    messageUid: int = 0


@dataclass
class DeleteMessageData:
    """删除消息数据类"""
    messageUid: int = 0


@dataclass
class UpdateMessageContentData:
    """更新消息内容数据类"""
    operator: str = ""
    messageUid: int = 0
    payload: Optional[MessagePayload] = None
    distribute: int = 0
    updateTimestamp: int = 0


@dataclass
class BroadMessageData:
    """广播消息数据类"""
    sender: str = ""
    line: int = 0
    payload: Optional[MessagePayload] = None


@dataclass
class BroadMessageResult:
    """广播消息结果类"""
    count: int = 0
    messageUid: int = 0


@dataclass
class MulticastMessageData:
    """群发消息数据类"""
    sender: str = ""
    targets: List[str] = field(default_factory=list)
    line: int = 0
    payload: Optional[MessagePayload] = None


@dataclass
class MultiMessageResult:
    """群发消息结果类"""
    messageUid: int = 0
    timestamp: int = 0


@dataclass
class RecallMultiCastMessageData:
    """撤回群发消息数据类"""
    operator: str = ""
    messageUid: int = 0
    receivers: List[str] = field(default_factory=list)


@dataclass
class OutputMessageData:
    """消息数据输出类"""
    messageId: int = 0
    sender: str = ""
    conversation: Optional[Conversation] = None
    payload: Optional[MessagePayload] = None
    timestamp: int = 0


@dataclass
class OutputTimestamp:
    """时间戳输出类"""
    timestamp: int = 0


@dataclass
class InputClearUserMessages:
    """清除用户消息输入类"""
    userId: str = ""
    conversation: Optional[Conversation] = None
    fromTime: int = 0
    toTime: int = 0


@dataclass
class InputUserConversation:
    """用户会话输入类"""
    userId: str = ""
    conversation: Optional[Conversation] = None


@dataclass
class InputStringList:
    """字符串列表输入类"""
    list: List[str] = field(default_factory=list)


@dataclass
class OutputStringList:
    """字符串列表输出类"""
    list: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """确保list字段始终是列表"""
        if self.list is None:
            self.list = []
    
    @classmethod
    def from_list(cls, data: list):
        """从纯列表创建实例（用于处理服务器直接返回列表的情况）"""
        instance = cls(list=data if data is not None else [])
        return instance


@dataclass
class InputOutputSensitiveWords:
    """敏感词输入输出类"""
    words: List[str] = field(default_factory=list)


@dataclass
class StringPairPojo:
    """字符串对POJO类"""
    first: str = ""
    second: str = ""


@dataclass
class InputAddFriendRequest:
    """添加好友请求输入类"""
    userId: str = ""
    friendUid: str = ""
    reason: str = ""
    force: bool = False


@dataclass
class InputUpdateFriendStatusRequest:
    """更新好友状态请求输入类"""
    userId: str = ""
    friendUid: str = ""
    status: int = 0
    extra: str = ""


@dataclass
class InputBlacklistRequest:
    """黑名单请求输入类"""
    userId: str = ""
    targetUid: str = ""
    status: int = 0


@dataclass
class InputUpdateAlias:
    """更新别名输入类"""
    operator: str = ""
    targetId: str = ""
    alias: str = ""


@dataclass
class InputGetAlias:
    """获取别名输入类"""
    operator: str = ""
    targetId: str = ""


@dataclass
class OutputGetAlias:
    """获取别名输出类"""
    alias: str = ""


@dataclass
class InputUpdateFriendExtra:
    """更新好友额外信息输入类"""
    operator: str = ""
    targetId: str = ""
    extra: str = ""


@dataclass
class RelationPojo:
    """关系POJO类"""
    userId: str = ""
    targetId: str = ""
    status: int = 0
    extra: str = ""
    alias: str = ""


@dataclass
class InputGetGroup:
    """获取群组输入类"""
    groupId: str = ""


@dataclass
class InputGetGroupMember:
    """获取群组成员输入类"""
    groupId: str = ""
    memberId: str = ""


@dataclass
class InputAddGroupMember:
    """添加群组成员输入类"""
    group_id: str = ""
    members: List[PojoGroupMember] = field(default_factory=list)
    operator: str = ""
    memberExtra: str = ""
    to_lines: List[int] = field(default_factory=list)
    notify_message: Optional[MessagePayload] = None


@dataclass
class InputSetGroupManager:
    """设置群组管理员输入类"""
    group_id: str = ""
    members: List[str] = field(default_factory=list)
    is_manager: bool = False
    operator: str = ""
    to_lines: List[int] = field(default_factory=list)
    notify_message: Optional[MessagePayload] = None


@dataclass
class InputMuteGroupMember:
    """禁言群组成员输入类"""
    group_id: str = ""
    members: List[str] = field(default_factory=list)
    is_manager: bool = False
    operator: str = ""
    to_lines: List[int] = field(default_factory=list)
    notify_message: Optional[MessagePayload] = None


@dataclass
class InputKickoffGroupMember:
    """踢出群组成员输入类"""
    group_id: str = ""
    members: List[str] = field(default_factory=list)
    operator: str = ""
    to_lines: List[int] = field(default_factory=list)
    notify_message: Optional[MessagePayload] = None


@dataclass
class InputQuitGroup:
    """退出群组输入类"""
    group_id: str = ""
    operator: str = ""
    to_lines: List[int] = field(default_factory=list)
    notify_message: Optional[MessagePayload] = None


@dataclass
class InputSetGroupMemberAlias:
    """设置群组成员别名输入类"""
    group_id: str = ""
    operator: str = ""
    memberId: str = ""
    alias: str = ""
    to_lines: List[int] = field(default_factory=list)
    notify_message: Optional[MessagePayload] = None


@dataclass
class InputSetGroupMemberExtra:
    """设置群组成员额外信息输入类"""
    group_id: str = ""
    operator: str = ""
    memberId: str = ""
    extra: str = ""
    to_lines: List[int] = field(default_factory=list)
    notify_message: Optional[MessagePayload] = None


@dataclass
class InputDismissGroup:
    """解散群组输入类"""
    operator: str = ""
    group_id: str = ""
    to_lines: List[int] = field(default_factory=list)
    notify_message: Optional[MessagePayload] = None


@dataclass
class InputTransferGroup:
    """转让群组输入类"""
    operator: str = ""
    group_id: str = ""
    new_owner: str = ""
    to_lines: List[int] = field(default_factory=list)
    notify_message: Optional[MessagePayload] = None


@dataclass
class InputModifyGroupInfo:
    """修改群组信息输入类"""
    group_id: str = ""
    operator: str = ""
    type: int = 0
    value: str = ""
    to_lines: List[int] = field(default_factory=list)
    notify_message: Optional[MessagePayload] = None


@dataclass
class InputGetUserGroupByType:
    """获取用户群组按类型输入类"""
    userId: str = ""
    groupMemberTypes: List[int] = field(default_factory=list)


@dataclass
class InputUserId:
    """用户ID输入类"""
    userId: str = ""


@dataclass
class InputGetUserInfo:
    """获取用户信息输入类"""
    userId: str = ""
    name: str = ""
    mobile: str = ""
    includeDeleted: bool = False


@dataclass
class InputGetUserList:
    """获取用户列表输入类"""
    count: int = 0
    offset: int = 0


@dataclass
class InputOutputUserBlockStatus:
    """用户封禁状态输入输出类"""
    userId: str = ""
    status: int = 0


@dataclass
class InputDestroyUser:
    """销毁用户输入类"""
    userId: str = ""


@dataclass
class InputRobotId:
    """机器人ID输入类"""
    robotId: str = ""


@dataclass
class InputCreateChannel:
    """创建频道输入类"""
    owner: str = ""
    name: str = ""
    targetId: str = ""
    callback: str = ""
    portrait: str = ""
    auto: int = 0
    secret: str = ""
    desc: str = ""
    state: int = 0
    extra: str = ""
    updateDt: int = 0
    menus: List['PojoChannelMenu'] = field(default_factory=list)


@dataclass
class OutputCreateChannel:
    """创建频道输出类"""
    targetId: str = ""


@dataclass
class OutputGetChannelInfo:
    """获取频道信息输出类"""
    targetId: str = ""
    name: str = ""
    owner: str = ""
    portrait: str = ""
    state: int = 0
    extra: str = ""


@dataclass
class PojoChannelMenu:
    """频道菜单类"""
    menuId: str = ""
    type: str = ""  # view, click 等
    name: str = ""
    key: str = ""
    url: str = ""
    mediaId: str = ""
    articleId: str = ""
    appId: str = ""
    appPage: str = ""
    extra: str = ""
    subMenus: List['PojoChannelMenu'] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """转换为字典，递归处理子菜单"""
        result = {
            "menuId": self.menuId,
            "type": self.type,
            "name": self.name,
            "key": self.key,
            "url": self.url,
            "mediaId": self.mediaId,
            "articleId": self.articleId,
            "appId": self.appId,
            "appPage": self.appPage,
            "extra": self.extra,
        }
        # 递归转换子菜单
        if self.subMenus:
            result["subMenus"] = [m.to_dict() for m in self.subMenus]
        else:
            result["subMenus"] = []
        return result


@dataclass
class InputChannelId:
    """频道ID输入类"""
    channelId: str = ""


@dataclass
class InputChannelSubscribe:
    """频道订阅输入类"""
    target: str = ""
    subscribe: int = 1  # 1=订阅, 0=取消订阅


@dataclass
class InputSubscribeChannel:
    """检查频道订阅输入类"""
    channelId: str = ""
    userId: str = ""
    subscribe: int = 0


@dataclass
class InputModifyChannelInfo:
    """修改频道信息输入类"""
    type: int = 0
    value: str = ""


@dataclass
class SendChannelMessageData:
    """发送频道消息数据类"""
    line: int = 0
    targets: List[str] = field(default_factory=list)
    payload: Optional[MessagePayload] = None


@dataclass
class OutputBooleanValue:
    """布尔值输出类"""
    value: bool = False


@dataclass
class SystemSettingPojo:
    """系统设置POJO类"""
    key: int = 0
    value: str = ""
    desc: str = ""


@dataclass
class UserSettingPojo:
    """用户设置POJO类"""
    userId: str = ""
    scope: int = 0
    key: str = ""
    value: str = ""


@dataclass
class HealthCheckResult:
    """健康检查结果类"""
    status: str = ""
    version: str = ""
    uptime: int = 0
    nodeId: int = 0


@dataclass
class InputCreateChatroom:
    """创建聊天室输入类"""
    chatroomId: str = ""
    title: str = ""
    desc: str = ""
    portrait: str = ""
    extra: str = ""
    state: int = 0


@dataclass
class OutputCreateChatroom:
    """创建聊天室输出类"""
    chatroomId: str = ""


@dataclass
class OutputGetChatroomInfo:
    """获取聊天室信息输出类"""
    chatroomId: str = ""
    title: str = ""
    desc: str = ""
    portrait: str = ""
    extra: str = ""
    state: int = 0


@dataclass
class InputChatroomId:
    """聊天室ID输入类"""
    chatroomId: str = ""


@dataclass
class InputChatroomMute:
    """聊天室禁言输入类"""
    chatroomId: str = ""
    mute: bool = False


@dataclass
class OutputUserChatroom:
    """用户聊天室输出类"""
    chatroomId: str = ""


@dataclass
class InputSetChatroomBlacklist:
    """设置聊天室黑名单输入类"""
    chatroomId: str = ""
    userId: str = ""
    status: int = 0


@dataclass
class InputSetChatroomManager:
    """设置聊天室管理员输入类"""
    chatroomId: str = ""
    userId: str = ""
    status: int = 0


@dataclass
class OutputChatroomBlackInfos:
    """聊天室黑名单信息输出类"""
    @dataclass
    class OutputChatroomBlackInfo:
        userId: str = ""
        status: int = 0
    
    infos: List[OutputChatroomBlackInfo] = field(default_factory=list)


@dataclass
class InputCreateDevice:
    """创建设备输入类"""
    deviceId: str = ""
    name: str = ""
    extra: str = ""


@dataclass
class OutputCreateDevice:
    """创建设备输出类"""
    deviceId: str = ""
    token: str = ""


@dataclass
class InputDeviceId:
    """设备ID输入类"""
    deviceId: str = ""


@dataclass
class OutputDevice:
    """设备信息输出类"""
    deviceId: str = ""
    name: str = ""
    extra: str = ""


@dataclass
class OutputDeviceList:
    """设备列表输出类"""
    devices: List[OutputDevice] = field(default_factory=list)


@dataclass
class InputCountOffset:
    """计数偏移输入类"""
    count: int = 0
    offset: int = 0


@dataclass
@dataclass
class PojoConferenceInfo:
    """会议信息类"""
    roomId: str = ""  # 服务器返回的是 roomId
    description: str = ""
    max_publishers: int = 0
    advance: bool = False
    recording: bool = False
    # 兼容字段
    conferenceId: str = ""
    conferenceTitle: str = ""
    password: str = ""
    pin: str = ""
    owner: str = ""
    startTime: int = 0
    endTime: int = 0
    maxPublishers: int = 0
    bitrate: int = 0
    permanent: bool = False


@dataclass
class PojoConferenceInfoList:
    """会议信息列表类"""
    conferenceInfoList: List[PojoConferenceInfo] = field(default_factory=list)


@dataclass
class GetOnlineUserCountResult:
    """获取在线用户数量结果类"""
    count: int = 0


@dataclass
class GetOnlineUserRequest:
    """获取在线用户请求类"""
    nodeId: int = 0
    offset: int = 0
    count: int = 0


@dataclass
class OnlineUserInfo:
    """在线用户信息类"""
    userId: str = ""
    clientId: str = ""
    platform: int = 0
    nodeId: int = 0
    lastSeen: int = 0


@dataclass
class GetOnlineUserResult:
    """获取在线用户结果类"""
    users: List[OnlineUserInfo] = field(default_factory=list)


@dataclass
class GetUserSessionResult:
    """获取用户会话结果类"""
    sessions: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class InputApplicationGetUserInfo:
    """应用获取用户信息输入类"""
    authCode: str = ""


@dataclass
class OutputApplicationUserInfo:
    """应用获取用户信息输出类"""
    userId: str = ""
    name: str = ""
    displayName: str = ""


@dataclass
class InputGetConvReadTime:
    """获取会话已读时间输入类"""
    userId: str = ""
    conversationType: int = 0
    target: str = ""
    line: int = 0


@dataclass
class InputMessageUid:
    """消息UID输入类"""
    messageUid: int = 0


@dataclass
class FilesPojo:
    """文件POJO类"""
    @dataclass
    class FilePojo:
        messageId: int = 0
        userId: str = ""
        conversation: Optional[Conversation] = None
        name: str = ""
        url: str = ""
        size: int = 0
        timestamp: int = 0
    
    files: List[FilePojo] = field(default_factory=list)


@dataclass
class InputGetPresignedUploadUrl:
    """获取预签名上传URL输入类"""
    mediaType: int = 0
    fileName: str = ""
    contentType: str = ""


@dataclass
class OutputPresignedUploadUrl:
    """获取预签名上传URL输出类"""
    url: str = ""           # 上传URL
    downloadUrl: str = ""   # 下载URL
    path: str = ""          # 文件路径
    expireTime: int = 0     # 过期时间
    type: int = 0           # 存储类型：1=七牛云，其他=阿里云/Minio等


@dataclass
class RobotCallbackPojo:
    """机器人回调POJO类"""
    url: str = ""


@dataclass
class QuoteInfo:
    """引用信息类"""
    messageUid: int = 0
    userId: str = ""
    userDisplayName: str = ""
    messageDigest: str = ""
    
    def encode(self):
        return {
            "u": self.messageUid,
            "i": self.userId,
            "n": self.userDisplayName,
            "d": self.messageDigest
        }
    
    def decode(self, data):
        self.messageUid = data.get("u", 0)
        self.userId = data.get("i", "")
        self.userDisplayName = data.get("n", "")
        self.messageDigest = data.get("d", "")
        return self


# ==================== 朋友圈相关模型类 ====================

@dataclass
class MediaEntry:
    """媒体条目类"""
    mediaType: int = 0  # 1=图片, 2=视频
    mediaUrl: str = ""  # 可以是远程URL或本地路径
    width: int = 0
    height: int = 0


@dataclass
class FeedPojo:
    """朋友圈动态类"""
    feedId: int = 0
    type: int = 0  # 0=文本, 1=图片, 2=视频, 3=链接
    text: str = ""
    medias: List[MediaEntry] = field(default_factory=list)
    to: List[str] = field(default_factory=list)  # 可见用户列表
    ex: List[str] = field(default_factory=list)  # 排除用户列表
    mu: List[str] = field(default_factory=list)  # @用户列表
    extra: str = ""
    timestamp: int = 0


@dataclass
class FeedsPojo:
    """朋友圈动态列表类"""
    feeds: List[FeedPojo] = field(default_factory=list)


@dataclass
class CommentPojo:
    """朋友圈评论类"""
    commentId: int = 0
    feedId: int = 0
    replyId: int = 0  # 回复的评论ID
    type: int = 0  # 0=文本, 1=点赞
    text: str = ""
    replyTo: str = ""  # 回复给哪个用户
    extra: str = ""
    timestamp: int = 0


@dataclass
class MomentProfilePojo:
    """朋友圈资料类"""
    userId: str = ""
    backgroundUrl: str = ""
    strangerVisibleCount: int = 0
    visibleScope: int = 0  # 0=无限制, 1=3天, 2=1月, 3=6月


@dataclass
class PostFeedResult:
    """发布动态结果类"""
    id: int = 0
    timestamp: int = 0


@dataclass
class PojoConferenceParticipant:
    """会议参与者类"""
    userId: str = ""
    name: str = ""
    joinTime: int = 0
   

@dataclass
class PojoConferenceParticipantList:
    """会议参与者列表类"""
    participants: List[PojoConferenceParticipant] = field(default_factory=list)


@dataclass
class RtpStream:
    """RTP流信息类"""
    streamId: int = 0
    type: str = ""  # audio 或 video


@dataclass
class RtpForwarder:
    """RTP转发器类"""
    publisherId: str = ""
    streams: List[RtpStream] = field(default_factory=list)


@dataclass
class PojoConferenceRtpForwarders:
    """会议RTP转发器列表类"""
    roomId: str = ""
    forwarders: List[RtpForwarder] = field(default_factory=list)


@dataclass
class OutputApplicationConfigData:
    """应用签名配置数据类"""
    appId: str = ""
    appType: int = 0
    timestamp: int = 0
    nonceStr: str = ""
    signature: str = ""


@dataclass
class SendMessageResult:
    """发送消息结果类"""
    messageUid: int = 0
    timestamp: int = 0
