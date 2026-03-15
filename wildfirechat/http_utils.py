"""
HTTP工具类
对应Java SDK中的 cn.wildfirechat.sdk.utilities.AdminHttpUtils 和 HttpUtils
"""
import hashlib
import json
import logging
import random
import time
from typing import TypeVar, Type, Optional, Callable
import dataclasses
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .models import IMResult
from .error_code import ErrorCode


def serialize_to_dict(obj):
    """
    将对象序列化为字典，支持 dataclass 和嵌套对象
    """
    if dataclasses.is_dataclass(obj):
        result = {}
        for field in dataclasses.fields(obj):
            value = getattr(obj, field.name)
            # 递归处理嵌套对象
            if value is not None:
                if dataclasses.is_dataclass(value):
                    value = serialize_to_dict(value)
                elif isinstance(value, list):
                    value = [serialize_to_dict(item) if dataclasses.is_dataclass(item) else item for item in value]
            # 过滤空值（但保留0和False）
            if value is not None and value != "":
                result[field.name] = value
            elif value == 0 or value is False:
                result[field.name] = value
        return result
    elif hasattr(obj, '__dict__'):
        return obj.__dict__
    else:
        return str(obj)


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

T = TypeVar('T')


class AdminHttpUtils:
    """管理员HTTP工具类"""
    
    # 配置常量
    DEFAULT_CONNECT_TIMEOUT = 15
    DEFAULT_READ_TIMEOUT = 15
    DEFAULT_MAX_RETRIES = 3
    MAX_CONN_TOTAL = 100
    MAX_CONN_PER_ROUTE = 50
    NONCE_MAX_RANGE = 1000000
    
    # 线程安全的全局变量
    _admin_url: Optional[str] = None
    _admin_secret: Optional[str] = None
    _session: Optional[requests.Session] = None
    _lock = False
    
    @classmethod
    def init(cls, url: str, secret: str, timeout: int = DEFAULT_READ_TIMEOUT):
        """
        初始化HTTP客户端和配置
        
        :param url: IM服务管理地址
        :param secret: 管理密钥
        :param timeout: 超时时间（秒）
        """
        # 参数校验
        if not url or not secret:
            raise ValueError("IM服务地址或密钥不能为空")
        
        cls._admin_url = url.strip()
        cls._admin_secret = secret.strip()
        
        # 创建session
        cls._session = requests.Session()
        
        # 配置重试策略
        retry_strategy = Retry(
            total=cls.DEFAULT_MAX_RETRIES,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=cls.MAX_CONN_PER_ROUTE,
            pool_maxsize=cls.MAX_CONN_TOTAL,
        )
        
        cls._session.mount("http://", adapter)
        cls._session.mount("https://", adapter)
        
        logger.info(f"AdminHttpUtils初始化完成，IM服务地址：{cls._admin_url}")
    
    @classmethod
    def _validate_init_status(cls):
        """校验初始化状态"""
        if not cls._admin_url or not cls._admin_secret or not cls._session:
            error_msg = "野火IM Server SDK未初始化，请调用AdminConfig.initAdmin(AdminUrl, AdminSecret)完成初始化"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    @classmethod
    def _generate_signature(cls) -> tuple:
        """生成签名"""
        nonce = random.randint(1, cls.NONCE_MAX_RANGE)
        timestamp = int(time.time() * 1000)
        sign_str = f"{nonce}|{cls._admin_secret}|{timestamp}"
        sign = hashlib.sha1(sign_str.encode('utf-8')).hexdigest()
        return nonce, timestamp, sign
    
    @classmethod
    def http_get(cls, path: str, result_class: Type[T] = None) -> IMResult:
        """
        HTTP GET请求
        
        :param path: 请求路径
        :param result_class: 结果类型
        :return: IMResult对象
        """
        cls._validate_init_status()
        
        if not path:
            raise ValueError("请求路径不能为空")
        
        url = cls._admin_url + path
        
        try:
            nonce, timestamp, sign = cls._generate_signature()
            headers = {
                "Content-type": "application/json; charset=utf-8",
                "nonce": str(nonce),
                "timestamp": str(timestamp),
                "sign": sign,
            }
            
            logger.info(f"HTTP GET请求：{url}")
            response = cls._session.get(
                url,
                headers=headers,
                timeout=(cls.DEFAULT_CONNECT_TIMEOUT, cls.DEFAULT_READ_TIMEOUT)
            )
            return cls._handle_response(response, result_class)
        except Exception as e:
            logger.error(f"HTTP GET请求失败，路径：{path}", exc_info=True)
            raise Exception(f"HTTP GET请求异常：{str(e)}")
    
    @classmethod
    def http_json_post(cls, path: str, data: any, result_class: Type[T] = None) -> IMResult:
        """
        HTTP JSON POST请求
        
        :param path: 请求路径
        :param data: 请求数据
        :param result_class: 结果类型
        :return: IMResult对象
        """
        cls._validate_init_status()
        
        if not path:
            raise ValueError("请求路径不能为空")
        
        url = cls._admin_url + path
        
        try:
            nonce, timestamp, sign = cls._generate_signature()
            headers = {
                "Content-type": "application/json; charset=utf-8",
                "Connection": "Keep-Alive",
                "nonce": str(nonce),
                "timestamp": str(timestamp),
                "sign": sign,
            }
            
            json_str = json.dumps(data, default=serialize_to_dict, ensure_ascii=False) if data else ""
            logger.info(f"HTTP POST请求：{url}，请求体：{cls._truncate_log_content(json_str)}")
            
            response = cls._session.post(
                url,
                headers=headers,
                data=json_str.encode('utf-8'),
                timeout=(cls.DEFAULT_CONNECT_TIMEOUT, cls.DEFAULT_READ_TIMEOUT)
            )
            return cls._handle_response(response, result_class)
        except Exception as e:
            logger.error(f"HTTP POST请求失败，路径：{path}", exc_info=True)
            raise Exception(f"HTTP POST请求异常：{str(e)}")
    
    @classmethod
    def _handle_response(cls, response: requests.Response, result_class: Type[T] = None) -> IMResult:
        """处理HTTP响应"""
        status_code = response.status_code
        content = response.text
        
        # 非200状态码处理
        if status_code != 200:
            error_msg = f"HTTP请求失败，状态码：{status_code}，响应内容：{cls._truncate_log_content(content)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        
        # 解析响应体
        logger.info(f"HTTP响应内容：{cls._truncate_log_content(content)}")
        
        try:
            json_data = json.loads(content)
        except json.JSONDecodeError:
            # 如果响应不是JSON格式，可能是简单的字符串
            result = IMResult()
            result.code = 0
            result.msg = "success"
            result.result = content
            return result
        
        result = IMResult()
        result.code = json_data.get("code", 0)
        result.msg = json_data.get("msg", "")
        
        result_data = json_data.get("result")
        if result_data is not None and result_class is not None and result_class != type(None):
            # 转换结果为指定类型
            if isinstance(result_data, dict):
                result.result = cls._dict_to_class(result_data, result_class)
            elif isinstance(result_data, list):
                # 特殊处理：如果 result_class 是 OutputStringList，将列表包装成对象
                from .models import OutputStringList
                if result_class == OutputStringList:
                    result.result = OutputStringList.from_list(result_data)
                else:
                    result.result = result_data
            else:
                result.result = result_data
        else:
            result.result = result_data
        
        # 检查错误码
        error_code = result.get_error_code()
        if error_code == ErrorCode.ERROR_CODE_AUTH_FAILURE:
            logger.error(f"鉴权失败，请检查IM服务地址({cls._admin_url})或密钥({cls._mask_secret(cls._admin_secret)})配置")
        elif error_code == ErrorCode.ERROR_CODE_SIGN_EXPIRED:
            logger.error(f"签名过期，请确保当前服务与IM服务({cls._admin_url})时间同步")
        
        return result
    
    @classmethod
    def _dict_to_class(cls, data: dict, clazz: Type[T]) -> T:
        """将字典转换为类实例，递归处理列表和嵌套dataclass"""
        if data is None:
            return None
        
        import dataclasses
        from typing import get_origin, get_args, List, Dict, Any
        
        # 处理dataclass
        if dataclasses.is_dataclass(clazz):
            field_map = {f.name: f for f in dataclasses.fields(clazz)}
            filtered_data = {}
            
            for key, value in data.items():
                if key not in field_map:
                    continue
                
                field = field_map[key]
                field_type = field.type
                
                # 处理列表类型（包括字段名为'list'的情况）
                origin = get_origin(field_type)
                if origin is list or origin is List:
                    args = get_args(field_type)
                    if args and len(args) == 1:
                        elem_type = args[0]
                        if dataclasses.is_dataclass(elem_type) and isinstance(value, list):
                            # 递归转换列表中的字典为dataclass
                            value = [cls._dict_to_class(item, elem_type) if isinstance(item, dict) else item 
                                     for item in value]
                        elif elem_type == dict or elem_type == Dict:
                            # List[Dict[...]] 类型，保持原样
                            pass
                        # 其他简单类型（str, int等）保持原样
                
                # 处理嵌套dataclass（非列表）
                elif dataclasses.is_dataclass(field_type) and isinstance(value, dict):
                    value = cls._dict_to_class(value, field_type)
                
                filtered_data[key] = value
            
            # 对于没有匹配到任何字段的情况，尝试直接使用原始数据
            if not filtered_data and data:
                # 检查是否有字段名冲突（如'list'字段）
                for field in dataclasses.fields(clazz):
                    if field.name in data:
                        filtered_data[field.name] = data[field.name]
            
            return clazz(**filtered_data)
        
        # 处理普通类
        instance = clazz()
        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        return instance
    
    @classmethod
    def _truncate_log_content(cls, content: str, max_length: int = 1024) -> str:
        """截断超长日志内容"""
        if not content:
            return ""
        if len(content) > max_length:
            return content[:max_length] + "..."
        return content
    
    @classmethod
    def _mask_secret(cls, secret: str) -> str:
        """掩码处理密钥"""
        if not secret or len(secret) <= 4:
            return "******"
        return secret[:2] + "******" + secret[-2:]


