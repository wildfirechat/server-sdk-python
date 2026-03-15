"""
协议常量定义
对应Java SDK中的 cn.wildfirechat.proto.ProtoConstants
"""


class ConversationType:
    """会话类型"""
    ConversationType_Private = 0
    ConversationType_Group = 1
    ConversationType_ChatRoom = 2
    ConversationType_Channel = 3
    ConversationType_Things = 4
    ConversationType_SecretChat = 5


class GroupType:
    """群组类型"""
    GroupType_Normal = 0
    GroupType_Free = 1
    GroupType_Restricted = 2
    GroupType_Organization = 3


class GroupMemberType:
    """群组成员类型"""
    GroupMemberType_Normal = 0
    GroupMemberType_Manager = 1
    GroupMemberType_Owner = 2
    GroupMemberType_Silent = 3
    GroupMemberType_Removed = 4
    GroupMemberType_Allowed = 5


class FriendRequestStatus:
    """好友请求状态"""
    RequestStatus_Sent = 0
    RequestStatus_Accepted = 1
    RequestStatus_Rejected = 2


class Platform:
    """平台类型"""
    Platform_UNSET = 0
    Platform_iOS = 1
    Platform_Android = 2
    Platform_Windows = 3
    Platform_OSX = 4
    Platform_WEB = 5
    Platform_WX = 6
    Platform_LINUX = 7
    Platform_iPad = 8
    Platform_APad = 9
    Platform_Harmony = 10
    Platform_HarmonyPad = 11
    Platform_HarmonyPC = 12
    Platform_AndroidWearable = 13
    Platform_HarmonyWearable = 14
    Platform_AndroidTV = 15
    Platform_AppleTV = 16
    Platform_HarmonyTV = 17
    Platform_MAX = Platform_HarmonyTV


class PullType:
    """拉取类型"""
    Pull_Normal = 0
    Pull_ChatRoom = 1
    Pull_Group = 2


class UserResultCode:
    """用户结果码"""
    Success = 0
    NotFound = 1
    NotModified = 2


class ChatroomState:
    """聊天室状态"""
    Chatroom_State_Normal = 0
    Chatroom_State_NotStart = 1
    Chatroom_State_End = 2


class ContentType:
    """消息内容类型"""
    Unknown = 0
    Text = 1
    Voice = 2
    Image = 3
    Location = 4
    File = 5
    Video = 6
    Sticker = 7
    Link = 8
    P_TEXT = 9
    Name_Card = 10
    Composited = 11
    Rich_Notification = 12
    Articles = 13
    StreamingText_Generationg = 14
    StreamingText_Generated = 15
    Not_Delivered = 16
    Ptt_Voice = 23
    Enter_Channel_Chat = 71
    Leave_Channel_Chat = 72
    Recall = 80
    Delete = 81
    Tip = 90
    Typing = 91
    Friend_Greeting = 92
    Friend_Added = 93
    PC_Login_Request = 94
    Create_Group = 104
    Add_Group_Member = 105
    Kickoff_Group_Member = 106
    Quit_Group = 107
    Dismiss_Group = 108
    Transfer_Group_Owner = 109
    Change_Group_Name = 110
    Modify_Group_Alias = 111
    Change_Group_Portrait = 112
    Change_Group_Mute = 113
    Change_Group_JoinType = 114
    Change_Group_PrivateChat = 115
    Change_Group_Searchable = 116
    Set_Group_Manager = 117
    Mute_Group_Member = 118
    Allow_Group_Member = 119
    Kickoff_Group_Member_Visible_Notification = 120
    Quit_Group_Visible_Notification = 121
    Modify_Group_Extra = 122
    Modify_Group_Member_Extra = 123
    Call_Start = 400
    Call_Accept = 401
    Call_End = 402
    Call_Add_Participant = 406
    Call_Multi_Call_Ongoing = 416


class MessagePersistFlag:
    """消息持久化标志"""
    NOT_PERSIST = 0
    PERSIST = 1
    PERSIST_AND_COUNT = 3
    TRANSPARENT = 4


class MessageMediaType:
    """消息媒体类型"""
    GENERAL = 0
    IMAGE = 1
    VOICE = 2
    VIDEO = 3
    FILE = 4
    PORTRAIT = 5
    FAVORITE = 6
    STICKER = 7
    MOMENTS = 8


