#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
野火IM Server SDK Python示例程序主类
对应Java SDK中的 cn.wildfirechat.sdk.Main

提供SDK功能演示的示例代码，包括：
- 用户管理操作
- 群组管理操作
- 消息发送操作
- 好友关系管理
- 聊天室功能
- 频道功能
- 机器人功能
"""
import logging
import sys
import time
import uuid
from datetime import datetime
from typing import List

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from wildfirechat import AdminConfig, UserAdmin, GroupAdmin, MessageAdmin, RelationAdmin
from wildfirechat import ChatroomAdmin, ChannelAdmin, GeneralAdmin, SensitiveAdmin, ConferenceAdmin
from wildfirechat import RobotService, ChannelServiceApi, MomentsAdmin
from wildfirechat.error_code import ErrorCode
from wildfirechat.proto_constants import (
    Platform, ModifyGroupInfoType, UpdateUserInfoMask, SystemSettingType,
    GroupMemberType, ConversationType, MyInfoType, ModifyChannelInfoType,
    ChannelState
)
from wildfirechat.models import (
    InputOutputUserInfo, InputCreateRobot, Conversation, MessagePayload,
    PojoGroupInfo, PojoGroupMember, InputCreateChannel, PojoChannelMenu,
    OutputStringList, OutputGetChannelInfo
)
from wildfirechat.message_content import (
    TextMessageContent, SoundMessageContent, ImageMessageContent, VideoMessageContent,
    FileMessageContent, LocationMessageContent, StickerMessageContent, LinkMessageContent,
    CardMessageContent, TipNotificationMessageContent, RichNotificationMessageContent,
    StreamTextGeneratingMessageContent, StreamTextGeneratedMessageContent, ArticleContent
)


class Main:
    """野火IM Server SDK示例程序主类"""
    
    def __init__(self):
        # 是否为商业版服务器
        self.commercial_server = True
        # 是否启用高级音视频功能
        self.advance_voip = True
        # 是否启用机器人朋友圈功能
        self.robot_moments_enabled = True
        # 是否启用朋友圈功能
        self.moments_enabled = True
        # 管理端口是18080
        self.admin_url = "http://localhost:18080"
        # 管理员密钥
        self.admin_secret = "123456"
        # 机器人和频道使用IM服务的公开端口80，注意不是18080
        self.im_url = "http://localhost"
    
    def run(self, args: List[str]):
        """
        程序主入口
        
        :param args: 命令行参数，包括：adminUrl、adminSecret、imUrl、commercialServer、advanceVoip
        """
        # 解析命令行参数
        if len(args) == 5:
            self.admin_url = args[0]
            self.admin_secret = args[1]
            self.im_url = args[2]
            self.commercial_server = args[3].lower() == "true"
            self.advance_voip = args[4].lower() == "true"
        else:
            if len(args) == 1 and args[0] in ("-h", "--help", "-help"):
                self._print_help()
                return
            self._print_help()
            logger.info(f"使用默认值: adminUrl={self.admin_url}, adminSecret={self.admin_secret}, "
                        f"imUrl={self.im_url}, commercialServer={self.commercial_server}, advanceVoip={self.advance_voip}")
        
        # admin使用的是18080端口，超级管理接口，理论上不能对外开放端口，也不能让非内部服务知悉密钥。
        # 执行管理员API测试
        self.test_admin()
        
        # 计算消息分表
        self.test_message_sharding()
        
        # Robot和Channel都是使用的80端口，第三方可以创建或者为第三方创建，第三方可以使用robot或者channel与IM系统进行对接。
        # 测试机器人功能
        self.test_robot()
        # 测试频道功能
        self.test_channel()
        
        logger.info("所有测试通过！")
    
    def _print_help(self):
        """打印帮助信息"""
        logger.info("Usage: python main.py adminUrl adminSecret imUrl commercialServer advanceVoip")
        logger.info("      e.g. python main.py http://192.168.1.80:18080 123456 http://192.168.1.80 false false")
    
    def test_admin(self):
        """
        管理员API测试总入口
        
        测试所有管理员功能，包括：
        - 用户管理
        - 用户关系管理
        - 群组管理
        - 聊天室管理
        - 消息管理
        - 消息内容测试
        - 频道API测试
        - 通用API测试
        - 敏感词API测试
        - 设备管理测试(仅商业版)
        - 会议功能测试(仅高级音视频版)
        - 朋友圈功能测试(仅启用时)
        """
        # 初始化服务API，使用管理员URL和密钥
        AdminConfig.init_admin(self.admin_url, self.admin_secret)
        
        # 执行各类管理员API测试
        self.test_user()           # 用户管理测试
        self.test_user_relation()  # 用户关系测试
        self.test_group()          # 群组管理测试
        self.test_chatroom()       # 聊天室测试
        self.test_message()        # 消息发送测试
        self.test_message_content() # 消息内容编码测试
        self.test_channel_api()    # 频道API测试
        self.test_general_api()    # 通用API测试
        self.test_sensitive_api()  # 敏感词API测试
        
        # 商业版功能测试
        # if self.commercial_server:
        #     self.test_device()     # 设备测试(仅商业版)
        
        # 高级音视频功能测试
        if self.advance_voip:
            self.test_conference() # 会议功能测试(仅高级音视频版)
        
        # 朋友圈功能测试
        if self.moments_enabled:
            self.test_moments_api() # 朋友圈API测试
        
        logger.info("Congratulation, all admin test case passed!!!!!!!")
    
    def test_user(self):
        """
        用户管理API测试
        
        测试以下功能：
        - 创建普通用户
        - 创建和删除机器人
        - 获取用户信息（按用户名、手机号、用户ID、邮箱）
        - 批量获取用户信息
        - 更新用户信息
        - 获取用户IM Token
        - 用户封禁/解封
        - 检查用户在线状态
        - 销毁用户（慎用）
        - 获取所有用户列表
        - 获取在线用户数量和列表（仅商业版）
        - 获取用户会话信息（仅商业版）
        """
        # 创建用户信息对象
        user_info = InputOutputUserInfo()
        user_info.userId = "userId1"
        user_info.name = "user1"
        user_info.mobile = "13900000000"
        user_info.displayName = "user 1"
        
        # 调用SDK创建用户
        result_create_user = UserAdmin.create_user(user_info)
        if result_create_user and result_create_user.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info(f"Create user {result_create_user.result.name} success")
        else:
            logger.info("Create user failure")
            sys.exit(-1)
        
        # 创建机器人信息对象
        create_robot = InputCreateRobot()
        create_robot.userId = "robot1"
        create_robot.name = "robot1"
        create_robot.displayName = "机器人"
        create_robot.owner = "userId1"
        create_robot.secret = "123456"
        create_robot.callback = "http://127.0.0.1:8883/robot/recvmsg"
        
        # 调用SDK创建机器人
        result_create_robot = UserAdmin.create_robot(create_robot)
        if result_create_robot and result_create_robot.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info(f"Create robot {result_create_robot.result.userId} success")
        else:
            logger.info("Create robot failure")
            sys.exit(-1)
        
        # 获取机器人信息
        output_robot_result = UserAdmin.get_robot_info("robot1")
        if output_robot_result and output_robot_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("Get robot success")
        else:
            logger.info("Get robot failure")
            sys.exit(-1)
        
        # 销毁机器人
        destroy_result = UserAdmin.destroy_robot("robot1")
        if destroy_result and destroy_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("Destroy robot success")
        else:
            logger.info("Destroy robot failure")
            sys.exit(-1)
        
        # 通过用户名获取用户信息
        result_get_user_info1 = UserAdmin.get_user_by_name(user_info.name)
        if result_get_user_info1 and result_get_user_info1.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            result = result_get_user_info1.result
            if (result.userId == user_info.userId and 
                result.name == user_info.name and
                result.mobile == user_info.mobile and
                result.displayName == user_info.displayName):
                logger.info("get user info success")
            else:
                logger.info("get user info by name failure")
                sys.exit(-1)
        else:
            logger.info("get user info by name failure")
            sys.exit(-1)
        
        # 通过手机号获取用户信息
        result_get_user_info2 = UserAdmin.get_user_by_mobile(user_info.mobile)
        if result_get_user_info2 and result_get_user_info2.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            result = result_get_user_info2.result
            if (result.userId == user_info.userId and
                result.name == user_info.name and
                result.mobile == user_info.mobile and
                result.displayName == user_info.displayName):
                logger.info("get user info success")
            else:
                logger.info("get user info by mobile failure")
                sys.exit(-1)
        else:
            logger.info("get user info by mobile failure")
            sys.exit(-1)
        
        # 通过用户ID获取用户信息
        result_get_user_info3 = UserAdmin.get_user_by_user_id(user_info.userId)
        if result_get_user_info3 and result_get_user_info3.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            result = result_get_user_info3.result
            if (result.userId == user_info.userId and
                result.name == user_info.name and
                result.mobile == user_info.mobile and
                result.displayName == user_info.displayName):
                logger.info("get user info success")
            else:
                logger.info("get user info by userId failure")
                sys.exit(-1)
        else:
            logger.info("get user info by userId failure")
            sys.exit(-1)
        
        # 通过邮箱获取用户信息（允许用户不存在）
        user_info_list_result = UserAdmin.get_user_by_email("13900000001@139.com")
        if (user_info_list_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS or
            user_info_list_result.get_error_code() == ErrorCode.ERROR_CODE_NOT_EXIST):
            logger.info("getUserByEmail success")
        else:
            logger.info("getUserByEmail failure")
            sys.exit(-1)
        
        # 批量获取用户信息
        batch_get_users = UserAdmin.get_batch_users(["userId1", "admin", "FireRobot", "TestUser"])
        if batch_get_users.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("get batch user success")
        else:
            logger.info("get batch user failure")
            sys.exit(-1)
        
        # 准备更新用户信息（先测试不存在的用户ID）
        update_user_info = InputOutputUserInfo()
        update_user_info.userId = str(int(time.time() * 1000))
        update_user_info.displayName = "updatedUserName"
        update_user_info.portrait = "updatedUserPortrait"
        # 设置更新标志：更新显示名称和头像
        update_user_flag = UpdateUserInfoMask.Update_User_DisplayName | UpdateUserInfoMask.Update_User_Portrait
        result = UserAdmin.update_user_info(update_user_info, update_user_flag)
        if result and result.get_error_code() == ErrorCode.ERROR_CODE_NOT_EXIST:
            logger.info("updateUserInfo success (not exist)")
        else:
            logger.info("updateUserInfo failure")
            sys.exit(-1)
        
        # 更新存在的用户信息
        update_user_info.userId = user_info.userId
        result = UserAdmin.update_user_info(update_user_info, update_user_flag)
        if result and result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("updateUserInfo success")
        else:
            logger.info("updateUserInfo failure")
            sys.exit(-1)
        
        # 验证用户信息是否更新成功
        result_get_user_info4 = UserAdmin.get_user_by_user_id(user_info.userId)
        if result_get_user_info4 and result_get_user_info4.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            result = result_get_user_info4.result
            if (result.userId == user_info.userId and
                result.displayName == update_user_info.displayName and
                result.portrait == update_user_info.portrait):
                logger.info("get user info success")
            else:
                logger.info("get user info by userId failure")
                sys.exit(-1)
        else:
            logger.info("get user info by userId failure")
            sys.exit(-1)
        
        # 获取用户的IM Token，用于客户端登录
        result_get_token = UserAdmin.get_user_token(user_info.userId, "client111", Platform.Platform_Android)
        if result_get_token and result_get_token.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info(f"get token success: {result_get_token.result.token}")
        else:
            logger.info("get user token failure")
            sys.exit(-1)
        
        # 封禁用户（状态码：2表示封禁）
        result_void = UserAdmin.update_user_block_status(user_info.userId, 2)
        if result_void and result_void.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("block user done")
        else:
            logger.info("block user failure")
            sys.exit(-1)
        
        # 检查用户封禁状态
        result_check_user_status = UserAdmin.check_user_block_status(user_info.userId)
        if result_check_user_status and result_check_user_status.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            if result_check_user_status.result.status == 2:
                logger.info("check user status success")
            else:
                logger.info("user status not correct")
                sys.exit(-1)
        else:
            logger.info("check user block status failure")
            sys.exit(-1)
        
        # 获取所有被封禁用户列表
        result_block_status_list = UserAdmin.get_blocked_list()
        if result_block_status_list and result_block_status_list.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            success = False
            for block_status in result_block_status_list.result.statusList:
                if block_status.userId == user_info.userId and block_status.status == 2:
                    logger.info("get block list done")
                    success = True
                    break
            if not success:
                logger.info("block user status is not expected")
                sys.exit(-1)
        else:
            logger.info("get block list failure")
            sys.exit(-1)
        
        # 解封用户（状态码：0表示正常）
        result_void = UserAdmin.update_user_block_status(user_info.userId, 0)
        if result_void and result_void.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("unblock user done")
        else:
            logger.info("unblock user failure")
            sys.exit(-1)
        
        # 再次检查用户状态，确认已解封
        result_check_user_status = UserAdmin.check_user_block_status(user_info.userId)
        if result_check_user_status and result_check_user_status.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            if result_check_user_status.result.status == 0:
                logger.info("check user status success")
            else:
                logger.info("user status not correct")
                sys.exit(-1)
        else:
            logger.info("check user block status failure")
            sys.exit(-1)
        
        # 检查用户在线状态
        output_check_user_online = UserAdmin.check_user_online_status(user_info.userId)
        if output_check_user_online and output_check_user_online.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info(f"check user online status success: {len(output_check_user_online.result.sessions)}")
        else:
            logger.info("check user online failure")
            sys.exit(-1)
        
        # 测试踢下线用户客户端
        kickoff_result = UserAdmin.kickoff_user_client(user_info.userId, None)
        if kickoff_result and kickoff_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("kickoff user client success")
        else:
            logger.info("kickoff user client failure")
            sys.exit(-1)
        
        # 慎用，这个方法可能功能不完全，如果用户不再需要，建议使用block功能屏蔽用户
        # 销毁用户（物理删除，不可恢复）
        void_im_result = UserAdmin.destroy_user("user11")
        if void_im_result and void_im_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("destroy user success")
        else:
            logger.info("destroy user failure")
            sys.exit(-1)
        
        # 获取所有用户列表（分页：每页100条，第0页）
        get_user_list_result = UserAdmin.get_all_users(100, 0)
        if get_user_list_result and get_user_list_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("getUserListIMResult success")
        else:
            logger.info("getUserListIMResult failure")
            sys.exit(-1)
        
        # 商业版专属功能
        if self.commercial_server:
            # 获取在线用户总数
            get_online_user_count_result = UserAdmin.get_online_user_count()
            if get_online_user_count_result and get_online_user_count_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("get user online count success")
            else:
                logger.info("get user online count failure")
                sys.exit(-1)
            
            # 获取在线用户列表（分页：第1页，从0开始，每页100条）
            get_online_user_result = UserAdmin.get_online_user(1, 0, 100)
            if get_online_user_result and get_online_user_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("get user online success")
            else:
                logger.info("get user online failure")
                sys.exit(-1)
            
            # 获取指定用户的会话信息
            get_user_session_result = UserAdmin.get_user_session("userId1")
            if get_user_session_result and get_user_session_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("get user session success")
            else:
                logger.info("get user session failure")
                sys.exit(-1)
    
    def test_user_relation(self):
        """
        用户关系管理API测试
        
        测试以下功能：
        - 发送好友请求
        - 设置好友关系
        - 获取好友列表
        - 解除好友关系
        - 黑名单管理
        - 好友备注（别名）管理
        - 好友额外信息管理
        - 获取好友关系详情
        """
        # 先创建2个用户用于测试好友关系
        user_info = InputOutputUserInfo()
        user_info.userId = "ff1"
        user_info.name = "ff1"
        user_info.mobile = "13800000000"
        user_info.displayName = "ff1"
        
        # 调用SDK创建第一个用户
        result_create_user = UserAdmin.create_user(user_info)
        if result_create_user and result_create_user.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info(f"Create user {result_create_user.result.name} success")
        else:
            logger.info("Create user failure")
            sys.exit(-1)
        
        # 创建第二个用户
        user_info = InputOutputUserInfo()
        user_info.userId = "ff2"
        user_info.name = "ff2"
        user_info.mobile = "13800000001"
        user_info.displayName = "ff2"
        
        # 调用SDK创建第二个用户
        result_create_user = UserAdmin.create_user(user_info)
        if result_create_user and result_create_user.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info(f"Create user {result_create_user.result.name} success")
        else:
            logger.info("Create user failure")
            sys.exit(-1)
        
        # 发送好友请求：ff1向ff2发送好友请求，附带问候语"hello"，直接设为好友
        result = RelationAdmin.send_friend_request("ff1", "ff2", "hello", True)
        if result and (result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS or
                       result.get_error_code() == ErrorCode.ERROR_CODE_ALREADY_FRIENDS):
            logger.info("send friend request success")
        else:
            logger.info("send friend request failure")
            sys.exit(-1)
        
        # 设置好友关系：ff1把ff2设为好友，并附带额外信息
        update_friend_status_result = RelationAdmin.set_user_friend("ff1", "ff2", True, '{"from":1}')
        if update_friend_status_result and update_friend_status_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("update friend status success")
        else:
            logger.info("update friend status failure")
            sys.exit(-1)
        
        # 获取ff1的好友列表
        result_get_friend_list = RelationAdmin.get_friend_list("ff1")
        if result_get_friend_list and result_get_friend_list.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            if "ff2" in result_get_friend_list.result.list:
                logger.info("get friend status success")
            else:
                logger.info("get friend status failure")
                sys.exit(-1)
        else:
            logger.info("get friend status failure")
            sys.exit(-1)
        
        # 解除好友关系：ff1删除ff2
        update_friend_status_result = RelationAdmin.set_user_friend("ff1", "ff2", False, None)
        if update_friend_status_result and update_friend_status_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("update friend status success")
        else:
            logger.info("update friend status failure")
            sys.exit(-1)
        
        # 再次获取好友列表，确认ff2已被删除
        result_get_friend_list = RelationAdmin.get_friend_list("ff1")
        if result_get_friend_list and result_get_friend_list.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            if "ff2" not in result_get_friend_list.result.list:
                logger.info("get friend status success")
            else:
                logger.info("get friend status failure")
                sys.exit(-1)
        else:
            logger.info("get friend status failure")
            sys.exit(-1)
        
        # 将ff2加入黑名单：ff1把ff2加入黑名单
        update_blacklist_status_result = RelationAdmin.set_user_blacklist("ff1", "ff2", True)
        if update_blacklist_status_result and update_blacklist_status_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("update blacklist status success")
        else:
            logger.info("update blacklist status failure")
            sys.exit(-1)
        
        # 获取黑名单列表
        result_get_friend_list = RelationAdmin.get_user_blacklist("ff1")
        if result_get_friend_list and result_get_friend_list.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            if "ff2" in result_get_friend_list.result.list:
                logger.info("get blacklist status success")
            else:
                logger.info("get blacklist status failure")
                sys.exit(-1)
        else:
            logger.info("get blacklist status failure")
            sys.exit(-1)
        
        # 设置好友备注（别名）
        alias = f"hello{int(time.time() * 1000)}"
        update_friend_alias = RelationAdmin.update_friend_alias("ff1", "ff2", alias)
        if update_friend_alias and update_friend_alias.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("update friend alias success")
        else:
            logger.info("update friend alias failure")
            sys.exit(-1)
        
        # 获取好友备注（别名）
        get_friend_alias = RelationAdmin.get_friend_alias("ff1", "ff2")
        if get_friend_alias and get_friend_alias.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            if get_friend_alias.result.alias == alias:
                logger.info("get friend alias success")
            else:
                logger.info("get friend alias failure")
                sys.exit(-1)
        else:
            logger.info("get friend alias failure")
            sys.exit(-1)
        
        # 设置好友额外信息（可以存储自定义数据）
        friend_extra = "hello friend extra"
        set_extra_result = RelationAdmin.update_friend_extra("ff1", "ff2", friend_extra)
        if set_extra_result and set_extra_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("set friend extra success")
        else:
            logger.info("set friend extra failure")
            sys.exit(-1)
        
        # 获取好友关系详情（包括额外信息等）
        get_relation = RelationAdmin.get_relation("ff1", "ff2")
        if get_relation and get_relation.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("get friend relation success")
        else:
            logger.info("get friend relation failure")
            sys.exit(-1)
        
        # 验证好友额外信息是否正确
        if friend_extra != get_relation.result.extra:
            logger.info("set friend extra failure")
            sys.exit(-1)
        
        # 测试获取用户的机器人列表
        user_robots_result = UserAdmin.get_user_robots("ff1")
        if user_robots_result and user_robots_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("get user robots success")
        else:
            logger.info("get user robots failure")
            sys.exit(-1)
    
    def test_group(self):
        """群组管理API测试"""
        # 先解散可能存在的测试群组
        GroupAdmin.dismiss_group("user1", "groupId1", None, None)
        
        group_info = PojoGroupInfo()
        group_info.target_id = "groupId1"
        group_info.owner = "user1"
        group_info.name = "test_group"
        group_info.extra = "hello extra"
        group_info.type = 2
        group_info.portrait = "http://portrait"
        
        members = []
        member1 = PojoGroupMember()
        member1.member_id = group_info.owner
        members.append(member1)
        
        member2 = PojoGroupMember()
        member2.member_id = "user2"
        members.append(member2)
        
        member3 = PojoGroupMember()
        member3.member_id = "user3"
        members.append(member3)
        
        result_create_group = GroupAdmin.create_group(group_info.owner, group_info, members, None, None, None)
        if result_create_group and result_create_group.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("create group success")
        else:
            logger.info("create group failure")
            sys.exit(-1)
        
        result_get_group_info = GroupAdmin.get_group_info(group_info.target_id)
        if result_get_group_info and result_get_group_info.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            result = result_get_group_info.result
            if (result.extra == group_info.extra and
                result.name == group_info.name and
                result.owner == group_info.owner):
                logger.info("get group success")
            else:
                logger.info("group info is not expected")
                sys.exit(-1)
        else:
            logger.info("get group info failure")
            sys.exit(-1)
        
        void_im_result = GroupAdmin.transfer_group(group_info.owner, group_info.target_id, "user2", None, None)
        if void_im_result and void_im_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("transfer success")
        else:
            logger.info("transfer group failure")
            sys.exit(-1)
        
        void_im_result = GroupAdmin.modify_group_info(
            group_info.owner, group_info.target_id,
            ModifyGroupInfoType.Modify_Group_Name, "HelloWorld", None, None
        )
        if void_im_result and void_im_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("modify group name success")
        else:
            logger.info("modify group name failure")
            sys.exit(-1)
        
        void_im_result = GroupAdmin.modify_group_info(
            group_info.owner, group_info.target_id,
            ModifyGroupInfoType.Modify_Group_Extra, "HelloWorld2", None, None
        )
        if void_im_result and void_im_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("modify group extra success")
        else:
            logger.info("modify group extra failure")
            sys.exit(-1)
        
        result_get_group_info = GroupAdmin.get_group_info(group_info.target_id)
        if result_get_group_info and result_get_group_info.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            if result_get_group_info.result.owner == "user2":
                group_info.owner = "user2"
                logger.info("get group success")
            else:
                logger.info("group info is not expected")
                sys.exit(-1)
        else:
            logger.info("get group info failure")
            sys.exit(-1)
        
        result_get_members = GroupAdmin.get_group_members(group_info.target_id)
        if result_get_members and result_get_members.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("get group member success")
        else:
            logger.info("get group member failure")
            sys.exit(-1)
        
        m = PojoGroupMember()
        m.member_id = "user1"
        m.alias = "hello user1"
        
        void_im_result = GroupAdmin.add_group_members("user1", group_info.target_id, [m], None, None, None)
        if void_im_result and void_im_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("add group member success")
        else:
            logger.info("add group member failure")
            sys.exit(-1)
        
        group_member_result = GroupAdmin.get_group_member(group_info.target_id, "user1")
        if group_member_result and group_member_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("get group member success")
        else:
            logger.info("get group member failure")
            sys.exit(-1)
        
        void_im_result = GroupAdmin.kickoff_group_members("user1", group_info.target_id, ["user3"], None, None)
        if void_im_result and void_im_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("kickoff group member success")
        else:
            logger.info("kickoff group member failure")
            sys.exit(-1)
        
        void_im_result = GroupAdmin.set_group_member_alias("user1", group_info.target_id, "user2", "test user2", None, None)
        if void_im_result and void_im_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("set group member alias success")
        else:
            logger.info("set group member alias failure")
            sys.exit(-1)
        
        void_im_result = GroupAdmin.set_group_member_extra(
            group_info.owner, group_info.target_id, group_info.owner,
            "hello member extra2", None, None
        )
        if void_im_result and void_im_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("set group member extra success")
        else:
            logger.info("set group member extra failure")
            sys.exit(-1)
        
        if self.commercial_server:
            m4 = PojoGroupMember()
            m4.member_id = "user4"
            m4.alias = "hello user4"
            
            m5 = PojoGroupMember()
            m5.member_id = "user5"
            m5.alias = "hello user5"
            
            void_im_result = GroupAdmin.add_group_members("user1", group_info.target_id, [m4, m5], None, None, None)
            if void_im_result and void_im_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("add group member success")
            else:
                logger.info("add group member failure")
                sys.exit(-1)
            
            void_im_result = GroupAdmin.set_group_manager("user1", group_info.target_id, ["user4", "user5"], True, None, None)
            if void_im_result and void_im_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("set group manager success")
            else:
                logger.info("set group manager failure")
                sys.exit(-1)
            
            void_im_result = GroupAdmin.set_group_manager("user1", group_info.target_id, ["user4", "user5"], False, None, None)
            if void_im_result and void_im_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("cancel group manager success")
            else:
                logger.info("cancel group manager failure")
                sys.exit(-1)
        
        void_im_result = GroupAdmin.quit_group("user4", group_info.target_id, None, None)
        if void_im_result and void_im_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("quit group success")
        else:
            logger.info("quit group failure")
            sys.exit(-1)
        
        group_ids_result = GroupAdmin.get_user_groups("user1")
        if group_ids_result and group_ids_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            if group_info.target_id in group_ids_result.result.groupIds:
                logger.info("get user groups success")
            else:
                logger.info("get user groups failure")
                sys.exit(-1)
        else:
            logger.info("get user groups failure")
            sys.exit(-1)
        
        group_ids_result = GroupAdmin.get_user_groups_by_type(
            "user2", [GroupMemberType.GroupMemberType_Manager, GroupMemberType.GroupMemberType_Owner]
        )
        if group_ids_result and group_ids_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("get user groups by type success")
        else:
            logger.info("get user groups by type failure")
            sys.exit(-1)
        
        group_ids_result = GroupAdmin.get_common_groups("user1", "user2")
        if group_ids_result and group_ids_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("get user common groups success")
        else:
            logger.info("get user common groups failure")
            sys.exit(-1)
        
        # 测试批量获取群组信息
        batch_group_info_result = GroupAdmin.batch_group_infos([group_info.target_id])
        if batch_group_info_result and batch_group_info_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("batch get group info success")
        else:
            logger.info("batch get group info failure")
            sys.exit(-1)
        
        # 测试群备注功能
        group_remark = "test group remark"
        set_group_remark_result = GroupAdmin.set_group_remark("user1", group_info.target_id, group_remark)
        if set_group_remark_result and set_group_remark_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("set group remark success")
        else:
            logger.info("set group remark failure")
            sys.exit(-1)

        time.sleep(1)
        get_group_remark_result = GroupAdmin.get_group_remark("user1", group_info.target_id)
        if (get_group_remark_result and 
            get_group_remark_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS and
            get_group_remark_result.result == group_remark):
            logger.info("get group remark success")
        else:
            logger.info("get group remark failure")
            sys.exit(-1)
        
        # 测试收藏群功能
        set_fav_group_result = GroupAdmin.set_fav_group("user1", group_info.target_id, True)
        if set_fav_group_result and set_fav_group_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("set fav group success")
        else:
            logger.info("set fav group failure")
            sys.exit(-1)
        
        time.sleep(1)
        is_fav_group_result = GroupAdmin.is_fav_group("user1", group_info.target_id)
        if (is_fav_group_result and 
            is_fav_group_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS and
            is_fav_group_result.result):
            logger.info("is fav group success")
        else:
            logger.info("is fav group failure")
            sys.exit(-1)
        
        # 取消收藏
        set_fav_group_result = GroupAdmin.set_fav_group("user1", group_info.target_id, False)
        if set_fav_group_result and set_fav_group_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("cancel fav group success")
        else:
            logger.info("cancel fav group failure")
            sys.exit(-1)
        
        # 仅专业版支持
        if self.commercial_server:
            # 开启群成员禁言
            void_im_result = GroupAdmin.mute_group_member("user1", group_info.target_id, ["user5"], True, None, None)
            if void_im_result and void_im_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("mute group member success")
            else:
                logger.info("mute group member failure")
                sys.exit(-1)
            # 关闭群成员禁言
            void_im_result = GroupAdmin.mute_group_member("user1", group_info.target_id, ["user5"], False, None, None)
            if void_im_result and void_im_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("unmute group member success")
            else:
                logger.info("unmute group member failure")
                sys.exit(-1)
            
            # 开启群成员白名单，当群全局禁言时，白名单用户可以发言
            void_im_result = GroupAdmin.allow_group_member("user1", group_info.target_id, ["user5"], True, None, None)
            if void_im_result and void_im_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("allow group member success")
            else:
                logger.info("allow group member failure")
                sys.exit(-1)
            
            # 关闭群成员白名单
            void_im_result = GroupAdmin.allow_group_member("user1", group_info.target_id, ["user5"], False, None, None)
            if void_im_result and void_im_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("unallow group member success")
            else:
                logger.info("unallow group member failure")
                sys.exit(-1)
        
        # 测试解散群组
        dismiss_group_result = GroupAdmin.dismiss_group("user2", group_info.target_id, None, None)
        if dismiss_group_result and dismiss_group_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("dismiss group success")
        else:
            logger.info("dismiss group failure")
            sys.exit(-1)
        
        # 验证群组已被解散
        result_get_group_info = GroupAdmin.get_group_info(group_info.target_id)
        if result_get_group_info and result_get_group_info.get_error_code() == ErrorCode.ERROR_CODE_NOT_EXIST:
            logger.info("group dismissed verified")
        else:
            logger.info("group dismiss verify failure")
            sys.exit(-1)
    
    def test_message(self):
        """消息管理API测试"""
        # 创建会话对象：目标用户ff2，会话类型为私聊
        conversation = Conversation()
        conversation.type = ConversationType.ConversationType_Private
        conversation.target = "ff2"
        
        # 创建文本消息内容并编码为MessagePayload
        text_message_content = TextMessageContent("Hello world")
        payload = text_message_content.encode()
        
        result_send_message = MessageAdmin.send_message("ff1", conversation, payload, None)
        if result_send_message and result_send_message.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("send message success")
        else:
            logger.info("send message failure")
            sys.exit(-1)
        
        output_message_data_result = MessageAdmin.get_message(result_send_message.result.messageUid)
        if (output_message_data_result and 
            output_message_data_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS and
            output_message_data_result.result.messageId == result_send_message.result.messageUid):
            logger.info("get message success")
        else:
            logger.info("get message failure")
            sys.exit(-1)
        
        string_result = MessageAdmin.recall_message("user1", result_send_message.result.messageUid)
        if string_result and string_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("recall message success")
        else:
            logger.info("recall message failure")
            sys.exit(-1)
        
        if self.commercial_server:
            # 商业版功能
            # 删除消息
            delete_result = MessageAdmin.delete_message(result_send_message.result.messageUid)
            if delete_result and delete_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("delete message success")
            else:
                logger.info("delete message failure")
                sys.exit(-1)
            
            # 重新发送消息用于更新测试
            payload.searchableContent = "hello world2"
            result_send_message = MessageAdmin.send_message("user1", conversation, payload, None)
            if result_send_message and result_send_message.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("send message success")
            else:
                logger.info("send message failure")
                sys.exit(-1)
            
            # 更新消息内容
            payload.searchableContent = "hello world3"
            update_result = MessageAdmin.update_message_content(
                "user1", result_send_message.result.messageUid, payload, True
            )
            if update_result and update_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("update message success")
            else:
                logger.info("update message failure")
                sys.exit(-1)
            
            # 广播消息
            broadcast_result = MessageAdmin.broadcast_message("user1", 0, payload)
            if broadcast_result and broadcast_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("broad message success")
            else:
                logger.info("broad message failure")
                sys.exit(-1)
            
            # 撤回广播消息
            recall_broadcast_result = MessageAdmin.recall_broadcast_message(
                "user1", broadcast_result.result.messageUid
            )
            if recall_broadcast_result and recall_broadcast_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("recall broadcast message success")
            else:
                logger.info("recall broadcast message failure")
            
            # 删除广播消息
            delete_broadcast_result = MessageAdmin.delete_broadcast_message(
                "user1", broadcast_result.result.messageUid
            )
            if delete_broadcast_result and delete_broadcast_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("delete broadcast message success")
            else:
                logger.info("delete broadcast message failure")
            
            # 获取会话已读时间戳
            from wildfirechat.models import Conversation as ConvModel
            conv = ConvModel()
            conv.type = ConversationType.ConversationType_Private
            conv.target = "admin"
            conv.line = 0
            read_time_result = MessageAdmin.get_conversation_read_timestamp("userId1", conv)
            if read_time_result and read_time_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("get conversation read time success")
            else:
                logger.info("get conversation read time failure")
            
            # 获取消息投递状态
            delivery_result = MessageAdmin.get_message_delivery("userId1")
            if delivery_result and delivery_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("get message delivery success")
            else:
                logger.info("get message delivery failure")
            
            # 清除会话
            clear_conv_result = MessageAdmin.clear_conversation("userId1", conv)
            if clear_conv_result and clear_conv_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("clear conversation success")
            else:
                logger.info("clear conversation failure")
            
            # 清空用户消息
            clear_user_msg_result = MessageAdmin.clear_user_messages(
                "userId1", conv, 0, int(time.time() * 1000)
            )
            if clear_user_msg_result and clear_user_msg_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("clear user messages success")
            else:
                logger.info("clear user messages failure")
        
        multicast_receivers = ["user2", "user3", "user4"]
        result_multicast_message = MessageAdmin.multicast_message("user1", multicast_receivers, 0, payload)
        if result_multicast_message and result_multicast_message.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info(f"multi message success, messageid is {result_multicast_message.result.messageUid}")
        else:
            logger.info("multi message failure")
            sys.exit(-1)
        
        void_im_result = MessageAdmin.recall_multicast_message(
            "user1", result_multicast_message.result.messageUid, multicast_receivers
        )
        if void_im_result and void_im_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("recall multicast message success")
        else:
            logger.info("recall multicast message failure")
            sys.exit(-1)
        
        # 测试删除多播消息
        delete_multi_cast_result = MessageAdmin.delete_multicast_message(
            "user1", result_multicast_message.result.messageUid, multicast_receivers
        )
        if delete_multi_cast_result and delete_multi_cast_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("delete multicast message success")
        else:
            logger.info("delete multicast message failure")
    
    def test_message_content(self):
        """消息内容编码测试"""
        sender = "userId2"
        conversation = Conversation()
        conversation.target = "3ygqmws2k"
        conversation.type = ConversationType.ConversationType_Private
        
        # 测试发送文本消息
        text_message_content = TextMessageContent("测试文本消息")
        payload = text_message_content.encode()
        result_send_message = MessageAdmin.send_message(sender, conversation, payload, None)
        self._check_send_message_result(result_send_message)
        
        # 测试发送语音消息
        sound_message_content = SoundMessageContent()
        sound_message_content.duration(7)
        sound_message_content.remote_media_url("https://media.wfcoss.cn/firechat/voice_message_sample.amr")
        payload = sound_message_content.encode()
        result_send_message = MessageAdmin.send_message(sender, conversation, payload, None)
        self._check_send_message_result(result_send_message)
        
        # 测试发送图片消息
        image_message_content = ImageMessageContent()
        # 这里省略了base64缩略图的处理
        image_message_content.remote_media_url("https://media.wfcoss.cn/firechat/image_message_sample.jpg")
        payload = image_message_content.encode()
        result_send_message = MessageAdmin.send_message(sender, conversation, payload, None)
        self._check_send_message_result(result_send_message)
        
        # 测试发送文件消息
        file_message_content = FileMessageContent()
        file_message_content.name("野火产品简介.pptx")
        file_message_content.size(38394)
        file_message_content.remote_media_url("https://media.wfcoss.cn/firechat/file_message_sample.pptx")
        payload = file_message_content.encode()
        result_send_message = MessageAdmin.send_message(sender, conversation, payload, None)
        self._check_send_message_result(result_send_message)
        
        # 测试发送链接消息
        link_message_content = LinkMessageContent()
        link_message_content.title("野火IM开发手册")
        link_message_content.url("https://docs.wildfirechat.cn")
        link_message_content.thumbnail_url("https://docs.wildfirechat.cn/favicon.ico")
        link_message_content.content_digest("野火IM开发手册，关于野火的所有知识都在这里！")
        payload = link_message_content.encode()
        result_send_message = MessageAdmin.send_message(sender, conversation, payload, None)
        self._check_send_message_result(result_send_message)
        
        # 测试发送名片消息
        card_message_content = CardMessageContent()
        card_message_content.type(0)  # 类型：0，用户
        card_message_content.target("FireRobot")
        card_message_content.name("FireRobot")
        card_message_content.portrait("https://cdn2.wildfirechat.net/robot.png")
        card_message_content.display_name("小火")
        card_message_content.from_user(sender)
        payload = card_message_content.encode()
        result_send_message = MessageAdmin.send_message(sender, conversation, payload, None)
        self._check_send_message_result(result_send_message)
        
        # 测试发送提醒消息
        tip_notification_message_content = TipNotificationMessageContent("这是一个提醒小灰条消息")
        payload = tip_notification_message_content.encode()
        result_send_message = MessageAdmin.send_message(sender, conversation, payload, None)
        self._check_send_message_result(result_send_message)
        
        # 测试富通知消息
        rich_notification_message_content = RichNotificationMessageContent(
            "产品审核通知", "您好，您的SSL证书以审核通过并成功办理，请关注", "https://www.wildfirechat.cn"
        )
        rich_notification_message_content.remark("谢谢惠顾")
        rich_notification_message_content.ex_name("证书小助手")
        rich_notification_message_content.app_id("1234567890")
        rich_notification_message_content.add_item("登陆账户", "野火IM", "#173177")
        rich_notification_message_content.add_item("产品名称", "域名wildifrechat.cn申请的免费SSL证书", "#173177")
        rich_notification_message_content.add_item("审核通过", "通过", "#173177")
        rich_notification_message_content.add_item("说明", "请登陆账户查看处理", "#173177")
        payload = rich_notification_message_content.encode()
        result_send_message = MessageAdmin.send_message(sender, conversation, payload, None)
        self._check_send_message_result(result_send_message)
        
        # 测试流式文本消息
        self.test_streaming_text(sender, conversation)
    
    def test_streaming_text(self, sender: str, conversation: Conversation):
        """
        流式文本消息测试
        
        演示如何发送流式文本消息，模拟AI逐字生成效果：
        - 将长文本分段发送
        - 使用StreamTextGeneratingMessageContent表示正在生成
        - 使用StreamTextGeneratedMessageContent表示生成完成
        """
        # 准备要发送的长文本
        full_text = """北京野火无限网络科技有限公司是成立于2019年底的一家科技创新企业，公司的主要目标是为广大企业和单位提供优质可控、私有部署的即时通讯和实时音视频能力，为社会信息化水平提高作出自己的贡献。

