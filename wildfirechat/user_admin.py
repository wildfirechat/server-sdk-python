"""
用户管理类
对应Java SDK中的 cn.wildfirechat.sdk.UserAdmin
"""
from typing import List
from .api_path import APIPath
from .http_utils import AdminHttpUtils
from .models import (
    IMResult, InputOutputUserInfo, OutputCreateUser, InputCreateRobot,
    OutputCreateRobot, OutputRobot, OutputUserInfoList, OutputGetUserList,
    OutputGetIMTokenData, OutputUserStatus, OutputUserBlockStatusList,
    OutputCheckUserOnline, GetOnlineUserCountResult, GetOnlineUserResult,
    GetUserSessionResult, OutputApplicationUserInfo, OutputStringList,
    OutputCreateDevice, OutputDevice, OutputDeviceList, 
    InputGetUserInfo, InputGetToken, InputUpdateUserInfo,
    InputDestroyUser, InputRobotId, InputUserId, InputOutputUserBlockStatus,
    StringPairPojo, InputGetUserList, InputCreateDevice, InputDeviceId,
    GetOnlineUserRequest, InputApplicationGetUserInfo
)
from .proto_constants import Platform


class UserAdmin:
    """用户管理类"""
    
    @staticmethod
    def get_user_by_name(name: str, include_deleted: bool = False) -> IMResult:
        """
        根据用户名获取用户信息
        
        :param name: 用户名
        :param include_deleted: 是否包含已删除的用户
        :return: 用户信息
        """
        path = APIPath.User_Get_Info
        get_user_info = InputGetUserInfo(name=name, includeDeleted=include_deleted)
        return AdminHttpUtils.http_json_post(path, get_user_info, InputOutputUserInfo)
    
    @staticmethod
    def get_user_by_user_id(user_id: str, include_deleted: bool = False) -> IMResult:
        """
        根据用户ID获取用户信息
        
        :param user_id: 用户ID
        :param include_deleted: 是否包含已删除的用户
        :return: 用户信息
        """
        path = APIPath.User_Get_Info
        get_user_info = InputGetUserInfo(userId=user_id, includeDeleted=include_deleted)
        return AdminHttpUtils.http_json_post(path, get_user_info, InputOutputUserInfo)
    
    @staticmethod
    def get_user_by_mobile(mobile: str, include_deleted: bool = False) -> IMResult:
        """
        根据手机号获取用户信息
        
        :param mobile: 手机号
        :param include_deleted: 是否包含已删除的用户
        :return: 用户信息
        """
        path = APIPath.User_Get_Info
        get_user_info = InputGetUserInfo(mobile=mobile, includeDeleted=include_deleted)
        return AdminHttpUtils.http_json_post(path, get_user_info, InputOutputUserInfo)
    
    @staticmethod
    def get_user_by_email(email: str) -> IMResult:
        """
        根据邮箱获取用户信息列表
        
        :param email: 邮箱地址
        :return: 用户信息列表
        """
        path = APIPath.User_Get_Email_Info
        return AdminHttpUtils.http_json_post(path, email, OutputUserInfoList)
    
    @staticmethod
    def get_all_users(count: int, offset: int) -> IMResult:
        """
        获取所有用户列表（分页）
        
        :param count: 每页数量
        :param offset: 偏移量
        :return: 用户列表
        """
        path = APIPath.User_Get_All
        input_data = InputGetUserList(count=count, offset=offset)
        return AdminHttpUtils.http_json_post(path, input_data, OutputGetUserList)
    
    @staticmethod
    def get_batch_users(user_ids: List[str]) -> IMResult:
        """
        批量获取用户信息
        
        :param user_ids: 用户ID列表
        :return: 用户信息列表
        """
        path = APIPath.User_Batch_Get_Infos
        input_data = {"list": user_ids}
        return AdminHttpUtils.http_json_post(path, input_data, OutputUserInfoList)
    
    @staticmethod
    def create_user(user: InputOutputUserInfo) -> IMResult:
        """
        创建用户
        
        :param user: 用户信息
        :return: 创建结果，包含用户ID
        """
        path = APIPath.Create_User
        return AdminHttpUtils.http_json_post(path, user, OutputCreateUser)
    
    @staticmethod
    def update_user_info(user: InputOutputUserInfo, flag: int) -> IMResult:
        """
        更新用户信息
        
        :param user: 用户信息
        :param flag: 更新标志位，指定要更新的字段（UpdateUserInfoMask）
        :return: 更新结果
        """
        path = APIPath.Update_User
        update_user_info = InputUpdateUserInfo(flag=flag, userInfo=user)
        return AdminHttpUtils.http_json_post(path, update_user_info, type(None))
    
    @staticmethod
    def create_robot(robot: InputCreateRobot) -> IMResult:
        """
        创建机器人
        
        :param robot: 机器人信息
        :return: 创建结果，包含机器人ID和Token
        """
        path = APIPath.Create_Robot
        return AdminHttpUtils.http_json_post(path, robot, OutputCreateRobot)
    
    @staticmethod
    def destroy_robot(user_id: str) -> IMResult:
        """
        销毁机器人
        
        :param user_id: 机器人用户ID
        :return: 销毁结果
        """
        path = APIPath.Destroy_User
        input_destroy_user = InputDestroyUser(userId=user_id)
        return AdminHttpUtils.http_json_post(path, input_destroy_user, type(None))
    
    @staticmethod
    def get_robot_info(robot_id: str) -> IMResult:
        """
        获取机器人信息
        
        :param robot_id: 机器人ID
        :return: 机器人信息
        """
        path = APIPath.User_Get_Robot_Info
        get_robot_info = InputRobotId(robotId=robot_id)
        return AdminHttpUtils.http_json_post(path, get_robot_info, OutputRobot)
    
    @staticmethod
    def get_user_robots(user_id: str) -> IMResult:
        """
        获取用户的机器人列表
        
        :param user_id: 用户ID
        :return: 机器人ID列表
        """
        path = APIPath.User_Get_User_Robots
        get_robot_info = InputUserId(userId=user_id)
        return AdminHttpUtils.http_json_post(path, get_robot_info, OutputStringList)
    
    @staticmethod
    def get_user_token(user_id: str, client_id: str, platform: int) -> IMResult:
        """
        获取用户的IM Token
        
        :param user_id: 用户ID
        :param client_id: 客户端ID
        :param platform: 平台类型
        :return: Token信息
        """
        path = APIPath.User_Get_Token
        get_token = InputGetToken(userId=user_id, clientId=client_id, platform=platform)
        return AdminHttpUtils.http_json_post(path, get_token, OutputGetIMTokenData)
    
    @staticmethod
    def update_user_block_status(user_id: str, block: int) -> IMResult:
        """
        更新用户封禁状态
        
        :param user_id: 用户ID
        :param block: 封禁状态：0-正常，1-封禁
        :return: 更新结果
        """
        path = APIPath.User_Update_Block_Status
        block_status = InputOutputUserBlockStatus(userId=user_id, status=block)
        return AdminHttpUtils.http_json_post(path, block_status, type(None))
    
    @staticmethod
    def check_user_block_status(user_id: str) -> IMResult:
        """
        检查用户封禁状态
        
        :param user_id: 用户ID
        :return: 用户封禁状态
        """
        path = APIPath.User_Check_Block_Status
        get_user_info = InputGetUserInfo(userId=user_id)
        return AdminHttpUtils.http_json_post(path, get_user_info, OutputUserStatus)
    
    @staticmethod
    def get_blocked_list() -> IMResult:
        """
        获取被封禁用户列表
        
        :return: 被封禁用户列表
        """
        path = APIPath.User_Get_Blocked_List
        return AdminHttpUtils.http_json_post(path, None, OutputUserBlockStatusList)
    
    @staticmethod
    def check_user_online_status(user_id: str) -> IMResult:
        """
        检查用户在线状态
        
        :param user_id: 用户ID
        :return: 用户在线状态
        """
        path = APIPath.User_Get_Online_Status
        get_user_info = InputGetUserInfo(userId=user_id)
        return AdminHttpUtils.http_json_post(path, get_user_info, OutputCheckUserOnline)
    
    @staticmethod
    def kickoff_user_client(user_id: str, client_id: str = None) -> IMResult:
        """
        强迫用户下线
        
        :param user_id: 用户ID
        :param client_id: 客户端ID，为空时踢下线所有客户端
        :return: 下线结果
        """
        path = APIPath.User_Kickoff_Client
        pojo = StringPairPojo(first=user_id, second=client_id if client_id else "")
        return AdminHttpUtils.http_json_post(path, pojo, type(None))
    
    @staticmethod
    def destroy_user(user_id: str) -> IMResult:
        """
        销毁用户
        
        :param user_id: 用户ID
        :return: 销毁结果
        """
        path = APIPath.Destroy_User
        input_destroy_user = InputDestroyUser(userId=user_id)
        return AdminHttpUtils.http_json_post(path, input_destroy_user, type(None))
    
    @staticmethod
    def create_or_update_device(device: InputCreateDevice) -> IMResult:
        """
        创建或更新设备信息（仅专业版支持）
        
        :param device: 设备信息
        :return: 创建或更新结果
        """
        path = APIPath.CreateOrUpdate_Device
        return AdminHttpUtils.http_json_post(path, device, OutputCreateDevice)
    
    @staticmethod
    def get_device(device_id: str) -> IMResult:
        """
        获取设备信息（仅专业版支持）
        
        :param device_id: 设备ID
        :return: 设备信息
        """
        path = APIPath.Get_Device
        input_device_id = InputDeviceId(deviceId=device_id)
        return AdminHttpUtils.http_json_post(path, input_device_id, OutputDevice)
    
    @staticmethod
    def get_user_devices(user_id: str) -> IMResult:
        """
        获取用户的设备列表
        
        :param user_id: 用户ID
        :return: 用户设备列表
        """
        path = APIPath.Get_User_Devices
        input_user_id = InputUserId(userId=user_id)
        return AdminHttpUtils.http_json_post(path, input_user_id, OutputDeviceList)
    
    @staticmethod
    def get_online_user_count() -> IMResult:
        """
        获取在线用户数量
        
        :return: 在线用户数量统计结果
        """
        return AdminHttpUtils.http_json_post(APIPath.User_Online_Count, None, GetOnlineUserCountResult)
    
    @staticmethod
    def get_online_user(node_id: int, offset: int, count: int) -> IMResult:
        """
        获取在线用户列表（分页）
        
        :param node_id: 节点ID，用于分布式部署场景
        :param offset: 偏移量
        :param count: 每页数量
        :return: 在线用户列表
        """
        request = GetOnlineUserRequest(nodeId=node_id, offset=offset, count=count)
        return AdminHttpUtils.http_json_post(APIPath.User_Online_List, request, GetOnlineUserResult)
    
    @staticmethod
    def application_get_user_info(auth_code: str) -> IMResult:
        """
        通过应用授权码获取用户信息
        
        :param auth_code: 应用授权码
        :return: 用户信息
        """
        path = APIPath.User_Application_Get_UserInfo
        input_data = InputApplicationGetUserInfo(authCode=auth_code)
        return AdminHttpUtils.http_json_post(path, input_data, OutputApplicationUserInfo)
    
    @staticmethod
    def get_user_session(user_id: str) -> IMResult:
        """
        获取用户会话信息
        
        :param user_id: 用户ID
        :return: 用户会话信息
        """
        input_user_id = InputUserId(userId=user_id)
        return AdminHttpUtils.http_json_post(APIPath.User_Session_List, input_user_id, GetUserSessionResult)