class ModifyGroupInfoType:
    """修改群组信息类型"""
    Modify_Group_Name = 0
    Modify_Group_Portrait = 1
    Modify_Group_Extra = 2
    Modify_Group_Mute = 3
    Modify_Group_JoinType = 4
    Modify_Group_PrivateChat = 5
    Modify_Group_Searchable = 6
    Modify_Group_History_Message = 7
    Modify_Group_Max_Member_Count = 8
    Modify_Group_Super_Group = 9
    Modify_Group_Type = 10


class PersistFlag:
    """持久化标志"""
    Not_Persist = 0
    Persist = 1
    Persist_And_Count = 3
    Transparent = 4


class ModifyChannelInfoType:
    """修改频道信息类型"""
    Modify_Channel_Name = 0
    Modify_Channel_Portrait = 1
    Modify_Channel_Desc = 2
    Modify_Channel_Extra = 3
    Modify_Channel_Secret = 4
    Modify_Channel_Callback = 5
    Modify_Channel_OnlyCallback = 6
    Modify_Channel_Menu = 7


class ChannelState:
    """频道状态"""
    Channel_State_Mask_FullInfo = 0x01
    Channel_State_Mask_Unsubscribed_User_Access = 0x02
    Channel_State_Mask_Active_Subscribe = 0x04
    Channel_State_Mask_Message_Unsubscribed = 0x08
    Channel_State_Mask_Private = 0x10
    Channel_State_Mask_Deleted = 0x40
    Channel_State_Mask_Global = 0x80


class UserType:
    """用户类型"""
    UserType_Normal = 0
    UserType_Robot = 1
    UserType_Device = 2
    UserType_Admin = 3
    UserType_Super_Admin = 100


class SystemSettingType:
    """系统设置类型"""
    Group_Max_Member_Count = 1
    NOT_ALLOW_USER_NAMES = 2


class SearchUserType:
    """搜索用户类型"""
    SearchUserType_General = 0
    SearchUserType_Name_Mobile = 1
    SearchUserType_Name = 2
    SearchUserType_Mobile = 3
    SearchUserType_UserId = 4
    SearchUserType_Name_Mobile_UserId = 5
    SearchUserType_Name_Mobile_DisplayName = 100


class UserSearchUserType:
    """用户搜索用户类型"""
    UserSearchUserType_ALL = 0
    UserSearchUserType_ONLY_USER = 1
    UserSearchUserType_ONLY_ROBOT = 2


class DisableSearchMask:
    """禁用搜索掩码"""
    DisableSearchDisplayNameMask = 1
    DisableSearchNameMask = 2
    DisableSearchMobileMask = 4
    DisableSearchUserIdMask = 8


class UserStatus:
    """用户状态"""
    Normal = 0
    Muted = 1
    Forbidden = 2


class BlacklistStrategy:
    """黑名单策略"""
    Message_Reject = 0
    Message_Ignore = 1


class GroupUpdateEventType:
    """群组更新事件类型"""
    Group_Event_Create = 0
    Group_Event_Update = 1
    Group_Event_Transfer = 2
    Group_Event_Mute = 3
    Group_Event_Unmute = 4
    Group_Event_Destroy = 5


class GroupMemberUpdateEventType:
    """群组成员更新事件类型"""
    Group_Member_Event_Join = 0
    Group_Member_Event_Leave = 1
    Group_Member_Event_Kickoff = 2
    Group_Member_Event_Type_Update = 3
    Group_Member_Event_Alias = 4
    Group_Member_Event_Extra = 5


class ChannelUpdateEventType:
    """频道更新事件类型"""
    Channel_Event_Create = 0
    Channel_Event_Update = 1
    Channel_Event_Transfer = 2
    Channel_Event_Destroy = 3


class ChatroomUpdateEventType:
    """聊天室更新事件类型"""
    Chatroom_Event_Create = 0
    Chatroom_Event_Destroy = 1


class ChatroomMemberUpdateEventType:
    """聊天室成员更新事件类型"""
    Chatroom_Member_Event_Join = 0
    Chatroom_Member_Event_Leave = 1
    Chatroom_Member_Event_Kickoff = 2
    Chatroom_Member_Event_Mute = 3
    Chatroom_Member_Event_Unmute = 4