野火IM是公司研发一套自主可控的即时通讯组件，具有全部私有化、功能齐全、协议稳定可靠、全平台支持、安全性高和支持国产化等技术特点。客户端分层设计，既可开箱即用，也可与现有系统深度融合。具有完善的服务端API和自定义消息功能，可以任意扩展功能。代码开源率高，方便二次开发和使用。支持多人实时音视频和会议功能，线上沟通更通畅。

公司致力于开源项目，在Github上开源项目广受好评，其中Server项目有超过7.1K个Star，组织合计Star超过1万个。有大量的技术公司受益于我们的开源，为自己的产品添加了即时通讯能力，这也算是我们公司为社会信息化建设做出的一点点贡献吧。

公司以即时通讯技术为核心，持续努力优化和完善即时通讯和实时音视频产品，努力为客户提供最优质的即时通讯和实时音视频能力。"""
        
        i = 0
        stream_id = str(uuid.uuid4())
        while i < len(full_text):
            i += 15
            finish = i >= len(full_text)
            part_text = full_text if finish else full_text[:i]
            
            if finish:
                message_content = StreamTextGeneratedMessageContent(part_text, stream_id)
            else:
                message_content = StreamTextGeneratingMessageContent(part_text, stream_id)
            
            # 消息转成Payload并发送
            payload = message_content.encode()
            result_send_message = MessageAdmin.send_message(sender, conversation, payload, None)
            if result_send_message and result_send_message.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("send message success")
            else:
                logger.info("send message failure")
                sys.exit(-1)
            
            time.sleep(0.5)
    
    def _check_send_message_result(self, result_send_message):
        """检查消息发送结果"""
        if result_send_message and result_send_message.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("send message success")
        else:
            logger.info("send message failure")
            sys.exit(-1)
    
    def test_chatroom(self):
        """聊天室管理API测试"""
        chatroom_id = "chatroomId1"
        chatroom_title = "TESTCHATROM"
        chatroom_desc = "this is a test chatroom"
        chatroom_portrait = "http://pic.com/test123.png"
        chatroom_extra = "{'managers:[\"user1\",\"user2\"]}"
        
        chatroom_result = ChatroomAdmin.create_chatroom(
            chatroom_id, chatroom_title, chatroom_desc, chatroom_portrait, chatroom_extra, 0
        )
        if (chatroom_result and 
            chatroom_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS and
            chatroom_result.result.chatroomId == chatroom_id):
            logger.info("create chatroom success")
        else:
            logger.info("create chatroom failure")
            sys.exit(-1)
        
        get_chatroom_info_result = ChatroomAdmin.get_chatroom_info(chatroom_id)
        if get_chatroom_info_result and get_chatroom_info_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            result = get_chatroom_info_result.result
            if (result.chatroomId == chatroom_id and
                result.title == chatroom_title and
                result.desc == chatroom_desc and
                result.portrait == chatroom_portrait and
                result.extra == chatroom_extra):
                logger.info("chatroom info correct")
            else:
                logger.info("chatroom info incorrect")
                sys.exit(-1)
        else:
            logger.info("get chatroom info failure")
            sys.exit(-1)
        
        member_list = ChatroomAdmin.get_chatroom_members(chatroom_id)
        if member_list and member_list.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("get chatroom member success")
        else:
            logger.info(f"get chatroom member failure: {member_list.get_error_code().msg}")
        
        void_im_result = ChatroomAdmin.destroy_chatroom(chatroom_id)
        if void_im_result and void_im_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("destroy chatroom done!")
        else:
            logger.info("destroy chatroom failure")
            sys.exit(-1)
        
        time.sleep(1)
        get_chatroom_info_result = ChatroomAdmin.get_chatroom_info(chatroom_id)
        if (get_chatroom_info_result and 
            get_chatroom_info_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS and
            get_chatroom_info_result.result.state == 2):  # Chatroom_State_End = 2
            logger.info("chatroom destroyed!")
        else:
            logger.info("chatroom not destroyed!")
            sys.exit(-1)
        
        user_chatroom_result = ChatroomAdmin.get_user_chatroom("userId1")
        if (user_chatroom_result and 
            (user_chatroom_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS or
             user_chatroom_result.get_error_code() == ErrorCode.ERROR_CODE_NOT_EXIST)):
            logger.info("get user chatroom success")
        else:
            logger.info("get user chatroom failure")
            sys.exit(-1)
        
        # 测试设置聊天室全局禁言
        set_chatroom_mute_result = ChatroomAdmin.set_chatroom_mute(chatroom_id, True)
        if set_chatroom_mute_result and set_chatroom_mute_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("set chatroom mute success")
        else:
            logger.info("set chatroom mute failure")
            sys.exit(-1)
        
        # 取消聊天室全局禁言
        set_chatroom_mute_result = ChatroomAdmin.set_chatroom_mute(chatroom_id, False)
        if set_chatroom_mute_result and set_chatroom_mute_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("cancel chatroom mute success")
        else:
            logger.info("cancel chatroom mute failure")
            sys.exit(-1)
        
        # 商业版功能：聊天室黑名单/管理员管理
        if self.commercial_server:
            # 设置用户聊天室黑名单：0正常；1禁言；2禁止加入
            set_blacklist_result = ChatroomAdmin.set_chatroom_blacklist("chatroom1", "userId1", 1)
            if set_blacklist_result and set_blacklist_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("add chatroom black success")
            else:
                logger.info("add chatroom black failure")
                sys.exit(-1)
            
            # 获取聊天室黑名单
            blacklist_result = ChatroomAdmin.get_chatroom_blacklist("chatroom1")
            if blacklist_result and blacklist_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("get chatroom blacklist success")
            else:
                logger.info("get chatroom blacklist failure")
                sys.exit(-1)
            
            # 取消用户聊天室黑名单
            set_blacklist_result = ChatroomAdmin.set_chatroom_blacklist("chatroom1", "userId1", 0)
            if set_blacklist_result and set_blacklist_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("remove chatroom black success")
            else:
                logger.info("remove chatroom black failure")
                sys.exit(-1)
            
            # 设置聊天室管理员
            set_manager_result = ChatroomAdmin.set_chatroom_manager("chatroom1", "userId1", 1)
            if set_manager_result and set_manager_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("add chatroom manager success")
            else:
                logger.info("add chatroom manager failure")
                sys.exit(-1)
            
            # 获取聊天室管理员列表
            managers_result = ChatroomAdmin.get_chatroom_manager_list("chatroom1")
            if managers_result and managers_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("get chatroom manager list success")
            else:
                logger.info("get chatroom manager list failure")
                sys.exit(-1)
            
            # 取消聊天室管理员
            set_manager_result = ChatroomAdmin.set_chatroom_manager("chatroom1", "userId1", 0)
            if set_manager_result and set_manager_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("remove chatroom manager success")
            else:
                logger.info("remove chatroom manager failure")
                sys.exit(-1)
    
    def test_channel_api(self):
        """频道管理API测试"""
        channel_name = "MyChannel"
        channel_owner = "user1"
        input_create_channel = InputCreateChannel()
        input_create_channel.name = channel_name
        input_create_channel.owner = channel_owner
        
        result_create_channel = ChannelAdmin.create_channel(input_create_channel)
        if result_create_channel and result_create_channel.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("create channel success")
            input_create_channel.targetId = result_create_channel.result.targetId
        else:
            logger.info("create channel failure")
            sys.exit(-1)
        
        result_get_channel = ChannelAdmin.get_channel_info(input_create_channel.targetId)
        if (result_get_channel and 
            result_get_channel.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS and
            result_get_channel.result.name == channel_name and
            result_get_channel.result.owner == channel_owner):
            logger.info("get channel success")
        else:
            logger.info("get channel failure")
            sys.exit(-1)
        
        subscriber = "aaa"
        void_im_result = ChannelAdmin.subscribe_channel(input_create_channel.targetId, subscriber)
        if void_im_result and void_im_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("subscribeChannel success")
        else:
            logger.info("subscriber channel failure")
            sys.exit(-1)
        
        time.sleep(0.1)
        boolean_result = ChannelAdmin.is_user_subscribed_channel(subscriber, input_create_channel.targetId)
        if (boolean_result and 
            boolean_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS and
            boolean_result.result.value):
            logger.info("subscribe status is correct")
        else:
            logger.info("subscribe status is incorrect")
            sys.exit(-1)
        
        void_im_result = ChannelAdmin.unsubscribe_channel(input_create_channel.targetId, subscriber)
        if void_im_result and void_im_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("unsubscribeChannel success")
        else:
            logger.info("unsubscriber channel failure")
            sys.exit(-1)
        
        time.sleep(0.1)
        boolean_result = ChannelAdmin.is_user_subscribed_channel(subscriber, input_create_channel.targetId)
        if (boolean_result and 
            boolean_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS and
            not boolean_result.result.value):
            logger.info("subscribe status is correct")
        else:
            logger.info("subscribe status is incorrect")
            sys.exit(-1)
        
        void_im_result = ChannelAdmin.destroy_channel(input_create_channel.targetId)
        if void_im_result and void_im_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("destroy channel success")
        else:
            logger.info("destroy channel failure")
            sys.exit(-1)
        
        result_get_channel = ChannelAdmin.get_channel_info(input_create_channel.targetId)
        if (result_get_channel and 
            result_get_channel.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS and
            (result_get_channel.result.state & 0x40) > 0):  # Channel_State_Mask_Deleted = 0x40
            logger.info("channel destroyed verified")
        else:
            logger.info("get channel failure")
            sys.exit(-1)
    
    def test_general_api(self):
        """通用API测试"""
        result_get_system_setting = GeneralAdmin.get_system_setting(SystemSettingType.Group_Max_Member_Count)
        if result_get_system_setting and result_get_system_setting.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("get system setting success")
        else:
            logger.info("get system setting failure")
            sys.exit(-1)
        
        result_set_system_setting = GeneralAdmin.set_system_setting(
            SystemSettingType.Group_Max_Member_Count, "2000", "最大群人数为2000"
        )
        if result_set_system_setting and result_set_system_setting.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("set system setting success")
        else:
            logger.info("set system setting failure")
            sys.exit(-1)
        
        result_get_system_setting = GeneralAdmin.get_system_setting(SystemSettingType.Group_Max_Member_Count)
        if (result_get_system_setting and 
            result_get_system_setting.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS and
            result_get_system_setting.result.value == "2000"):
            logger.info("get system setting success")
        else:
            logger.info("get system setting failure")
            sys.exit(-1)

        health = GeneralAdmin.health_check()
        if health and health.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info(f"health check success: {health.result}")
        else:
            logger.info("health check failure")
            sys.exit(-1)
        
        # 测试用户设置功能
        set_user_setting_result = GeneralAdmin.set_user_setting("user1", 1, "test_key", "test_value")
        if set_user_setting_result and set_user_setting_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("set user setting success")
        else:
            logger.info("set user setting failure")
            sys.exit(-1)

        time.sleep(1)
        get_user_setting_result = GeneralAdmin.get_user_setting("user1", 1, "test_key")
        if (get_user_setting_result and 
            get_user_setting_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS and
            get_user_setting_result.result.value == "test_value"):
            logger.info("get user setting success")
        else:
            logger.info("get user setting failure")
            sys.exit(-1)
        
        if self.commercial_server:
            # 测试会话置顶功能
            set_top_result = GeneralAdmin.set_conversation_top(
                "user1", ConversationType.ConversationType_Private, "user2", 0, True
            )
            if set_top_result and set_top_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("set conversation top success")
            else:
                logger.info("set conversation top failure")
                sys.exit(-1)
            
            time.sleep(1)
            get_top_result = GeneralAdmin.get_conversation_top(
                "user1", ConversationType.ConversationType_Private, "user2", 0
            )
            if get_top_result and get_top_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS and get_top_result.result:
                logger.info("get conversation top success")
            else:
                logger.info("get conversation top failure")
                sys.exit(-1)
            
            # 取消置顶
            set_top_result = GeneralAdmin.set_conversation_top(
                "user1", ConversationType.ConversationType_Private, "user2", 0, False
            )
            if set_top_result and set_top_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("cancel conversation top success")
            else:
                logger.info("cancel conversation top failure")
                sys.exit(-1)
            
            # 测试获取会话文件
            conv_files_result = GeneralAdmin.get_conversation_files(
                ConversationType.ConversationType_Private, "user2", 0, "user1", 0, True, 10
            )
            if conv_files_result and conv_files_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("get conversation files success")
            else:
                logger.info("get conversation files failure")
            
            # 测试获取用户文件
            user_files_result = GeneralAdmin.get_user_files("user1", 0, True, 10)
            if user_files_result and user_files_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("get user files success")
            else:
                logger.info("get user files failure")
            
            # 测试获取单个文件信息
            if (user_files_result.result and user_files_result.result.files and 
                len(user_files_result.result.files) > 0):
                message_id = user_files_result.result.files[0].messageId
                file_result = GeneralAdmin.get_file(message_id)
                if file_result and file_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                    logger.info("get file success")
                else:
                    logger.info("get file failure")
    
    def test_sensitive_api(self):
        """敏感词API测试"""
        words = ["a", "b", "c"]
        
        # 添加敏感词
        add_result = SensitiveAdmin.add_sensitive_words(words)
        if add_result and add_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("add sensitive words success")
        else:
            logger.info("add sensitive words failure")
            sys.exit(-1)
        
        time.sleep(0.1)
        
        # 获取敏感词列表
        query_result = SensitiveAdmin.get_sensitive_words()
        if (query_result and query_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS and
            all(word in query_result.result.words for word in words)):
            logger.info("sensitive word added")
        else:
            logger.info("sensitive word not added")
            sys.exit(-1)
        
        # 删除敏感词
        remove_result = SensitiveAdmin.remove_sensitive_words(words)
        if remove_result and remove_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("remove sensitive words success")
        else:
            logger.info("remove sensitive words failure")
            sys.exit(-1)
        
        time.sleep(0.1)
        
        # 验证敏感词已删除
        query_result = SensitiveAdmin.get_sensitive_words()
        if (query_result and query_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS and
            not any(word in query_result.result.words for word in words)):
            logger.info("sensitive word removed")
        else:
            logger.info("sensitive word not removed")
            sys.exit(-1)
    
    def test_device(self):
        """设备管理API测试（仅商业版）"""
        # 创建设备
        from wildfirechat.models import InputCreateDevice
        device = InputCreateDevice()
        device.deviceId = "device1"
        device.name = "测试设备"
        device.extra = "设备额外信息"
        
        result = UserAdmin.create_or_update_device(device)
        if result and result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("create device success")
        else:
            logger.info("create device failure")
            # 不退出，因为设备可能已经存在
        
        # 获取设备信息
        result = UserAdmin.get_device("device1")
        if result and result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("get device success")
        else:
            logger.info("get device failure")
            # 不退出
    
    def test_conference(self):
        """会议管理API测试（仅高级音视频版）"""
        # 获取会议列表
        list_result = ConferenceAdmin.list_conferences(count=100, offset=0)
        if list_result and list_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("conference list success")
        else:
            logger.info("get conference list failure")
            sys.exit(-1)
        
        # 清理现有会议
        if list_result.result and list_result.result.conferenceInfoList:
            for conference_info in list_result.result.conferenceInfoList:
                # 支持不同的字段名
                room_id = getattr(conference_info, 'roomId', None) or getattr(conference_info, 'conferenceId', '')
                if room_id:
                    destroy_result = ConferenceAdmin.destroy_conference(room_id)
                    if destroy_result and destroy_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                        logger.info("destroy room success")
                    else:
                        logger.info("destroy room skipped (may be in use or not exist)")
                        # 不退出，因为会议可能正在被使用
        
        # 再次获取会议列表
        list_result = ConferenceAdmin.list_conferences(count=100, offset=0)
        if list_result and list_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("conference list success")
        else:
            logger.info("get conference list failure")
            sys.exit(-1)
        
        # 生成会议房间ID
        import uuid
        room_id1 = str(uuid.uuid4())
        room_id2 = str(uuid.uuid4())
        
        # 创建普通会议房间
        create_result = ConferenceAdmin.create_conference(
            room_id1, "hello room description", "123456", advance=False, recording=False
        )
        if create_result and create_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("create conference success")
        else:
            logger.info("create conference skipped (server may not support)")
            # 不退出，继续其他测试
            return
        
        # 创建高级会议房间
        create_result = ConferenceAdmin.create_conference(
            room_id2, "hello room description advanced", "123456", advance=True, recording=False
        )
        if create_result and create_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("create conference success")
        else:
            logger.info("create conference skipped (server may not support)")
            # 不退出，继续其他测试
            return
        
        # 检查会议是否存在
        exist_result = ConferenceAdmin.check_conference_exist(room_id1)
        if exist_result and exist_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("exist conference success")
        else:
            logger.info("exist conference skipped")
        
        # 开启会议录制
        recording_result = ConferenceAdmin.set_recording(room_id2, True)
        if recording_result and recording_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("recording conference success")
        else:
            logger.info("recording conference skipped")
        
        # 获取会议列表
        list_result = ConferenceAdmin.list_conferences(count=100, offset=0)
        if list_result and list_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("conference list success")
        else:
            logger.info("get conference list failure")
            return
        
        # 获取参会者列表
        if list_result.result and list_result.result.conferenceInfoList:
            for conference_info in list_result.result.conferenceInfoList:
                room_id = getattr(conference_info, 'roomId', None) or getattr(conference_info, 'conferenceId', '')
                if room_id:
                    participants_result = ConferenceAdmin.list_participants(room_id)
                    if participants_result and participants_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                        logger.info("list participants success")
                    else:
                        logger.info("list participants skipped")
        
        # 获取RTP转发器列表 - 使用存在的会议ID
        rtp_room_id = room_id1 if room_id1 else room_id2
        rtp_result = ConferenceAdmin.list_rtp_forward(rtp_room_id)
        if rtp_result and rtp_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("list rtp forward success")
            # 停止所有转发器
            if rtp_result.result and rtp_result.result.forwarders:
                for forwarder in rtp_result.result.forwarders:
                    if forwarder.streams:
                        for stream in forwarder.streams:
                            stop_result = ConferenceAdmin.stop_rtp_forward(
                                rtp_room_id, stream.streamId
                            )
                            if stop_result and stop_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                                logger.info("stop rtp forward success")
                            else:
                                logger.info("stop rtp forward skipped")
        else:
            # 可能没有这个会议或没有转发器，不退出
            logger.info("list rtp forward skipped")
    
    def test_moments_api(self):
        """朋友圈API测试"""
        feed_pojo = {
            "sender": "userId1",
            "type": 0,  # 文本类型
            "text": "hello from admin"
        }
        send_result = MomentsAdmin.post_feeds(feed_pojo)
        if send_result and send_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("send moments feed success")
        else:
            logger.info("send moments feed failure")
            sys.exit(-1)
    
    def test_robot(self):
        """机器人功能测试"""
        robot_id = "robot1"
        robot_secret = "123456"
        
        # 初始化服务API
        AdminConfig.init_admin(self.admin_url, self.admin_secret)
        
        # 创建机器人
        create_robot = InputCreateRobot()
        create_robot.userId = robot_id
        create_robot.name = robot_id
        create_robot.displayName = "机器人"
        create_robot.owner = "userId1"
        create_robot.secret = robot_secret
        create_robot.callback = "http://127.0.0.1:8883/robot/recvmsg"
        
        result_create_robot = UserAdmin.create_robot(create_robot)
        if result_create_robot and result_create_robot.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info(f"Create robot {result_create_robot.result.userId} success")
        else:
            logger.info("Create robot failure")
            # 不退出，因为机器人可能已经存在
        
        # 使用完需要释放
        robot_service = RobotService(self.im_url, robot_id, robot_secret)
        
        # 获取机器人资料
        robot_profile_result = robot_service.get_profile()
        if robot_profile_result and robot_profile_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("get robot profile success")
        else:
            logger.info("get robot profile failure")
            sys.exit(-1)
        
        # 更新机器人资料
        display_name = f"testrobot{int(time.time() * 1000)}"
        update_profile_result = robot_service.update_profile(MyInfoType.Modify_DisplayName, display_name)
        if update_profile_result and update_profile_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("modify profile success")
        else:
            logger.info("modify profile failure")
            sys.exit(-1)

        time.sleep(1)
        # 验证更新成功
        robot_profile_result = robot_service.get_profile()
        if (robot_profile_result and 
            robot_profile_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS and
            robot_profile_result.result.displayName == display_name):
            logger.info("get profile success")
        else:
            logger.info("get profile failure")
            sys.exit(-1)
        
        # 设置机器人回调地址
        robot_callback = "http://hellow123"
        set_callback_result = robot_service.set_callback(robot_callback)
        if set_callback_result and set_callback_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("set callback success")
        else:
            logger.info("set callback failure")
            sys.exit(-1)
        
        # 获取机器人回调地址
        get_callback_result = robot_service.get_callback()
        if (get_callback_result and 
            get_callback_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS and
            get_callback_result.result.url == robot_callback):
            logger.info("get callback success")
        else:
            logger.info("get callback failure")
            sys.exit(-1)
        
        # 删除机器人回调地址
        delete_callback_result = robot_service.delete_callback()
        if delete_callback_result and delete_callback_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("delete callback success")
        else:
            logger.info("delete callback failure")
            sys.exit(-1)
        
        # 验证回调地址已删除
        get_callback_result = robot_service.get_callback()
        if (get_callback_result and 
            get_callback_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS and
            not get_callback_result.result.url):
            logger.info("get callback success")
        else:
            logger.info("get callback failure")
            sys.exit(-1)
        
        # 创建会话对象
        conversation = Conversation()
        conversation.target = "user2"
        conversation.type = ConversationType.ConversationType_Private
        
        # 创建消息payload
        payload = MessagePayload()
        payload.type = 1
        payload.searchableContent = "hello world"
        
        # 测试机器人发送消息
        result_robot_send_message = robot_service.send_message(conversation.to_dict(), payload.to_dict())
        if result_robot_send_message and result_robot_send_message.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("robot send message success")
        else:
            logger.info("robot send message failure")
            sys.exit(-1)
        
        # 测试机器人回复消息
        reply_result = robot_service.reply_message(
            result_robot_send_message.result.messageUid, payload.to_dict(), False
        )
        if reply_result and reply_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("robot reply message success")
        else:
            logger.info("robot reply message failure")
            # 不退出，因为某些服务器可能不支持
        
        # 测试通过手机号获取用户信息
        result_get_user_by_mobile = robot_service.get_user_info_by_mobile("13900000000")
        if result_get_user_by_mobile and result_get_user_by_mobile.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("robot get user info by mobile success")
        else:
            logger.info("robot get user info by mobile failure")
            # 不退出
        
        # 测试通过用户名获取用户信息
        result_get_user_by_name = robot_service.get_user_info_by_name("user1")
        if result_get_user_by_name and result_get_user_by_name.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("robot get user info by name success")
        else:
            logger.info("robot get user info by name failure")
            # 不退出
        
        # 商业版功能
        if self.commercial_server:
            time.sleep(1)
            # 撤回消息
            recall_result = robot_service.recall_message(result_robot_send_message.result.messageUid)
            if recall_result and recall_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("robot recall message success")
            else:
                logger.info("robot recall message failure")
                sys.exit(-1)
            
            # 更新消息
            payload.searchableContent = "hello world, updated message content"
            result_robot_send_message = robot_service.send_message(conversation.to_dict(), payload.to_dict())
            if result_robot_send_message and result_robot_send_message.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("robot send message success")
            else:
                logger.info("robot send message failure")
                sys.exit(-1)
            
            time.sleep(1)
            update_result = robot_service.update_message(result_robot_send_message.result.messageUid, payload.to_dict())
            if update_result and update_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("robot update message success")
            else:
                logger.info("robot update message failure")
                sys.exit(-1)
            
            # 测试获取应用签名
            config_result = robot_service.get_application_signature()
            if config_result:
                logger.info(f"get application signature: {config_result.result}")
            else:
                logger.info("get application signature skipped")
        
        # 测试获取用户信息
        result_get_user_info = robot_service.get_user_info("userId1")
        if result_get_user_info and result_get_user_info.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("robot get user info success")
        else:
            logger.info("robot get user info by userId failure")
            sys.exit(-1)
        
        # 测试机器人群组管理
        group_id = f"robot_group{int(time.time() * 1000)}"
        group_info = {
            "target_id": group_id,
            "name": "test_group",
            "type": 2,
            "extra": "hello extra",
            "portrait": "http://portrait"
        }
        
        members = [
            {"member_id": "user1"},
            {"member_id": "user2"},
            {"member_id": "user3"}
        ]
        
        # 创建群组
        result_create_group = robot_service.create_group(group_info, members)
        if result_create_group and result_create_group.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("create group success")
        else:
            logger.info("create group failure")
            sys.exit(-1)
        
        # 获取群组信息
        result_get_group_info = robot_service.get_group_info(group_id)
        if result_get_group_info and result_get_group_info.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("get group success")
        else:
            logger.info("get group failure")
            sys.exit(-1)
        
        # 修改群组信息
        modify_result = robot_service.modify_group_info(group_id, ModifyGroupInfoType.Modify_Group_Name, "HelloWorld")
        if modify_result and modify_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("modify group success")
        else:
            logger.info("modify group failure")
            sys.exit(-1)
        
        # 获取群组成员
        result_get_members = robot_service.get_group_members(group_id)
        if result_get_members and result_get_members.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("get group member success")
        else:
            logger.info("get group member failure")
            sys.exit(-1)
        
        # 添加群成员
        new_member = {"member_id": "user0", "alias": "hello user0"}
        add_result = robot_service.add_group_members(group_id, [new_member])
        if add_result and add_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("add group member success")
        else:
            logger.info("add group member failure")
            sys.exit(-1)
        
        # 踢出群成员
        kickoff_result = robot_service.kickoff_group_members(group_id, ["user3"])
        if kickoff_result and kickoff_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("kickoff group member success")
        else:
            logger.info("kickoff group member failure")
            sys.exit(-1)
        
        # 设置群成员别名
        alias_result = robot_service.set_group_member_alias(group_id, "user2", "test user2")
        if alias_result and alias_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("set group member alias success")
        else:
            logger.info("set group member alias failure")
            sys.exit(-1)
        
        # 设置群成员extra
        extra_result = robot_service.set_group_member_extra(group_id, "user2", "robot member extra")
        if extra_result and extra_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("set group member extra success")
        else:
            logger.info("set group member extra failure")
            sys.exit(-1)
        
        # 商业版功能
        if self.commercial_server:
            # 设置群管理员
            manager_result = robot_service.set_group_manager(group_id, ["user2", "user0"], True)
            if manager_result and manager_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("set group manager success")
            else:
                logger.info("set group manager failure")
                sys.exit(-1)
            
            # 取消群管理员
            manager_result = robot_service.set_group_manager(group_id, ["user2", "user0"], False)
            if manager_result and manager_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("cancel group manager success")
            else:
                logger.info("cancel group manager failure")
                sys.exit(-1)
            
            # 禁言群成员
            mute_result = robot_service.mute_group_member(group_id, ["user5"], True)
            if mute_result and mute_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("mute group member success")
            else:
                logger.info("mute group member failure")
                sys.exit(-1)
            
            # 取消禁言
            mute_result = robot_service.mute_group_member(group_id, ["user5"], False)
            if mute_result and mute_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("unmute group member success")
            else:
                logger.info("unmute group member failure")
                sys.exit(-1)
            
            # 允许群成员发言（白名单）
            allow_result = robot_service.allow_group_member(group_id, ["user5"], True)
            if allow_result and allow_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("allow group member success")
            else:
                logger.info("allow group member failure")
                sys.exit(-1)
            
            # 取消允许
            allow_result = robot_service.allow_group_member(group_id, ["user5"], False)
            if allow_result and allow_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("unallow group member success")
            else:
                logger.info("unallow group member failure")
                sys.exit(-1)
        
        # 转让群组
        transfer_result = robot_service.transfer_group(group_id, "user2")
        if transfer_result and transfer_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("transfer success")
        else:
            logger.info("transfer failure")
            sys.exit(-1)

        time.sleep(1)
        # 验证转让成功
        result_get_group_info = robot_service.get_group_info(group_id)
        if (result_get_group_info and 
            result_get_group_info.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS and
            result_get_group_info.result.owner == "user2"):
            logger.info("get group success")
        else:
            logger.info("get group failure")
            sys.exit(-1)
        
        # 退出群组
        quit_result = robot_service.quit_group(group_id)
        if quit_result and quit_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("quit group success")
        else:
            logger.info("quit group failure")
            sys.exit(-1)
        
        # 测试机器人朋友圈功能
        if self.robot_moments_enabled:
            logger.info("开始测试机器人朋友圈功能...")
            
            # 发布文本动态
            feed_result = robot_service.post_moments_feed(
                feed_type=0,  # 文本
                text="hello from robot",
                to_users=["userId1", "userId2"],
                extra="hello_extra"
            )
            if feed_result and feed_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("post moments feed success")
                feed_id = feed_result.result.get("feedId", 0) if feed_result.result else 0
            else:
                logger.info("post moments feed failure")
                sys.exit(-1)
            
            # 获取动态列表
            feeds_result = robot_service.get_moments_feeds(count=10)
            if feeds_result and feeds_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("pull moments feeds success")
            else:
                logger.info("pull moments feeds failure")
                sys.exit(-1)
            
            # 获取单条动态
            if feed_id > 0:
                single_feed_result = robot_service.get_moments_feed(feed_id)
                if single_feed_result and single_feed_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                    logger.info("pull moments one feed success")
                else:
                    logger.info("pull moments one feed failure")
                    sys.exit(-1)
                
                # 发布点赞
                thumb_up_result = robot_service.post_moments_comment(
                    feed_id=feed_id,
                    comment_type=1,  # 点赞
                    text=""
                )
                if thumb_up_result and thumb_up_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                    logger.info("post moments thumb up success")
                    comment_id_thumb = thumb_up_result.result.get("commentId", 0) if thumb_up_result.result else 0
                else:
                    logger.info("post moments thumb up failure")
                    sys.exit(-1)
                
                # 发布评论
                comment_result = robot_service.post_moments_comment(
                    feed_id=feed_id,
                    comment_type=0,  # 文本评论
                    text="comment hello"
                )
                if comment_result and comment_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                    logger.info("post moments comment text success")
                    comment_id_text = comment_result.result.get("commentId", 0) if comment_result.result else 0
                else:
                    logger.info("post moments comment text failure")
                    sys.exit(-1)
                
                # 更新动态
                update_result = robot_service.update_moments_feed(
                    feed_id=feed_id,
                    feed_type=0,
                    text="hello from robot2",
                    extra="hello_extra2"
                )
                if update_result and update_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                    logger.info("update moments feed success")
                else:
                    logger.info("update moments feed failure")
                    sys.exit(-1)
                
                # 删除点赞
                if comment_id_thumb > 0:
                    delete_thumb_result = robot_service.delete_moments_comment(feed_id, comment_id_thumb)
                    if delete_thumb_result and delete_thumb_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                        logger.info("delete moments thumb up success")
                    else:
                        logger.info("delete moments thumb up failure")
                        sys.exit(-1)
                
                # 删除评论
                if comment_id_text > 0:
                    delete_comment_result = robot_service.delete_moments_comment(feed_id, comment_id_text)
                    if delete_comment_result and delete_comment_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                        logger.info("delete moments comment text success")
                    else:
                        logger.info("delete moments comment text failure")
                        sys.exit(-1)
                
                # 删除动态
                delete_result = robot_service.delete_moments_feed(feed_id)
                if delete_result and delete_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                    logger.info("delete moments feed success")
                else:
                    logger.info("delete moments feed failure")
                    sys.exit(-1)
            
            # 获取用户朋友圈资料
            profile_result = robot_service.get_user_moments_profile(robot_id)
            if profile_result and profile_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("get user moments profile success")
            else:
                logger.info("get user moments profile failure")
                sys.exit(-1)
            
            # 更新朋友圈背景
            bg_result = robot_service.update_moments_background_url("https://example.com/bg.jpg")
            if bg_result and bg_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("update moments background success")
            else:
                logger.info("update moments background failure")
                # 不退出
            
            # 更新陌生人可见数量
            visible_count_result = robot_service.update_moments_stranger_visible_count(10)
            if visible_count_result and visible_count_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("update moments visible count success")
            else:
                logger.info("update moments visible count failure")
                # 不退出
            
            # 更新可见范围
            visible_scope_result = robot_service.update_moments_visible_scope(0)
            if visible_scope_result and visible_scope_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("update moments visible scope success")
            else:
                logger.info("update moments visible scope failure")
                # 不退出
            
            # 更新黑名单
            blacklist_result = robot_service.update_moments_black_list(add_list=["user1"])
            if blacklist_result and blacklist_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("update moments blacklist success")
            else:
                logger.info("update moments blacklist failure")
                # 不退出
            
            # 更新屏蔽列表
            blocklist_result = robot_service.update_moments_block_list(add_list=["user2"])
            if blocklist_result and blocklist_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
                logger.info("update moments blocklist success")
            else:
                logger.info("update moments blocklist failure")
                # 不退出
            
            logger.info("机器人朋友圈功能测试完成")
        
        # 销毁机器人
        UserAdmin.destroy_robot(robot_id)
    
    def test_channel(self):
        """
        频道功能测试（仅专业版支持）
        
        测试以下功能：
        - 创建频道
        - 获取频道信息
        - 修改频道信息
        - 获取频道列表
        - 关注/取消关注频道
        - 获取频道关注者
        - 设置频道菜单
        - 发送频道消息
        - 获取频道历史消息
        - 获取用户关注的频道
        - 删除频道（标记为已删除）
        """
        # 初始化服务API
        AdminConfig.init_admin(self.admin_url, self.admin_secret)
        
        # 先创建3个用户
        user_info = InputOutputUserInfo()
        user_info.userId = "userId1"
        user_info.name = "user1"
        user_info.mobile = "13900000000"
        user_info.displayName = "user 1"
        
        result_create_user = UserAdmin.create_user(user_info)
        if result_create_user and result_create_user.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info(f"Create user {result_create_user.result.name} success")
        else:
            logger.info("Create user failure")
            sys.exit(-1)
        
        user_info = InputOutputUserInfo()
        user_info.userId = "userId2"
        user_info.name = "user2"
        user_info.mobile = "13900000002"
        user_info.displayName = "user 2"
        
        result_create_user = UserAdmin.create_user(user_info)
        if result_create_user and result_create_user.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info(f"Create user {result_create_user.result.name} success")
        else:
            logger.info("Create user failure")
            sys.exit(-1)
        
        user_info = InputOutputUserInfo()
        user_info.userId = "userId3"
        user_info.name = "user3"
        user_info.mobile = "13900000003"
        user_info.displayName = "user 3"
        
        result_create_user = UserAdmin.create_user(user_info)
        if result_create_user and result_create_user.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info(f"Create user {result_create_user.result.name} success")
        else:
            logger.info("Create user failure")
            sys.exit(-1)
        
        # 1. 先使用admin api创建频道
        # 先尝试销毁可能已存在的频道
        channel_id = "channelId123"
        ChannelAdmin.destroy_channel(channel_id)
        
        input_create_channel = InputCreateChannel()
        input_create_channel.name = "testChannel"
        input_create_channel.owner = "userId1"
        secret = "channelsecret"
        input_create_channel.secret = secret
        input_create_channel.targetId = channel_id
        input_create_channel.auto = 1
        input_create_channel.callback = "http://192.168.1.81:8088/wf/channelId123"
        input_create_channel.state = (ChannelState.Channel_State_Mask_FullInfo | 
                                      ChannelState.Channel_State_Mask_Unsubscribed_User_Access |
                                      ChannelState.Channel_State_Mask_Active_Subscribe |
                                      ChannelState.Channel_State_Mask_Message_Unsubscribed)
        
        result_create_channel = ChannelAdmin.create_channel(input_create_channel)
        if result_create_channel and result_create_channel.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("create channel success")
        else:
            logger.info("create channel failure")
            sys.exit(-1)
        
        # 2. 初始化api，注意端口是80，不是18080 //使用完需要释放
        channel_service_api = ChannelServiceApi(self.im_url, channel_id, secret)
        
        # 3. 测试channel api功能
        
        # 测试用户关注频道
        result_void = channel_service_api.subscribe("userId2")
        if result_void and result_void.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("subscribe success")
        else:
            logger.info("subscribe failure")
            sys.exit(-1)
        
        # 测试另一个用户关注频道
        result_void = channel_service_api.subscribe("userId3")
        if result_void and result_void.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("subscribe done")
        else:
            logger.info("subscribe failure")
            sys.exit(-1)
        
        # 使用Admin API让userId4关注频道
        result_void = ChannelAdmin.subscribe_channel(channel_id, "userId4")
        if result_void and result_void.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("subscribe done")
        else:
            logger.info("subscribe failure")
            sys.exit(-1)
        
        # 获取频道订阅者列表
        result_string_list = channel_service_api.get_subscriber_list()
        if (result_string_list and 
            result_string_list.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS and
            "userId2" in result_string_list.result.list and
            "userId3" in result_string_list.result.list and
            "userId4" in result_string_list.result.list):
            logger.info("get subscriber done")
        else:
            logger.info("get subscriber failure")
            sys.exit(-1)
        
        # 检查用户是否订阅了频道
        boolean_result = channel_service_api.is_subscriber("userId2")
        if (boolean_result and 
            boolean_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS and
            boolean_result.result):
            logger.info("is subscriber success")
        else:
            logger.info("is subscriber failure")
            sys.exit(-1)
        
        # 测试用户取消关注频道
        result_void = channel_service_api.unsubscribe("userId2")
        if result_void and result_void.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("unsubscriber done")
        else:
            logger.info("unsubscriber failure")
            sys.exit(-1)
        
        # 验证userId2已不在订阅者列表中
        result_string_list = channel_service_api.get_subscriber_list()
        if (result_string_list and 
            result_string_list.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS and
            "userId3" in result_string_list.result.list and
            "userId2" not in result_string_list.result.list):
            logger.info("get subscriber done")
        else:
            logger.info("get subscriber failure")
            sys.exit(-1)
        
        # 测试频道获取用户信息
        result_get_user_info = channel_service_api.get_user_info("userId3")
        if result_get_user_info and result_get_user_info.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("get user info success")
        else:
            logger.info("get user info failure")
            sys.exit(-1)
        
        # 创建消息payload
        payload = MessagePayload()
        payload.type = 1
        payload.searchableContent = "hello world"
        
        result_send_message = channel_service_api.send_message(0, None, payload)
        if result_send_message and result_send_message.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("send message to all the subscriber success")
        else:
            logger.info("send message to all the subscriber failure")
            sys.exit(-1)
        
        # 测试重新发布消息
        republish_result = channel_service_api.republish_message(
            result_send_message.result.messageUid, ["userId2", "userId3"]
        )
        if republish_result and republish_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("republish message success")
        else:
            logger.info("republish message failure")
            sys.exit(-1)
        
        # 测试发送文章消息
        article_content = ArticleContent(
            title="article1",
            cover="https://media.wfcoss.cn/channel-assets/20220816/2dd76540daa9444dae44e942aa1c2bbc.png",
            digest="这是一个测试文章",
            content="测试一下文章的功能",
            url="https://mp.weixin.qq.com/s/W6tanLbALd3qqZM8r3MTgA",
            is_original=True
        )
        article_content.add_sub_article(
            "article2",
            "https://media.wfcoss.cn/channel-assets/20220816/2dd76540daa9444dae44e942aa1c2bbc.png",
            "这是第二个测试文章",
            "测试一下文章的功能",
            "https://mp.weixin.qq.com/s/W6tanLbALd3qqZM8r3MTgA",
            False
        )
        article_content.add_sub_article(
            "article3",
            "https://media.wfcoss.cn/channel-assets/20220816/2dd76540daa9444dae44e942aa1c2bbc.png",
            "这是第三个测试文章",
            "测试一下文章的功能",
            "https://mp.weixin.qq.com/s/W6tanLbALd3qqZM8r3MTgA",
            False
        )
        article_payload = article_content.encode()
        result_send_message = channel_service_api.send_message(0, None, article_payload)
        if result_send_message and result_send_message.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("send article message success")
        else:
            logger.info("send article message failure")
            sys.exit(-1)
        
        # 发送定向消息给指定用户
        payload.searchableContent = "hello to user2"
        result_send_message = channel_service_api.send_message(0, ["userId2"], payload)
        if result_send_message and result_send_message.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("send message to user2 success")
        else:
            logger.info("send message to user2 failure")
            sys.exit(-1)
        
        # 测试修改频道描述信息
        void_result = channel_service_api.modify_channel_info(
            ModifyChannelInfoType.Modify_Channel_Desc, 
            f"this is a test channel, update at: {datetime.now()}"
        )
        if void_result and void_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("modify channel profile success")
        else:
            logger.info("modify channel profile failure")
            sys.exit(-1)
        
        # 测试修改频道菜单
        menus = []
        menu1 = PojoChannelMenu()
        menu1.menuId = str(uuid.uuid4())
        menu1.type = "view"
        menu1.name = "一级菜单1"
        menu1.key = "key1"
        menu1.url = "http://www.baidu.com"
        menus.append(menu1)
        
        menu2 = PojoChannelMenu()
        menu2.menuId = str(uuid.uuid4())
        menu2.type = "view"
        menu2.name = "一级菜单2"
        menu2.key = "key2"
        menu2.url = "http://www.sohu.com"
        menu2.subMenus = []
        menus.append(menu2)
        
        menu21 = PojoChannelMenu()
        menu21.menuId = str(uuid.uuid4())
        menu21.type = "click"
        menu21.name = "二级菜单21"
        menu21.key = "key21"
        menu21.url = "http://www.sohu.com"
        menu2.subMenus.append(menu21)
        
        import json
        menu_str = json.dumps([m.to_dict() for m in menus], ensure_ascii=False)
        void_result = channel_service_api.modify_channel_info(
            ModifyChannelInfoType.Modify_Channel_Menu, menu_str
        )
        if void_result and void_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("modify channel menu success")
        else:
            logger.info("modify channel menu failure")
            sys.exit(-1)
        
        # 获取频道信息
        output_get_channel_info = channel_service_api.get_channel_info()
        if output_get_channel_info and output_get_channel_info.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("get channel info success")
        else:
            logger.info("get channel info failure")
            sys.exit(-1)
        
        # 测试修改频道菜单（使用modify_channel_menu方法）
        test_menus = []
        test_menu = PojoChannelMenu()
        test_menu.menuId = str(uuid.uuid4())
        test_menu.type = "view"
        test_menu.name = "测试菜单"
        test_menu.key = "test_key"
        test_menu.url = "http://www.test.com"
        test_menus.append(test_menu)
        
        modify_menu_result = channel_service_api.modify_channel_menu(test_menus)
        if modify_menu_result and modify_menu_result.get_error_code() == ErrorCode.ERROR_CODE_SUCCESS:
            logger.info("modify channel menu success")
        else:
            logger.info("modify channel menu failure")
        
        # 获取应用签名
        config = channel_service_api.get_application_signature()
        logger.info(f"Config: {config}")
        
        # 使用完需要释放
        # channel_service_api.close()  # Python版本没有close方法
    
    def test_message_sharding(self):
        """消息分表计算测试"""
        user_id = "user1"
        # 计算用户消息表：使用用户ID的哈希值对128取模
        hash_id = abs(hash(user_id)) % 128
        user_message_table = f"t_user_messages_{hash_id}"
        logger.info(f"user:{user_id} user messages table is {user_message_table}")
        
        # 计算消息表：使用年份和月份
        now = datetime.now()
        month = now.month - 1  # 0-11
        year = now.year % 3
        message_table = f"t_messages_{year * 12 + month}"
        logger.info(f"This month save message to table {message_table}")


def main():
    """主函数"""
    main_app = Main()
    main_app.run(sys.argv[1:] if len(sys.argv) > 1 else [])


if __name__ == "__main__":
    main()
