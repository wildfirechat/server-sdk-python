"""
通用管理类
对应Java SDK中的 cn.wildfirechat.sdk.GeneralAdmin
"""
import os
import mimetypes
from typing import Optional
from .api_path import APIPath
from .http_utils import AdminHttpUtils
from .models import (
    IMResult, SystemSettingPojo, UserSettingPojo, HealthCheckResult, FilesPojo,
    InputUserId, InputGetPresignedUploadUrl, OutputPresignedUploadUrl
)
from .proto_constants import SystemSettingType, MessageMediaType


class GeneralAdmin:
    """通用管理类"""
    
    @staticmethod
    def get_system_setting(id: int) -> IMResult:
        """
        获取系统设置
        
        :param id: 设置项ID
        :return: 系统设置
        """
        input_data = {"id": id}
        return AdminHttpUtils.http_json_post(APIPath.Get_System_Setting, input_data, SystemSettingPojo)
    
    @staticmethod
    def set_system_setting(id: int, value: str, desc: str = "") -> IMResult:
        """
        设置系统设置
        
        :param id: 设置项ID
        :param value: 设置值
        :param desc: 设置描述
        :return: 设置结果
        """
        input_data = {"id": id, "value": value, "desc": desc}
        return AdminHttpUtils.http_json_post(APIPath.Put_System_Setting, input_data, type(None))
    
    @staticmethod
    def health_check() -> IMResult:
        """
        健康检查
        
        :return: 健康检查结果
        """
        return AdminHttpUtils.http_get(APIPath.Health, HealthCheckResult)
    
    @staticmethod
    def set_user_setting(user_id: str, scope: int, key: str, value: str) -> IMResult:
        """
        设置用户设置
        
        :param user_id: 用户ID
        :param scope: 设置范围
        :param key: 设置键
        :param value: 设置值
        :return: 设置结果
        """
        input_data = {"userId": user_id, "scope": scope, "key": key, "value": value}
        return AdminHttpUtils.http_json_post(APIPath.User_Put_Setting, input_data, type(None))
    
    @staticmethod
    def get_user_setting(user_id: str, scope: int, key: str) -> IMResult:
        """
        获取用户设置
        
        :param user_id: 用户ID
        :param scope: 设置范围
        :param key: 设置键
        :return: 用户设置
        """
        input_data = {"userId": user_id, "scope": scope, "key": key}
        return AdminHttpUtils.http_json_post(APIPath.User_Get_Setting, input_data, UserSettingPojo)
    
    @staticmethod
    def set_conversation_top(user_id: str, conversation_type: int, target: str,
                             line: int, top: bool) -> IMResult:
        """
        设置会话置顶
        
        :param user_id: 用户ID
        :param conversation_type: 会话类型
        :param target: 会话目标
        :param line: 线路
        :param top: 是否置顶
        :return: 设置结果
        """
        key = f"{conversation_type}-{line}-{target}"
        value = "1" if top else "0"
        return GeneralAdmin.set_user_setting(user_id, 3, key, value)
    
    @staticmethod
    def get_conversation_top(user_id: str, conversation_type: int, target: str,
                             line: int) -> IMResult:
        """
        获取会话置顶状态
        
        :param user_id: 用户ID
        :param conversation_type: 会话类型
        :param target: 会话目标
        :param line: 线路
        :return: 是否置顶
        """
        # scope 3 是置顶设置
        key = f"{conversation_type}-{line}-{target}"
        result = GeneralAdmin.get_user_setting(user_id, 3, key)
        if result.code == 0 and result.result:
            # 转换结果为布尔值
            bool_result = IMResult()
            bool_result.code = result.code
            bool_result.msg = result.msg
            bool_result.result = result.result.value == "1"
            return bool_result
        return result
    
    @staticmethod
    def get_conversation_files(conversation_type: int, target: str, line: int,
                               user_id: str, offset: int, desc: bool,
                               count: int) -> IMResult:
        """
        获取会话文件列表（仅专业版支持）
        
        如果是单聊会话，target和userId代表会话的2个用户；如果是其他会话userId无意义。
        
        :param conversation_type: 会话类型
        :param target: 会话目标ID
        :param line: 线路
        :param user_id: 用户ID
        :param offset: 偏移量
        :param desc: 是否降序
        :param count: 每页数量
        :return: 文件列表
        """
        input_data = {
            "conversationType": conversation_type,
            "target": target,
            "line": line,
            "userId": user_id,
            "offset": offset,
            "desc": desc,
            "count": count
        }
        return AdminHttpUtils.http_json_post(APIPath.Get_Conversation_Files, input_data, FilesPojo)
    
    @staticmethod
    def get_user_files(user_id: str, offset: int, desc: bool, count: int) -> IMResult:
        """
        获取用户文件列表
        
        :param user_id: 用户ID
        :param offset: 偏移量
        :param desc: 是否降序
        :param count: 每页数量
        :return: 文件列表
        """
        input_data = {
            "userId": user_id,
            "offset": offset,
            "desc": desc,
            "count": count
        }
        return AdminHttpUtils.http_json_post(APIPath.Get_User_Files, input_data, FilesPojo)
    
    @staticmethod
    def get_file(message_id: int) -> IMResult:
        """
        根据消息ID获取文件信息
        
        :param message_id: 消息ID
        :return: 文件信息
        """
        input_data = {"messageUid": message_id}
        return AdminHttpUtils.http_json_post(APIPath.Get_Message_File, input_data, FilesPojo.FilePojo)
    
    @staticmethod
    def get_customer() -> IMResult:
        """
        获取客户信息
        
        :return: 客户信息
        """
        return AdminHttpUtils.http_json_post(APIPath.GET_CUSTOMER, None, str)
    
    @staticmethod
    def get_presigned_upload_url(file_name: str, media_type: int, content_type: str) -> IMResult:
        """
        获取预签名上传URL
        
        :param file_name: 文件名
        :param media_type: 媒体类型，参考 MessageMediaType
        :param content_type: 文件Content-Type，例如 "image/jpeg", "application/octet-stream" 等
        :return: 预签名上传URL信息
        """
        request_pojo = InputGetPresignedUploadUrl(
            fileName=file_name,
            mediaType=media_type,
            contentType=content_type
        )
        return AdminHttpUtils.http_json_post(APIPath.Get_Presigned_Upload_Url, request_pojo, OutputPresignedUploadUrl)
    
    @staticmethod
    def _get_content_type_by_file_name(file_name: str) -> str:
        """
        根据文件名获取Content-Type
        
        :param file_name: 文件名
        :return: Content-Type，如果无法识别则返回 "application/octet-stream"
        """
        if not file_name:
            return "application/octet-stream"
        
        # 首先尝试使用 mimetypes 猜测
        content_type, _ = mimetypes.guess_type(file_name)
        
        # 如果无法识别，使用常见扩展名映射
        if content_type is None:
            lower_name = file_name.lower()
            ext_map = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.bmp': 'image/bmp',
                '.webp': 'image/webp',
                '.mp4': 'video/mp4',
                '.mov': 'video/quicktime',
                '.avi': 'video/x-msvideo',
                '.mp3': 'audio/mpeg',
                '.wav': 'audio/wav',
                '.pdf': 'application/pdf',
                '.doc': 'application/msword',
                '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                '.xls': 'application/vnd.ms-excel',
                '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                '.ppt': 'application/vnd.ms-powerpoint',
                '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                '.txt': 'text/plain',
                '.html': 'text/html',
                '.htm': 'text/html',
                '.json': 'application/json',
                '.xml': 'application/xml',
                '.zip': 'application/zip',
                '.rar': 'application/x-rar-compressed',
                '.7z': 'application/x-7z-compressed',
                '.tar': 'application/x-tar',
                '.gz': 'application/gzip',
            }
            ext = os.path.splitext(lower_name)[1]
            content_type = ext_map.get(ext, 'application/octet-stream')
        
        return content_type
    
    @staticmethod
    def upload_file(file_path: str, media_type: int = MessageMediaType.FILE, content_type: str = None) -> IMResult:
        """
        上传文件
        
        流程：先调用get_presigned_upload_url获取预签名上传地址，然后直接上传文件。
        上传成功后返回文件的下载地址等信息。
        
        :param file_path: 要上传的文件路径
        :param media_type: 媒体类型，参考 MessageMediaType，默认为 FILE
        :param content_type: 文件Content-Type，如果为None则根据文件名自动识别
        :return: 上传结果，包含下载地址
        """
        import requests
        
        if not file_path or not os.path.exists(file_path):
            raise ValueError("文件路径不能为空或文件不存在")
        
        file_name = os.path.basename(file_path)
        
        # 如果未指定Content-Type，根据文件名自动获取
        if content_type is None:
            content_type = GeneralAdmin._get_content_type_by_file_name(file_name)
        
        # 1. 获取预签名上传地址
        presigned_result = GeneralAdmin.get_presigned_upload_url(file_name, media_type, content_type)
        
        if presigned_result.code != 0:
            return presigned_result
        
        presigned_url = presigned_result.result
        if presigned_url is None or not presigned_url.url:
            result = IMResult()
            result.code = -1
            result.msg = "预签名上传地址为空"
            return result
        
        # 2. 上传文件
        try:
            with open(file_path, 'rb') as f:
                headers = {'Content-Type': content_type}
                response = requests.put(presigned_url.url, data=f, headers=headers)
                
                if response.status_code not in [200, 201]:
                    result = IMResult()
                    result.code = response.status_code
                    result.msg = f"文件上传失败，HTTP状态码：{response.status_code}"
                    return result
                
                # 返回下载地址
                result = IMResult()
                result.code = 0
                result.result = presigned_url.url
                return result
        except Exception as e:
            result = IMResult()
            result.code = -1
            result.msg = str(e)
            return result
