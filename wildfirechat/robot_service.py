"""
机器人服务类
对应Java SDK中的 cn.wildfirechat.sdk.RobotService
"""
import hashlib
import random
import time
from typing import List
from .api_path import APIPath
from .http_utils import RobotHttpUtils
from .models import (
    IMResult, OutputRobot, RobotCallbackPojo, PojoGroupInfo, PojoGroupMember,
    OutputCreateGroupResult, OutputGroupMemberList,
    PojoGroupInfoList, OutputGroupIds, OutputApplicationUserInfo, SendMessageResult
)


class RobotService:
    """机器人服务类"""
    
    def __init__(self, im_url: str, robot_id: str, robot_secret: str):
        """
        初始化机器人服务
        
        :param im_url: IM服务地址
        :param robot_id: 机器人ID
        :param robot_secret: 机器人密钥
        """
        # Java SDK 中对所有字符串参数调用 trim()
        self.im_url = im_url.strip().rstrip('/')
        self.robot_id = robot_id.strip()
        self.robot_secret = robot_secret.strip()
    
    def _generate_auth_headers(self) -> dict:
        """生成认证头"""
        # Java SDK: (int)(Math.random() * 100000 + 3)
        nonce = str(random.randint(3, 100002))
        # Java SDK: System.currentTimeMillis()
        timestamp = str(int(time.time() * 1000))
        sign_str = f"{nonce}|{self.robot_secret}|{timestamp}"
        sign = hashlib.sha1(sign_str.encode('utf-8')).hexdigest()
        
        return {
            "rid": self.robot_id,
            "nonce": nonce,
            "timestamp": timestamp,
            "sign": sign
        }
    
    def get_profile(self) -> IMResult:
        """
        获取机器人资料
        
        :return: 机器人资料
        """
        url = f"{self.im_url}{APIPath.Robot_Get_Profile}"
        headers = self._generate_auth_headers()
        return RobotHttpUtils.http_json_post(url, None, headers, OutputRobot)
    
    def update_profile(self, modify_type: int, value: str) -> IMResult:
        """
        更新机器人资料
        
        :param modify_type: 修改类型
        :param value: 新值
        :return: 更新结果
        """
        url = f"{self.im_url}{APIPath.Robot_Update_Profile}"
        headers = self._generate_auth_headers()
        data = {"intValue": modify_type, "strValue": value}
        return RobotHttpUtils.http_json_post(url, data, headers, type(None))
    
    def set_callback(self, callback_url: str) -> IMResult:
        """
        设置机器人回调地址
        
        :param callback_url: 回调地址
        :return: 设置结果
        """
        url = f"{self.im_url}{APIPath.Robot_Set_Callback}"
        headers = self._generate_auth_headers()
        data = {"url": callback_url}
        return RobotHttpUtils.http_json_post(url, data, headers, type(None))
    
    def get_callback(self) -> IMResult:
        """
        获取机器人回调地址
        
        :return: 回调地址
        """
        url = f"{self.im_url}{APIPath.Robot_Get_Callback}"
        headers = self._generate_auth_headers()
        return RobotHttpUtils.http_json_post(url, None, headers, RobotCallbackPojo)
    
    def delete_callback(self) -> IMResult:
        """
        删除机器人回调地址
        
        :return: 删除结果
        """
        url = f"{self.im_url}{APIPath.Robot_Delete_Callback}"
        headers = self._generate_auth_headers()
        return RobotHttpUtils.http_json_post(url, None, headers, type(None))
    
    def send_message(self, conversation: dict, payload: dict) -> IMResult:
        """
        发送消息
        
        :param conversation: 会话信息
        :param payload: 消息内容
        :return: 发送结果
        """
        url = f"{self.im_url}{APIPath.Robot_Message_Send}"
        headers = self._generate_auth_headers()
        data = {"conv": conversation, "payload": payload}
        return RobotHttpUtils.http_json_post(url, data, headers, SendMessageResult)
    
    def recall_message(self, message_uid: int) -> IMResult:
        """
        撤回消息
        
        :param message_uid: 消息UID
        :return: 撤回结果
        """
        url = f"{self.im_url}{APIPath.Robot_Message_Recall}"
        headers = self._generate_auth_headers()
        data = {"messageUid": message_uid}
        return RobotHttpUtils.http_json_post(url, data, headers, type(None))
    
    def update_message(self, message_uid: int, payload: dict) -> IMResult:
        """
        更新消息
        
        :param message_uid: 消息UID
        :param payload: 新的消息内容
        :return: 更新结果
        """
        url = f"{self.im_url}{APIPath.Robot_Message_Update}"
        headers = self._generate_auth_headers()
        data = {"messageUid": message_uid, "payload": payload}
        return RobotHttpUtils.http_json_post(url, data, headers, OutputApplicationUserInfo)
    
    def get_user_info(self, user_id: str) -> IMResult:
        """
        获取用户信息
        
        :param user_id: 用户ID
        :return: 用户信息
        """
        url = f"{self.im_url}{APIPath.Robot_User_Info}"
        headers = self._generate_auth_headers()
        data = {"userId": user_id}
        return RobotHttpUtils.http_json_post(url, data, headers, OutputCreateGroupResult)
    
    def create_group(self, group_info: dict, members: List[dict],
                     member_extra: str = None, to_lines: List[int] = None,
                     notify_message: dict = None) -> IMResult:
        """
        创建群组
        
        :param group_info: 群组信息 (PojoGroupInfo的dict格式)
        :param members: 成员列表 (PojoGroupMember的dict格式列表)
        :param member_extra: 成员额外信息
        :param to_lines: 消息同步到的线路列表
        :param notify_message: 通知消息
        :return: 创建结果
        """
        url = f"{self.im_url}{APIPath.Robot_Create_Group}"
        headers = self._generate_auth_headers()
        # Java后端使用下划线命名：group_info, member_id 等
        converted_members = []
        for m in members:
            converted_member = {}
            if "member_id" in m:
                converted_member["member_id"] = m["member_id"]
            if "alias" in m:
                converted_member["alias"] = m["alias"]
            if "type" in m:
                converted_member["type"] = m["type"]
            if "extra" in m:
                converted_member["extra"] = m["extra"]
            converted_members.append(converted_member)
        
        data = {
            "group": {"group_info": group_info, "members": converted_members},
            "member_extra": member_extra if member_extra else "",
            "to_lines": to_lines if to_lines else [],
            "notify_message": notify_message
        }
        return RobotHttpUtils.http_json_post(url, data, headers, type(None))
    
    def dismiss_group(self, group_id: str) -> IMResult:
        """
        解散群组
        
        :param group_id: 群组ID
        :return: 解散结果
        """
        url = f"{self.im_url}{APIPath.Robot_Group_Dismiss}"
        headers = self._generate_auth_headers()
        data = {"group_id": group_id}
        return RobotHttpUtils.http_json_post(url, data, headers, type(None))
    
    def get_group_info(self, group_id: str) -> IMResult:
        """
        获取群组信息
        
        :param group_id: 群组ID
        :return: 群组信息
        """
        url = f"{self.im_url}{APIPath.Robot_Group_Get_Info}"
        headers = self._generate_auth_headers()
        data = {"groupId": group_id}
        return RobotHttpUtils.http_json_post(url, data, headers, PojoGroupInfo)
    
    def get_group_members(self, group_id: str) -> IMResult:
        """
        获取群组成员列表
        
        :param group_id: 群组ID
        :return: 群组成员列表
        """
        url = f"{self.im_url}{APIPath.Robot_Group_Member_List}"
        headers = self._generate_auth_headers()
        data = {"groupId": group_id}
        return RobotHttpUtils.http_json_post(url, data, headers, OutputGroupMemberList)
    
    def add_group_members(self, group_id: str, members: List[dict]) -> IMResult:
        """
        添加群组成员
        
        :param group_id: 群组ID
        :param members: 成员列表 (PojoGroupMember的dict格式列表)
        :return: 添加结果
        """
        url = f"{self.im_url}{APIPath.Robot_Group_Member_Add}"
        headers = self._generate_auth_headers()
        # Java后端使用下划线命名：member_id 等
        converted_members = []
        for m in members:
            converted_member = {}
            if "member_id" in m:
                converted_member["member_id"] = m["member_id"]
            if "alias" in m:
                converted_member["alias"] = m["alias"]
            if "type" in m:
                converted_member["type"] = m["type"]
            if "extra" in m:
                converted_member["extra"] = m["extra"]
            converted_members.append(converted_member)
        
        data = {"group_id": group_id, "members": converted_members}
        return RobotHttpUtils.http_json_post(url, data, headers, type(None))
    
    def kickoff_group_members(self, group_id: str, members: List[str]) -> IMResult:
        """
        踢出群组成员
        
        :param group_id: 群组ID
        :param members: 成员ID列表
        :return: 踢出结果
        """
        url = f"{self.im_url}{APIPath.Robot_Group_Member_Kickoff}"
        headers = self._generate_auth_headers()
        data = {"group_id": group_id, "members": members}
        return RobotHttpUtils.http_json_post(url, data, headers, type(None))
    
    def quit_group(self, group_id: str) -> IMResult:
        """
        退出群组
        
        :param group_id: 群组ID
        :return: 退出结果
        """
        url = f"{self.im_url}{APIPath.Robot_Group_Member_Quit}"
        headers = self._generate_auth_headers()
        data = {"group_id": group_id}
        return RobotHttpUtils.http_json_post(url, data, headers, type(None))
    
    def modify_group_info(self, group_id: str, modify_type: int, value: str) -> IMResult:
        """
        修改群组信息
        
        :param group_id: 群组ID
        :param modify_type: 修改类型
        :param value: 新值
        :return: 修改结果
        """
        url = f"{self.im_url}{APIPath.Robot_Group_Modify_Info}"
        headers = self._generate_auth_headers()
        data = {"group_id": group_id, "type": modify_type, "value": value}
        return RobotHttpUtils.http_json_post(url, data, headers, type(None))
    
    def transfer_group(self, group_id: str, new_owner: str) -> IMResult:
        """
        转让群组
        
        :param group_id: 群组ID
        :param new_owner: 新群主
        :return: 转让结果
        """
        url = f"{self.im_url}{APIPath.Robot_Group_Transfer}"
        headers = self._generate_auth_headers()
        data = {"group_id": group_id, "new_owner": new_owner}
        return RobotHttpUtils.http_json_post(url, data, headers, type(None))
    
    def set_group_manager(self, group_id: str, members: List[str], is_manager: bool) -> IMResult:
        """
        设置群组管理员
        
        :param group_id: 群组ID
        :param members: 成员ID列表
        :param is_manager: 是否设置为管理员
        :return: 设置结果
        """
        url = f"{self.im_url}{APIPath.Robot_Group_Set_Manager}"
        headers = self._generate_auth_headers()
        data = {"group_id": group_id, "members": members, "is_manager": is_manager}
        return RobotHttpUtils.http_json_post(url, data, headers, type(None))
    
    def mute_group_member(self, group_id: str, members: List[str], is_mute: bool) -> IMResult:
        """
        禁言群组成员
        
        :param group_id: 群组ID
        :param members: 成员ID列表
        :param is_mute: 是否禁言
        :return: 设置结果
        """
        url = f"{self.im_url}{APIPath.Robot_Group_Mute_Member}"
        headers = self._generate_auth_headers()
        data = {"group_id": group_id, "members": members, "is_mute": is_mute}
        return RobotHttpUtils.http_json_post(url, data, headers, type(None))
    
    def allow_group_member(self, group_id: str, members: List[str], is_allow: bool) -> IMResult:
        """
        允许群组成员发言
        
        :param group_id: 群组ID
        :param members: 成员ID列表
        :param is_allow: 是否允许
        :return: 设置结果
        """
        url = f"{self.im_url}{APIPath.Robot_Group_Allow_Member}"
        headers = self._generate_auth_headers()
        data = {"group_id": group_id, "members": members, "is_allow": is_allow}
        return RobotHttpUtils.http_json_post(url, data, headers, type(None))
    
    def set_group_member_alias(self, group_id: str, member_id: str, alias: str) -> IMResult:
        """
        设置群组成员别名
        
        :param group_id: 群组ID
        :param member_id: 成员ID
        :param alias: 别名
        :return: 设置结果
        """
        url = f"{self.im_url}{APIPath.Robot_Group_Set_Member_Alias}"
        headers = self._generate_auth_headers()
        data = {"group_id": group_id, "memberId": member_id, "alias": alias}
        return RobotHttpUtils.http_json_post(url, data, headers, type(None))
    
    def set_group_member_extra(self, group_id: str, member_id: str, extra: str) -> IMResult:
        """
        设置群组成员额外信息
        
        :param group_id: 群组ID
        :param member_id: 成员ID
        :param extra: 额外信息
        :return: 设置结果
        """
        url = f"{self.im_url}{APIPath.Robot_Group_Set_Member_Extra}"
        headers = self._generate_auth_headers()
        data = {"group_id": group_id, "memberId": member_id, "extra": extra}
        return RobotHttpUtils.http_json_post(url, data, headers, type(None))
    
    def reply_message(self, message_uid: int, payload: dict, is_locate: bool = False) -> IMResult:
        """
        回复消息
        
        :param message_uid: 要回复的消息UID
        :param payload: 消息内容
        :param is_locate: 是否定位到原消息
        :return: 发送结果
        """
        url = f"{self.im_url}{APIPath.Robot_Message_Reply}"
        headers = self._generate_auth_headers()
        data = {"messageUid": message_uid, "payload": payload, "locate": is_locate}
        return RobotHttpUtils.http_json_post(url, data, headers, SendMessageResult)
    
    def get_user_info_by_mobile(self, mobile: str) -> IMResult:
        """
        通过手机号获取用户信息
        
        :param mobile: 手机号
        :return: 用户信息
        """
        url = f"{self.im_url}{APIPath.Robot_User_Info}"
        headers = self._generate_auth_headers()
        data = {"mobile": mobile}
        return RobotHttpUtils.http_json_post(url, data, headers, OutputCreateGroupResult)
    
    def get_user_info_by_name(self, name: str) -> IMResult:
        """
        通过用户名获取用户信息
        
        :param name: 用户名
        :return: 用户信息
        """
        url = f"{self.im_url}{APIPath.Robot_User_Info}"
        headers = self._generate_auth_headers()
        data = {"name": name}
        return RobotHttpUtils.http_json_post(url, data, headers, OutputCreateGroupResult)
    
    def get_application_signature(self) -> IMResult:
        """
        获取应用签名配置
        
        :return: 应用签名配置
        """
        from .models import OutputApplicationConfigData
        url = f"{self.im_url}{APIPath.Robot_Get_Presigned_Upload_Url}"
        headers = self._generate_auth_headers()
        return RobotHttpUtils.http_json_post(url, None, headers, OutputApplicationConfigData)
    
    def application_get_user_info(self, auth_code: str) -> IMResult:
        """
        通过授权码获取用户信息
        
        :param auth_code: 授权码
        :return: 用户信息
        """
        url = f"{self.im_url}{APIPath.Robot_Application_Get_UserInfo}"
        headers = self._generate_auth_headers()
        data = {"authCode": auth_code}
        return RobotHttpUtils.http_json_post(url, data, headers, OutputApplicationUserInfo)


    # ==================== 朋友圈相关方法 ====================

    def post_moments_feed(self, feed_type: int, text: str, medias: List[dict] = None,
                          to_users: List[str] = None, exclude_users: List[str] = None,
                          mentioned_users: List[str] = None, extra: str = "") -> IMResult:
        """
        发布朋友圈动态

        :param feed_type: 动态类型 (0=文本, 1=图片, 2=视频, 3=链接)
        :param text: 文本内容
        :param medias: 媒体列表 (MediaEntry 的 dict 格式列表)
        :param to_users: 可见用户列表
        :param exclude_users: 排除用户列表
        :param mentioned_users: @用户列表
        :param extra: 额外信息
        :return: 发布结果
        """
        url = f"{self.im_url}{APIPath.Robot_Moments_Post_Feed}"
        headers = self._generate_auth_headers()
        data = {
            "type": feed_type,
            "text": text,
            "medias": medias if medias else [],
            "to": to_users if to_users else [],
            "ex": exclude_users if exclude_users else [],
            "mu": mentioned_users if mentioned_users else [],
            "extra": extra
        }
        return RobotHttpUtils.http_json_post(url, data, headers)

    def update_moments_feed(self, feed_id: int, feed_type: int, text: str, medias: List[dict] = None,
                            to_users: List[str] = None, exclude_users: List[str] = None,
                            mentioned_users: List[str] = None, extra: str = "") -> IMResult:
        """
        更新朋友圈动态

        :param feed_id: 动态ID
        :param feed_type: 动态类型
        :param text: 文本内容
        :param medias: 媒体列表
        :param to_users: 可见用户列表
        :param exclude_users: 排除用户列表
        :param mentioned_users: @用户列表
        :param extra: 额外信息
        :return: 更新结果
        """
        url = f"{self.im_url}{APIPath.Robot_Moments_Update_Feed}"
        headers = self._generate_auth_headers()
        data = {
            "feedId": feed_id,
            "type": feed_type,
            "text": text,
            "medias": medias if medias else [],
            "to": to_users if to_users else [],
            "ex": exclude_users if exclude_users else [],
            "mu": mentioned_users if mentioned_users else [],
            "extra": extra
        }
        return RobotHttpUtils.http_json_post(url, data, headers, type(None))

    def get_moments_feeds(self, feed_id: int = 0, count: int = 10, user_id: str = "") -> IMResult:
        """
        获取朋友圈动态列表

        :param feed_id: 起始动态ID (0表示从最新开始)
        :param count: 获取数量
        :param user_id: 指定用户ID (空字符串表示所有用户)
        :return: 动态列表
        """
        url = f"{self.im_url}{APIPath.Robot_Moments_Pull_Feeds}"
        headers = self._generate_auth_headers()
        data = {"feedId": feed_id, "count": count, "user": user_id}
        return RobotHttpUtils.http_json_post(url, data, headers)

    def get_moments_feed(self, feed_id: int) -> IMResult:
        """
        获取单条朋友圈动态

        :param feed_id: 动态ID
        :return: 动态详情
        """
        url = f"{self.im_url}{APIPath.Robot_Moments_Fetch_Feed}"
        headers = self._generate_auth_headers()
        data = {"feedId": feed_id}
        return RobotHttpUtils.http_json_post(url, data, headers)

    def delete_moments_feed(self, feed_id: int) -> IMResult:
        """
        删除朋友圈动态

        :param feed_id: 动态ID
        :return: 删除结果
        """
        url = f"{self.im_url}{APIPath.Robot_Moments_Recall_Feed}"
        headers = self._generate_auth_headers()
        data = {"id": feed_id}
        return RobotHttpUtils.http_json_post(url, data, headers, type(None))

    def post_moments_comment(self, feed_id: int, comment_type: int, text: str,
                             reply_id: int = 0, reply_to: str = "", extra: str = "") -> IMResult:
        """
        发布朋友圈评论

        :param feed_id: 动态ID
        :param comment_type: 评论类型 (0=文本, 1=点赞)
        :param text: 评论内容
        :param reply_id: 回复的评论ID
        :param reply_to: 回复给哪个用户
        :param extra: 额外信息
        :return: 发布结果
        """
        url = f"{self.im_url}{APIPath.Robot_Moments_Post_Comment}"
        headers = self._generate_auth_headers()
        data = {
            "feedId": feed_id,
            "type": comment_type,
            "text": text,
            "replyId": reply_id,
            "replyTo": reply_to,
            "extra": extra
        }
        return RobotHttpUtils.http_json_post(url, data, headers)

    def delete_moments_comment(self, feed_id: int, comment_id: int) -> IMResult:
        """
        删除朋友圈评论

        :param feed_id: 动态ID
        :param comment_id: 评论ID
        :return: 删除结果
        """
        url = f"{self.im_url}{APIPath.Robot_Moments_Recall_Comment}"
        headers = self._generate_auth_headers()
        data = {"id": comment_id, "id2": feed_id}
        return RobotHttpUtils.http_json_post(url, data, headers, type(None))

    def get_user_moments_profile(self, user_id: str) -> IMResult:
        """
        获取用户朋友圈资料

        :param user_id: 用户ID
        :return: 朋友圈资料
        """
        url = f"{self.im_url}{APIPath.Robot_Moments_Fetch_Profiles}"
        headers = self._generate_auth_headers()
        data = {"u": user_id}
        return RobotHttpUtils.http_json_post(url, data, headers)

    def update_moments_background_url(self, url_str: str) -> IMResult:
        """
        更新朋友圈背景图

        :param url_str: 背景图URL
        :return: 更新结果
        """
        url = f"{self.im_url}{APIPath.Robot_Moments_Update_Profiles_Value}"
        headers = self._generate_auth_headers()
        data = {"t": 0, "v": url_str}  # t=0 表示背景图
        return RobotHttpUtils.http_json_post(url, data, headers, type(None))

    def update_moments_stranger_visible_count(self, count: int) -> IMResult:
        """
        更新陌生人可见动态数量

        :param count: 数量
        :return: 更新结果
        """
        url = f"{self.im_url}{APIPath.Robot_Moments_Update_Profiles_Value}"
        headers = self._generate_auth_headers()
        data = {"t": 1, "i": count}  # t=1 表示陌生人可见数量
        return RobotHttpUtils.http_json_post(url, data, headers, type(None))

    def update_moments_visible_scope(self, scope: int) -> IMResult:
        """
        更新朋友圈可见范围

        :param scope: 0=无限制, 1=3天, 2=1月, 3=6月
        :return: 更新结果
        """
        url = f"{self.im_url}{APIPath.Robot_Moments_Update_Profiles_Value}"
        headers = self._generate_auth_headers()
        data = {"t": 2, "i": scope}  # t=2 表示可见范围
        return RobotHttpUtils.http_json_post(url, data, headers, type(None))

    def update_moments_black_list(self, add_list: List[str] = None, remove_list: List[str] = None) -> IMResult:
        """
        更新朋友圈黑名单

        :param add_list: 添加的用户列表
        :param remove_list: 移除的用户列表
        :return: 更新结果
        """
        url = f"{self.im_url}{APIPath.Robot_Moments_Update_Profiles_List_Value}"
        headers = self._generate_auth_headers()
        data = {"b": False, "al": add_list if add_list else [], "rl": remove_list if remove_list else []}
        return RobotHttpUtils.http_json_post(url, data, headers, type(None))

    def update_moments_block_list(self, add_list: List[str] = None, remove_list: List[str] = None) -> IMResult:
        """
        更新朋友圈屏蔽列表

        :param add_list: 添加的用户列表
        :param remove_list: 移除的用户列表
        :return: 更新结果
        """
        url = f"{self.im_url}{APIPath.Robot_Moments_Update_Profiles_List_Value}"
        headers = self._generate_auth_headers()
        data = {"b": True, "al": add_list if add_list else [], "rl": remove_list if remove_list else []}
        return RobotHttpUtils.http_json_post(url, data, headers, type(None))