class RobotHttpUtils:
    """机器人HTTP工具类"""
    
    DEFAULT_TIMEOUT = 15
    _session: Optional[requests.Session] = None
    
    @classmethod
    def get_session(cls) -> requests.Session:
        """获取HTTP Session"""
        if cls._session is None:
            cls._session = requests.Session()
        return cls._session
    
    @classmethod
    def http_json_post(cls, url: str, data: any, headers: dict = None, result_class: Type[T] = None) -> IMResult:
        """
        HTTP JSON POST请求
        
        :param url: 请求URL
        :param data: 请求数据
        :param headers: 请求头
        :param result_class: 结果类型，用于自动转换result字段
        :return: IMResult对象
        """
        session = cls.get_session()
        
        try:
            json_str = json.dumps(data, default=serialize_to_dict, ensure_ascii=False) if data else ""
            logger.info(f"Robot HTTP POST请求：{url}")
            
            request_headers = {
                "Content-type": "application/json; charset=utf-8",
                "Connection": "Keep-Alive",
            }
            if headers:
                request_headers.update(headers)
            
            response = session.post(
                url,
                headers=request_headers,
                data=json_str.encode('utf-8'),
                timeout=cls.DEFAULT_TIMEOUT
            )
            
            status_code = response.status_code
            content = response.text
            
            if status_code != 200:
                error_msg = f"HTTP请求失败，状态码：{status_code}"
                logger.error(error_msg)
                raise Exception(error_msg)
            
            json_data = json.loads(content)
            result = IMResult()
            result.code = json_data.get("code", 0)
            result.msg = json_data.get("msg", "")
            
            result_data = json_data.get("result")
            if result_data is not None and result_class is not None and result_class != type(None):
                # 转换结果为指定类型
                if isinstance(result_data, dict):
                    result.result = cls._dict_to_class(result_data, result_class)
                elif isinstance(result_data, list):
                    # 特殊处理：如果 result_class 是 OutputStringList，将列表包装成对象
                    from .models import OutputStringList
                    if result_class == OutputStringList:
                        result.result = OutputStringList.from_list(result_data)
                    else:
                        result.result = result_data
                else:
                    result.result = result_data
            else:
                result.result = result_data
            
            return result
        except Exception as e:
            logger.error(f"Robot HTTP POST请求失败", exc_info=True)
            raise Exception(f"HTTP POST请求异常：{str(e)}")
    
    @classmethod
    def _dict_to_class(cls, data: dict, clazz: Type[T]) -> T:
        """将字典转换为类实例"""
        if data is None:
            return None
        
        import dataclasses
        if dataclasses.is_dataclass(clazz):
            field_names = {f.name for f in dataclasses.fields(clazz)}
            filtered_data = {k: v for k, v in data.items() if k in field_names}
            return clazz(**filtered_data)
        
        # 处理普通类
        instance = clazz()
        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        return instance


