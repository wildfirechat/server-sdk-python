"""
会议管理类
对应Java SDK中的 cn.wildfirechat.sdk.ConferenceAdmin
"""
from typing import List
from .api_path import APIPath
from .http_utils import AdminHttpUtils
from .models import (
    IMResult, InputCountOffset, PojoConferenceInfoList,
    PojoConferenceParticipantList, PojoConferenceRtpForwarders
)


class ConferenceAdmin:
    """会议管理类"""
    
    @staticmethod
    def list_conferences(count: int = 0, offset: int = 0) -> IMResult:
        """
        获取会议列表（分页）
        
        :param count: 每页数量
        :param offset: 偏移量
        :return: 会议列表
        """
        input_data = InputCountOffset(count=count, offset=offset)
        return AdminHttpUtils.http_json_post(APIPath.Conference_List, input_data, PojoConferenceInfoList)
    
    @staticmethod
    def check_conference_exist(conference_id: str) -> IMResult:
        """
        检查会议是否存在
        
        :param conference_id: 会议ID
        :return: 是否存在
        """
        input_data = {"conferenceId": conference_id}
        return AdminHttpUtils.http_json_post(APIPath.Conference_Exist, input_data, bool)
    
    @staticmethod
    def list_participants(conference_id: str) -> IMResult:
        """
        获取会议参与者列表
        
        :param conference_id: 会议ID
        :return: 参与者列表
        """
        input_data = {"conferenceId": conference_id}
        return AdminHttpUtils.http_json_post(APIPath.Conference_List_Participant, input_data, PojoConferenceParticipantList)
    
    @staticmethod
    def create_conference(conference_id: str, conference_title: str, password: str = "",
                          advance: bool = False, recording: bool = False) -> IMResult:
        """
        创建会议
        
        :param conference_id: 会议ID
        :param conference_title: 会议标题
        :param password: 会议密码
        :param advance: 是否高级会议
        :param recording: 是否录制
        :return: 创建结果
        """
        input_data = {
            "conferenceId": conference_id,
            "conferenceTitle": conference_title,
            "password": password,
            "advance": advance,
            "recording": recording
        }
        return AdminHttpUtils.http_json_post(APIPath.Conference_Create, input_data, type(None))
    
    @staticmethod
    def destroy_conference(conference_id: str) -> IMResult:
        """
        销毁会议
        
        :param conference_id: 会议ID
        :return: 销毁结果
        """
        input_data = {"conferenceId": conference_id}
        return AdminHttpUtils.http_json_post(APIPath.Conference_Destroy, input_data, type(None))
    
    @staticmethod
    def set_recording(conference_id: str, recording: bool) -> IMResult:
        """
        设置会议录制状态
        
        :param conference_id: 会议ID
        :param recording: 是否录制
        :return: 设置结果
        """
        input_data = {"conferenceId": conference_id, "recording": recording}
        return AdminHttpUtils.http_json_post(APIPath.Conference_Recording, input_data, type(None))
    
    @staticmethod
    def rtp_forward(conference_id: str, rtp_forwarder: dict) -> IMResult:
        """
        RTP转发
        
        :param conference_id: 会议ID
        :param rtp_forwarder: RTP转发配置
        :return: 转发结果
        """
        input_data = {"conferenceId": conference_id, "rtpForwarder": rtp_forwarder}
        return AdminHttpUtils.http_json_post(APIPath.Conference_Rtp_Forward, input_data, type(None))
    
    @staticmethod
    def stop_rtp_forward(conference_id: str, stream_id: int) -> IMResult:
        """
        停止RTP转发
        
        :param conference_id: 会议ID
        :param stream_id: 流ID
        :return: 停止结果
        """
        input_data = {"conferenceId": conference_id, "streamId": stream_id}
        return AdminHttpUtils.http_json_post(APIPath.Conference_Stop_Rtp_Forward, input_data, type(None))
    
    @staticmethod
    def list_rtp_forward(conference_id: str) -> IMResult:
        """
        获取RTP转发列表
        
        :param conference_id: 会议ID
        :return: RTP转发列表
        """
        input_data = {"conferenceId": conference_id}
        return AdminHttpUtils.http_json_post(APIPath.Conference_List_Rtp_Forward, input_data, PojoConferenceRtpForwarders)
