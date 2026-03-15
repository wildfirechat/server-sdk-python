"""
好友关系管理类
对应Java SDK中的 cn.wildfirechat.sdk.RelationAdmin
"""
from .api_path import APIPath
from .http_utils import AdminHttpUtils
from .models import (
    IMResult, OutputStringList, RelationPojo, OutputGetAlias,
    InputUpdateFriendStatusRequest, InputBlacklistRequest, InputUserId,
    InputUpdateAlias, InputGetAlias, InputUpdateFriendExtra, InputAddFriendRequest,
    StringPairPojo
)


class RelationAdmin:
    """好友关系管理类"""
    
    @staticmethod
    def set_user_friend(user_id: str, target_id: str, is_friend: bool, extra: str = None) -> IMResult:
        """
        设置用户好友关系
        
        :param user_id: 用户ID
        :param target_id: 目标用户ID
        :param is_friend: true-设置为好友，false-删除好友
        :param extra: 额外信息
        :return: 设置结果
        """
        path = APIPath.Friend_Update_Status
        input_data = InputUpdateFriendStatusRequest(
            userId=user_id,
            friendUid=target_id,
            status=0 if is_friend else 1,  # 历史遗留问题，在IM数据库中0是好友，1是好友被删除
            extra=extra if extra else ""
        )
        return AdminHttpUtils.http_json_post(path, input_data, type(None))
    
    @staticmethod
    def get_friend_list(user_id: str) -> IMResult:
        """
        获取好友列表
        
        :param user_id: 用户ID
        :return: 好友ID列表
        """
        path = APIPath.Friend_Get_List
        input_data = InputUserId(userId=user_id)
        return AdminHttpUtils.http_json_post(path, input_data, OutputStringList)
    
    @staticmethod
    def set_user_blacklist(user_id: str, target_id: str, is_blacklist: bool) -> IMResult:
        """
        设置黑名单
        
        :param user_id: 用户ID
        :param target_id: 目标用户ID
        :param is_blacklist: true-加入黑名单，false-移出黑名单
        :return: 设置结果
        """
        path = APIPath.Blacklist_Update_Status
        input_data = InputBlacklistRequest(
            userId=user_id,
            targetUid=target_id,
            status=2 if is_blacklist else 1
        )
        return AdminHttpUtils.http_json_post(path, input_data, type(None))
    
    @staticmethod
    def get_user_blacklist(user_id: str) -> IMResult:
        """
        获取用户黑名单
        
        :param user_id: 用户ID
        :return: 黑名单用户ID列表
        """
        path = APIPath.Blacklist_Get_List
        input_data = InputUserId(userId=user_id)
        return AdminHttpUtils.http_json_post(path, input_data, OutputStringList)
    
    @staticmethod
    def update_friend_alias(operator: str, target_id: str, alias: str) -> IMResult:
        """
        更新好友别名
        
        :param operator: 操作者用户ID
        :param target_id: 目标用户ID
        :param alias: 别名
        :return: 更新结果
        """
        path = APIPath.Friend_Set_Alias
        input_data = InputUpdateAlias(
            operator=operator,
            targetId=target_id,
            alias=alias
        )
        return AdminHttpUtils.http_json_post(path, input_data, type(None))
    
    @staticmethod
    def get_friend_alias(operator: str, target_id: str) -> IMResult:
        """
        获取好友别名
        
        :param operator: 操作者用户ID
        :param target_id: 目标用户ID
        :return: 好友别名
        """
        path = APIPath.Friend_Get_Alias
        input_data = InputGetAlias(
            operator=operator,
            targetId=target_id
        )
        return AdminHttpUtils.http_json_post(path, input_data, OutputGetAlias)
    
    @staticmethod
    def update_friend_extra(operator: str, target_id: str, extra: str) -> IMResult:
        """
        更新好友额外信息
        
        :param operator: 操作者用户ID
        :param target_id: 目标用户ID
        :param extra: 额外信息
        :return: 更新结果
        """
        path = APIPath.Friend_Set_Extra
        input_data = InputUpdateFriendExtra(
            operator=operator,
            targetId=target_id,
            extra=extra
        )
        return AdminHttpUtils.http_json_post(path, input_data, type(None))
    
    @staticmethod
    def send_friend_request(user_id: str, target_id: str, reason: str, force: bool = False) -> IMResult:
        """
        发送好友请求
        
        :param user_id: 用户ID
        :param target_id: 目标用户ID
        :param reason: 申请理由
        :param force: 是否强制添加（直接成为好友无需对方同意）
        :return: 发送结果
        """
        path = APIPath.Friend_Send_Request
        input_data = InputAddFriendRequest(
            userId=user_id,
            friendUid=target_id,
            reason=reason,
            force=force
        )
        return AdminHttpUtils.http_json_post(path, input_data, type(None))
    
    @staticmethod
    def get_relation(user_id: str, target_id: str) -> IMResult:
        """
        获取两个用户之间的关系
        
        :param user_id: 用户1的ID
        :param target_id: 用户2的ID
        :return: 关系信息
        """
        path = APIPath.Relation_Get
        input_data = StringPairPojo(first=user_id, second=target_id)
        return AdminHttpUtils.http_json_post(path, input_data, RelationPojo)
