"""
频道服务类
对应Java SDK中的 cn.wildfirechat.sdk.ChannelServiceApi

提供频道相关的功能，包括：
- 获取用户信息
- 修改频道信息
- 发送和撤回消息
- 用户订阅管理
- 订阅者列表查询

注意：仅专业版支持，社区版不支持
"""
import hashlib
import random
import time
from typing import List
from .api_path import APIPath
from .http_utils import ChannelHttpUtils
from .models import (
    IMResult, InputOutputUserInfo, OutputGetChannelInfo, SendMessageResult,
    InputGetUserInfo, InputModifyChannelInfo, SendChannelMessageData,
    RecallMessageData, InputChannelSubscribe, OutputStringList,
    OutputApplicationUserInfo, InputApplicationGetUserInfo, InputUserId,
    PojoChannelMenu
)
from .proto_constants import ApplicationType, ModifyChannelInfoType


class ChannelServiceApi:
    """频道服务类"""
    
    def __init__(self, im_url: str, channel_id: str, secret: str):
        """
        创建频道服务实例
        
        :param im_url: IM服务器地址，例如 http://localhost
        :param channel_id: 频道ID
        :param secret: 频道密钥
        """
        # Java SDK 中对所有字符串参数调用 trim()
        self.im_url = im_url.strip().rstrip('/')
        self.channel_id = channel_id.strip()
        self.secret = secret.strip()
    
    def _get_auth_headers(self) -> dict:
        """获取认证头"""
        # Java SDK: (int)(Math.random() * 100000 + 3)
        nonce = str(random.randint(3, 100002))
        # Java SDK使用毫秒时间戳 (System.currentTimeMillis())
        timestamp = str(int(time.time() * 1000))
        sign_str = f"{nonce}|{self.secret}|{timestamp}"
        sign = hashlib.sha1(sign_str.encode('utf-8')).hexdigest()
        
        return {
            "cid": self.channel_id,
            "nonce": nonce,
            "timestamp": timestamp,
            "sign": sign
        }
    
    def get_user_info(self, user_id: str) -> IMResult:
        """
        获取用户信息
        
        :param user_id: 用户ID
        :return: 用户信息
        """
        url = f"{self.im_url}{APIPath.Channel_User_Info}"
        headers = self._get_auth_headers()
        input_data = InputGetUserInfo(userId=user_id)
        return ChannelHttpUtils.http_json_post(url, input_data, headers, InputOutputUserInfo)
    
    def get_user_info_by_name(self, user_name: str) -> IMResult:
        """
        通过用户名获取用户信息
        
        :param user_name: 用户名
        :return: 用户信息
        """
        url = f"{self.im_url}{APIPath.Channel_User_Info}"
        headers = self._get_auth_headers()
        input_data = InputGetUserInfo(name=user_name)
        return ChannelHttpUtils.http_json_post(url, input_data, headers, InputOutputUserInfo)
    
    def get_user_info_by_mobile(self, mobile: str) -> IMResult:
        """
        通过手机号获取用户信息
        
        :param mobile: 手机号
        :return: 用户信息
        """
        url = f"{self.im_url}{APIPath.Channel_User_Info}"
        headers = self._get_auth_headers()
        input_data = InputGetUserInfo(mobile=mobile)
        return ChannelHttpUtils.http_json_post(url, input_data, headers, InputOutputUserInfo)
    
    def modify_channel_info(self, modify_type: int, value: str) -> IMResult:
        """
        修改频道信息
        
        :param modify_type: 修改类型（ModifyChannelInfoType）
        :param value: 新值
        :return: 修改结果
        """
        url = f"{self.im_url}{APIPath.Channel_Update_Profile}"
        headers = self._get_auth_headers()
        input_data = InputModifyChannelInfo(type=modify_type, value=value)
        return ChannelHttpUtils.http_json_post(url, input_data, headers, type(None))
    
    def modify_channel_menu(self, menus: List[PojoChannelMenu]) -> IMResult:
        """
        修改频道菜单
        
        :param menus: 菜单列表
        :return: 修改结果
        """
        import json
        menu_str = json.dumps([m.to_dict() for m in menus], ensure_ascii=False)
        return self.modify_channel_info(ModifyChannelInfoType.Modify_Channel_Menu, menu_str)
    
    def get_channel_info(self) -> IMResult:
        """
        获取频道信息
        
        :return: 频道信息
        """
        url = f"{self.im_url}{APIPath.Channel_Get_Profile}"
        headers = self._get_auth_headers()
        return ChannelHttpUtils.http_json_post(url, None, headers, OutputGetChannelInfo)
    
    def send_message(self, line: int, targets: List[str], payload: dict) -> IMResult:
        """
        发送消息
        
        :param line: 线路
        :param targets: 目标用户列表
        :param payload: 消息内容
        :return: 发送结果
        """
        url = f"{self.im_url}{APIPath.Channel_Message_Send}"
        headers = self._get_auth_headers()
        input_data = {
            "line": line,
            "targets": targets,
            "payload": payload
        }
        return ChannelHttpUtils.http_json_post(url, input_data, headers, SendMessageResult)
    
    def recall_message(self, message_uid: int) -> IMResult:
        """
        撤回消息
        
        :param message_uid: 消息UID
        :return: 撤回结果
        """
        url = f"{self.im_url}{APIPath.Channel_Msg_Recall}"
        headers = self._get_auth_headers()
        input_data = RecallMessageData(messageUid=message_uid)
        return ChannelHttpUtils.http_json_post(url, input_data, headers, str)
    
    def republish_message(self, message_uid: int, targets: List[str]) -> IMResult:
        """
        重新发布消息
        
        :param message_uid: 消息UID
        :param targets: 目标用户列表
        :return: 重新发布结果
        """
        url = f"{self.im_url}{APIPath.Channel_Msg_Republish}"
        headers = self._get_auth_headers()
        input_data = {
            "messageId": message_uid,
            "targets": targets
        }
        return ChannelHttpUtils.http_json_post(url, input_data, headers)
    
    def subscribe(self, user_id: str) -> IMResult:
        """
        订阅用户
        
        :param user_id: 用户ID
        :return: 订阅结果
        """
        url = f"{self.im_url}{APIPath.Channel_Subscribe}"
        headers = self._get_auth_headers()
        input_data = InputChannelSubscribe(target=user_id, subscribe=1)
        return ChannelHttpUtils.http_json_post(url, input_data, headers)
    
    def unsubscribe(self, user_id: str) -> IMResult:
        """
        取消订阅用户
        
        :param user_id: 用户ID
        :return: 取消订阅结果
        """
        url = f"{self.im_url}{APIPath.Channel_Subscribe}"
        headers = self._get_auth_headers()
        input_data = InputChannelSubscribe(target=user_id, subscribe=0)
        return ChannelHttpUtils.http_json_post(url, input_data, headers)
    
    def get_subscriber_list(self) -> IMResult:
        """
        获取订阅者列表
        
        :return: 订阅者列表
        """
        url = f"{self.im_url}{APIPath.Channel_Subscriber_List}"
        headers = self._get_auth_headers()
        return ChannelHttpUtils.http_json_post(url, None, headers, OutputStringList)
    
    def is_subscriber(self, user_id: str) -> IMResult:
        """
        检查用户是否是订阅者
        
        :param user_id: 用户ID
        :return: 是否订阅
        """
        url = f"{self.im_url}{APIPath.Channel_Is_Subscriber}"
        headers = self._get_auth_headers()
        input_data = InputUserId(userId=user_id)
        return ChannelHttpUtils.http_json_post(url, input_data, headers, bool)
    
    def application_get_user_info(self, auth_code: str) -> IMResult:
        """
        通过授权码获取用户信息
        
        :param auth_code: 授权码
        :return: 用户信息
        """
        url = f"{self.im_url}{APIPath.Channel_Application_Get_UserInfo}"
        headers = self._get_auth_headers()
        input_data = InputApplicationGetUserInfo(authCode=auth_code)
        return ChannelHttpUtils.http_json_post(url, input_data, headers, OutputApplicationUserInfo)
    
    def get_application_signature(self) -> 'OutputApplicationConfigData':
        """
        获取应用签名
        
        :return: 应用签名配置
        """
        from .models import OutputApplicationConfigData
        # Java SDK: (int)(Math.random() * 100000 + 3), System.currentTimeMillis()/1000
        nonce = random.randint(3, 100002)
        timestamp = int(time.time())  # 秒级时间戳
        sign_str = f"{nonce}|{self.channel_id}|{timestamp}|{self.secret}"
        sign = hashlib.sha1(sign_str.encode('utf-8')).hexdigest()
        
        config = OutputApplicationConfigData()
        config.appId = self.channel_id
        config.appType = ApplicationType.ApplicationType_Channel
        config.timestamp = timestamp
        config.nonceStr = str(nonce)
        config.signature = sign
        return config
