"""
管理员配置类
对应Java SDK中的 cn.wildfirechat.sdk.AdminConfig
"""
from .http_utils import AdminHttpUtils


class AdminConfig:
    """管理员配置类"""
    
    @staticmethod
    def init_admin(url: str, secret: str, timeout: int = 15):
        """
        初始化管理员配置
        
        :param url: IM服务器地址，例如: http://your-im-server.com:18080
        :param secret: 管理员密钥，在服务器配置中设置
        :param timeout: 超时时间（秒），默认15秒
        """
        AdminHttpUtils.init(url, secret, timeout)