class ChannelHttpUtils:
    """频道HTTP工具类"""
    
    DEFAULT_TIMEOUT = 15
    _session: Optional[requests.Session] = None
    
    @classmethod
    def get_session(cls) -> requests.Session:
        """获取HTTP Session"""
        if cls._session is None:
            cls._session = requests.Session()
        return cls._session
    
    @classmethod
    def http_json_post(cls, url: str, data: any, headers: dict = None, result_class: Type[T] = None) -> IMResult:
        """HTTP JSON POST请求"""
        session = cls.get_session()
        
        try:
            json_str = json.dumps(data, default=serialize_to_dict, ensure_ascii=False) if data else ""
            logger.info(f"Channel HTTP POST请求：{url}")
            
            request_headers = {
                "Content-type": "application/json; charset=utf-8",
                "Connection": "Keep-Alive",
            }
            if headers:
                request_headers.update(headers)
            
            response = session.post(
                url,
                headers=request_headers,
                data=json_str.encode('utf-8'),
                timeout=cls.DEFAULT_TIMEOUT
            )
            
            status_code = response.status_code
            content = response.text
            
            if status_code != 200:
                error_msg = f"HTTP请求失败，状态码：{status_code}"
                logger.error(error_msg)
                raise Exception(error_msg)
            
            json_data = json.loads(content)
            result = IMResult()
            result.code = json_data.get("code", 0)
            result.msg = json_data.get("msg", "")
            
            result_data = json_data.get("result")
            if result_data is not None and result_class is not None and result_class != type(None):
                # 转换结果为指定类型
                if isinstance(result_data, dict):
                    result.result = cls._dict_to_class(result_data, result_class)
                elif isinstance(result_data, list):
                    # 特殊处理：如果 result_class 是 OutputStringList，将列表包装成对象
                    from .models import OutputStringList
                    if result_class == OutputStringList:
                        result.result = OutputStringList.from_list(result_data)
                    else:
                        result.result = result_data
                else:
                    result.result = result_data
            else:
                result.result = result_data
            
            return result
        except Exception as e:
            logger.error(f"Channel HTTP POST请求失败", exc_info=True)
            raise Exception(f"HTTP POST请求异常：{str(e)}")
    
    @classmethod
    def _dict_to_class(cls, data: dict, clazz: Type[T]) -> T:
        """将字典转换为类实例"""
        if data is None:
            return None
        
        import dataclasses
        if dataclasses.is_dataclass(clazz):
            field_names = {f.name for f in dataclasses.fields(clazz)}
            filtered_data = {k: v for k, v in data.items() if k in field_names}
            return clazz(**filtered_data)
        
        # 处理普通类
        instance = clazz()
        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        return instance
    
    @classmethod
    def http_get(cls, url: str, headers: dict = None) -> IMResult:
        """HTTP GET请求"""
        session = cls.get_session()
        
        try:
            request_headers = {
                "Content-type": "application/json; charset=utf-8",
            }
            if headers:
                request_headers.update(headers)
            
            response = session.get(
                url,
                headers=request_headers,
                timeout=cls.DEFAULT_TIMEOUT
            )
            
            status_code = response.status_code
            content = response.text
            
            if status_code != 200:
                error_msg = f"HTTP请求失败，状态码：{status_code}"
                logger.error(error_msg)
                raise Exception(error_msg)
            
            json_data = json.loads(content)
            result = IMResult()
            result.code = json_data.get("code", 0)
            result.msg = json_data.get("msg", "")
            result.result = json_data.get("result")
            return result
        except Exception as e:
            logger.error(f"Channel HTTP GET请求失败", exc_info=True)
            raise Exception(f"HTTP GET请求异常：{str(e)}")
