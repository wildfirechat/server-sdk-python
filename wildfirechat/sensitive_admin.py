"""
敏感词管理类
对应Java SDK中的 cn.wildfirechat.sdk.SensitiveAdmin
"""
from typing import List
from .api_path import APIPath
from .http_utils import AdminHttpUtils
from .models import IMResult, InputOutputSensitiveWords


class SensitiveAdmin:
    """敏感词管理类"""
    
    @staticmethod
    def add_sensitive_words(words: List[str]) -> IMResult:
        """
        添加敏感词
        
        :param words: 敏感词列表
        :return: 添加结果
        """
        input_data = InputOutputSensitiveWords(words=words)
        return AdminHttpUtils.http_json_post(APIPath.Sensitive_Add, input_data, type(None))
    
    @staticmethod
    def remove_sensitive_words(words: List[str]) -> IMResult:
        """
        删除敏感词
        
        :param words: 敏感词列表
        :return: 删除结果
        """
        input_data = InputOutputSensitiveWords(words=words)
        return AdminHttpUtils.http_json_post(APIPath.Sensitive_Del, input_data, type(None))
    
    @staticmethod
    def get_sensitive_words() -> IMResult:
        """
        获取敏感词列表
        
        :return: 敏感词列表
        """
        return AdminHttpUtils.http_json_post(APIPath.Sensitive_Query, None, InputOutputSensitiveWords)
