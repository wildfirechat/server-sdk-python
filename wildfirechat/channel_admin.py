"""
频道管理类
对应Java SDK中的 cn.wildfirechat.sdk.ChannelAdmin
"""
from .api_path import APIPath
from .http_utils import AdminHttpUtils
from .models import (
    IMResult, OutputCreateChannel, OutputGetChannelInfo, OutputBooleanValue,
    InputCreateChannel, InputChannelId, InputSubscribeChannel
)


class ChannelAdmin:
    """频道管理类"""
    
    @staticmethod
    def create_channel(input_data: InputCreateChannel) -> IMResult:
        """
        创建频道
        
        :param input_data: 创建频道输入参数
        :return: 创建结果，包含频道ID
        """
        return AdminHttpUtils.http_json_post(APIPath.Create_Channel, input_data, OutputCreateChannel)
    
    @staticmethod
    def get_channel_info(channel_id: str) -> IMResult:
        """
        获取频道信息
        
        :param channel_id: 频道ID
        :return: 频道信息
        """
        input_data = InputChannelId(channelId=channel_id)
        return AdminHttpUtils.http_json_post(APIPath.Get_Channel_Info, input_data, OutputGetChannelInfo)
    
    @staticmethod
    def subscribe_channel(channel_id: str, user_id: str) -> IMResult:
        """
        订阅频道
        
        :param channel_id: 频道ID
        :param user_id: 用户ID
        :return: 订阅结果
        """
        input_data = InputSubscribeChannel(channelId=channel_id, userId=user_id, subscribe=1)
        return AdminHttpUtils.http_json_post(APIPath.Subscribe_Channel, input_data, type(None))
    
    @staticmethod
    def unsubscribe_channel(channel_id: str, user_id: str) -> IMResult:
        """
        取消订阅频道
        
        :param channel_id: 频道ID
        :param user_id: 用户ID
        :return: 取消订阅结果
        """
        input_data = InputSubscribeChannel(channelId=channel_id, userId=user_id, subscribe=0)
        return AdminHttpUtils.http_json_post(APIPath.Subscribe_Channel, input_data, type(None))
    
    @staticmethod
    def is_user_subscribed_channel(user_id: str, channel_id: str) -> IMResult:
        """
        检查用户是否关注了频道
        
        :param user_id: 用户ID
        :param channel_id: 频道ID
        :return: 是否关注
        """
        input_data = InputSubscribeChannel(channelId=channel_id, userId=user_id, subscribe=0)
        return AdminHttpUtils.http_json_post(APIPath.Check_User_Subscribe_Channel, input_data, OutputBooleanValue)
    
    @staticmethod
    def destroy_channel(channel_id: str) -> IMResult:
        """
        销毁频道
        
        :param channel_id: 频道ID
        :return: 销毁结果
        """
        input_data = InputChannelId(channelId=channel_id)
        return AdminHttpUtils.http_json_post(APIPath.Destroy_Channel, input_data, type(None))
