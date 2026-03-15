"""
聊天室管理类
对应Java SDK中的 cn.wildfirechat.sdk.ChatroomAdmin
"""
from .api_path import APIPath
from .http_utils import AdminHttpUtils
from .models import (
    IMResult, OutputCreateChatroom, OutputGetChatroomInfo, OutputStringList,
    OutputUserChatroom, OutputChatroomBlackInfos, InputChatroomId,
    InputCreateChatroom, InputChatroomMute, InputSetChatroomBlacklist,
    InputSetChatroomManager, InputUserId
)


class ChatroomAdmin:
    """聊天室管理类"""
    
    @staticmethod
    def create_chatroom(chatroom_id: str, title: str, desc: str = "",
                        portrait: str = "", extra: str = "", state: int = 0) -> IMResult:
        """
        创建聊天室
        
        :param chatroom_id: 聊天室ID
        :param title: 聊天室标题
        :param desc: 聊天室描述
        :param portrait: 聊天室头像
        :param extra: 额外信息
        :param state: 聊天室状态
        :return: 创建结果
        """
        chatroom_data = InputCreateChatroom(
            chatroomId=chatroom_id,
            title=title,
            desc=desc,
            portrait=portrait,
            extra=extra,
            state=state
        )
        return AdminHttpUtils.http_json_post(APIPath.Create_Chatroom, chatroom_data, OutputCreateChatroom)
    
    @staticmethod
    def get_chatroom_info(chatroom_id: str) -> IMResult:
        """
        获取聊天室信息
        
        :param chatroom_id: 聊天室ID
        :return: 聊天室信息
        """
        input_data = InputChatroomId(chatroomId=chatroom_id)
        return AdminHttpUtils.http_json_post(APIPath.Chatroom_Info, input_data, OutputGetChatroomInfo)
    
    @staticmethod
    def get_chatroom_members(chatroom_id: str) -> IMResult:
        """
        获取聊天室成员列表
        
        :param chatroom_id: 聊天室ID
        :return: 聊天室成员列表
        """
        input_data = InputChatroomId(chatroomId=chatroom_id)
        return AdminHttpUtils.http_json_post(APIPath.Chatroom_GetMembers, input_data, OutputStringList)
    
    @staticmethod
    def destroy_chatroom(chatroom_id: str) -> IMResult:
        """
        销毁聊天室
        
        :param chatroom_id: 聊天室ID
        :return: 销毁结果
        """
        input_data = InputChatroomId(chatroomId=chatroom_id)
        return AdminHttpUtils.http_json_post(APIPath.Chatroom_Destroy, input_data, type(None))
    
    @staticmethod
    def get_user_chatroom(user_id: str) -> IMResult:
        """
        获取用户的聊天室
        
        :param user_id: 用户ID
        :return: 用户聊天室信息
        """
        input_data = InputUserId(userId=user_id)
        return AdminHttpUtils.http_json_post(APIPath.Chatroom_GetUserChatroom, input_data, OutputUserChatroom)
    
    @staticmethod
    def set_chatroom_mute(chatroom_id: str, mute: bool) -> IMResult:
        """
        设置聊天室全局禁言
        
        :param chatroom_id: 聊天室ID
        :param mute: 是否禁言
        :return: 设置结果
        """
        input_data = InputChatroomMute(chatroomId=chatroom_id, mute=mute)
        return AdminHttpUtils.http_json_post(APIPath.Chatroom_MuteAll, input_data, type(None))
    
    @staticmethod
    def set_chatroom_blacklist(chatroom_id: str, user_id: str, status: int) -> IMResult:
        """
        设置用户聊天室黑名单
        
        :param chatroom_id: 聊天室ID
        :param user_id: 用户ID
        :param status: 0正常；1禁言；2禁止加入
        :return: 设置结果
        """
        input_data = InputSetChatroomBlacklist(
            chatroomId=chatroom_id,
            userId=user_id,
            status=status
        )
        return AdminHttpUtils.http_json_post(APIPath.Chatroom_SetBlacklist, input_data, type(None))
    
    @staticmethod
    def get_chatroom_blacklist(chatroom_id: str) -> IMResult:
        """
        获取聊天室黑名单
        
        :param chatroom_id: 聊天室ID
        :return: 聊天室黑名单信息
        """
        input_data = InputChatroomId(chatroomId=chatroom_id)
        return AdminHttpUtils.http_json_post(APIPath.Chatroom_GetBlacklist, input_data, OutputChatroomBlackInfos)
    
    @staticmethod
    def set_chatroom_manager(chatroom_id: str, user_id: str, status: int) -> IMResult:
        """
        设置聊天室管理员
        
        :param chatroom_id: 聊天室ID
        :param user_id: 用户ID
        :param status: 0取消；1设置
        :return: 设置结果
        """
        input_data = InputSetChatroomManager(
            chatroomId=chatroom_id,
            userId=user_id,
            status=status
        )
        return AdminHttpUtils.http_json_post(APIPath.Chatroom_SetManager, input_data, type(None))
    
    @staticmethod
    def get_chatroom_manager_list(chatroom_id: str) -> IMResult:
        """
        获取聊天室管理员列表
        
        :param chatroom_id: 聊天室ID
        :return: 管理员列表
        """
        input_data = InputChatroomId(chatroomId=chatroom_id)
        return AdminHttpUtils.http_json_post(APIPath.Chatroom_GetManagerList, input_data, OutputStringList)