class UpdateUserInfoMask:
    """更新用户信息掩码"""
    Update_User_DisplayName = 0x01
    Update_User_Portrait = 0x02
    Update_User_Gender = 0x04
    Update_User_Mobile = 0x08
    Update_User_Email = 0x10
    Update_User_Address = 0x20
    Update_User_Company = 0x40
    Update_User_Social = 0x80
    Update_User_Extra = 0x100
    Update_User_Name = 0x200


class RequestSourceType:
    """请求来源类型"""
    Request_From_User = 0
    Request_From_Admin = 1
    Request_From_Robot = 2
    Request_From_Channel = 3


class ApplicationType:
    """应用类型"""
    ApplicationType_Robot = 0
    ApplicationType_Channel = 1
    ApplicationType_Admin = 2


class ForbiddenClientGroupOperationMask:
    """禁止客户端群组操作掩码"""
    Forbidden_Create_Group = 0x01
    Forbidden_Dismiss_Group = 0x02
    Forbidden_Join_Group = 0x04
    Forbidden_Quit_Group = 0x08
    Forbidden_Invite_Group_Member = 0x10
    Forbidden_Kickoff_Group_Member = 0x20
    Forbidden_Transfer_Group = 0x40
    Forbidden_Set_Group_Manage = 0x80
    Forbidden_Allow_Group_Member = 0x100
    Forbidden_Mute_Group = 0x200
    Forbidden_Modify_Group_Info = 0x400
    Forbidden_Mute_Group_Member = 0x800


class MomentsContentType:
    """朋友圈内容类型"""
    Moments_Content_Text_Type = 0
    Moments_Content_Image_Type = 1
    Moments_Content_Video_Type = 2
    Moments_Content_Link_Type = 3


class MomentsCommentType:
    """朋友圈评论类型"""
    Moments_Comment_Text_Type = 0
    Moments_Comment_Thumbup_Type = 1


class MomentsVisibleScope:
    """朋友圈可见范围"""
    Moments_VisibleScope_NoLimit = 0
    Moments_VisibleScope_3Days = 1
    Moments_VisibleScope_1Month = 2
    Moments_VisibleScope_6Months = 3


# 消息内容类型常量
MESSAGE_CONTENT_TYPE_CREATE_GROUP = 104
MESSAGE_CONTENT_TYPE_ADD_GROUP_MEMBER = 105
MESSAGE_CONTENT_TYPE_KICKOF_GROUP_MEMBER = 106
MESSAGE_CONTENT_TYPE_QUIT_GROUP = 107
MESSAGE_CONTENT_TYPE_DISMISS_GROUP = 108
MESSAGE_CONTENT_TYPE_TRANSFER_GROUP_OWNER = 109
MESSAGE_CONTENT_TYPE_CHANGE_GROUP_NAME = 110
MESSAGE_CONTENT_TYPE_MODIFY_GROUP_ALIAS = 111
MESSAGE_CONTENT_TYPE_CHANGE_GROUP_PORTRAIT = 112
MESSAGE_CONTENT_TYPE_CHANGE_MUTE = 113
MESSAGE_CONTENT_TYPE_CHANGE_JOINTYPE = 114
MESSAGE_CONTENT_TYPE_CHANGE_PRIVATECHAT = 115
MESSAGE_CONTENT_TYPE_CHANGE_SEARCHABLE = 116
MESSAGE_CONTENT_TYPE_SET_MANAGER = 117
MESSAGE_CONTENT_TYPE_MUTE_MEMBER = 118
MESSAGE_CONTENT_TYPE_ALLOW_MEMBER = 119
MESSAGE_CONTENT_TYPE_KICKOF_GROUP_MEMBER_VISIBLE = 120
MESSAGE_CONTENT_TYPE_QUIT_GROUP_VISIBLE = 121
MESSAGE_CONTENT_TYPE_MODIFY_GROUP_EXTRA = 122
MESSAGE_CONTENT_TYPE_MODIFY_GROUP_MEMBER_EXTRA = 123
MESSAGE_CONTENT_TYPE_MODIFY_GROUP_SETTINGS = 124
MESSAGE_CONTENT_TYPE_REJECT_JOIN_GROUP = 125


class MyInfoType:
    """我的信息类型"""
    Modify_DisplayName = 0
