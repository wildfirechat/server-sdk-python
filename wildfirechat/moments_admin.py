"""
朋友圈管理类
对应Java SDK中的 cn.wildfirechat.sdk.MomentsAdmin
"""
from .api_path import APIPath
from .http_utils import AdminHttpUtils
from .models import IMResult, SendMessageResult


class MomentsAdmin:
    """朋友圈管理类"""
    
    @staticmethod
    def post_feeds(feed_pojo: dict) -> IMResult:
        """
        发布朋友圈动态
        
        :param feed_pojo: 动态信息字典，包含 sender, type, text, medias 等字段
        :return: 发布结果
        """
        return AdminHttpUtils.http_json_post(APIPath.Admin_Moments_Post_Feed, feed_pojo, SendMessageResult)
