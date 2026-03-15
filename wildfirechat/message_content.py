"""
消息内容类
对应Java SDK中的 cn.wildfirechat.sdk.messagecontent 包
"""
import base64
import json
from abc import ABC, abstractmethod
from typing import List
from .models import MessagePayload, QuoteInfo
from .proto_constants import ContentType, PersistFlag


class MessageContent(ABC):
    """消息内容基类"""
    
    def __init__(self):
        self._mentioned_type = 0
        self._mentioned_targets = []
        self._extra = ""
    
    def mentioned_type(self, mentioned_type: int):
        """设置@类型"""
        self._mentioned_type = mentioned_type
        return self
    
    def mentioned_targets(self, mentioned_targets: List[str]):
        """设置@目标"""
        self._mentioned_targets = mentioned_targets
        return self
    
    def extra(self, extra: str):
        """设置额外信息"""
        self._extra = extra
        return self
    
    def encode(self) -> MessagePayload:
        """编码为MessagePayload"""
        payload = MessagePayload()
        payload.type = self.get_content_type()
        payload.persistFlag = self.get_persist_flag()
        payload.mentionedType = self._mentioned_type
        payload.mentionedTarget = self._mentioned_targets
        payload.extra = self._extra
        return payload
    
    def decode(self, payload: MessagePayload):
        """从MessagePayload解码"""
        self._mentioned_type = payload.mentionedType
        self._mentioned_targets = payload.mentionedTarget if payload.mentionedTarget else []
        self._extra = payload.extra if payload.extra else ""
    
    @abstractmethod
    def get_content_type(self) -> int:
        """获取内容类型"""
        pass
    
    @abstractmethod
    def get_persist_flag(self) -> int:
        """获取持久化标志"""
        pass


class TextMessageContent(MessageContent):
    """文本消息内容类"""
    
    def __init__(self, text: str = ""):
        super().__init__()
        self._text = text
        self._quote_info = None
    
    def text(self, text: str):
        """设置文本"""
        self._text = text
        return self
    
    def get_text(self) -> str:
        """获取文本"""
        return self._text
    
    def set_text(self, text: str):
        """设置文本"""
        self._text = text
    
    def get_quote_info(self) -> QuoteInfo:
        """获取引用信息"""
        return self._quote_info
    
    def set_quote_info(self, quote_info: QuoteInfo):
        """设置引用信息"""
        self._quote_info = quote_info
    
    def get_content_type(self) -> int:
        return ContentType.Text
    
    def get_persist_flag(self) -> int:
        return PersistFlag.Persist_And_Count
    
    def encode(self) -> MessagePayload:
        payload = super().encode()
        payload.searchableContent = self._text
        if self._quote_info:
            quote_json = json.dumps(self._quote_info.encode(), ensure_ascii=False)
            payload.base64edData = base64.b64encode(quote_json.encode('utf-8')).decode('utf-8')
        return payload
    
    def decode(self, payload: MessagePayload):
        super().decode(payload)
        self._text = payload.searchableContent if payload.searchableContent else ""
        if payload.base64edData:
            try:
                quote_json = base64.b64decode(payload.base64edData).decode('utf-8')
                quote_data = json.loads(quote_json)
                self._quote_info = QuoteInfo()
                self._quote_info.decode(quote_data)
            except:
                pass


class SoundMessageContent(MessageContent):
    """语音消息内容类"""
    
    def __init__(self):
        super().__init__()
        self._duration = 0
        self._remote_media_url = ""
    
    def duration(self, duration: int):
        """设置时长"""
        self._duration = duration
        return self
    
    def get_duration(self) -> int:
        """获取时长"""
        return self._duration
    
    def set_duration(self, duration: int):
        """设置时长"""
        self._duration = duration
    
    def remote_media_url(self, url: str):
        """设置远程媒体URL"""
        self._remote_media_url = url
        return self
    
    def get_remote_media_url(self) -> str:
        """获取远程媒体URL"""
        return self._remote_media_url
    
    def set_remote_media_url(self, url: str):
        """设置远程媒体URL"""
        self._remote_media_url = url
    
    def get_content_type(self) -> int:
        return ContentType.Voice
    
    def get_persist_flag(self) -> int:
        return PersistFlag.Persist_And_Count
    
    def encode(self) -> MessagePayload:
        payload = super().encode()
        payload.mediaType = 2  # VOICE
        payload.remoteMediaUrl = self._remote_media_url
        payload.content = str(self._duration)
        return payload
    
    def decode(self, payload: MessagePayload):
        super().decode(payload)
        self._remote_media_url = payload.remoteMediaUrl if payload.remoteMediaUrl else ""
        try:
            self._duration = int(payload.content) if payload.content else 0
        except:
            self._duration = 0


class ImageMessageContent(MessageContent):
    """图片消息内容类"""
    
    def __init__(self):
        super().__init__()
        self._thumbnail_bytes = b""
        self._remote_media_url = ""
    
    def thumbnail_bytes(self, thumbnail: bytes):
        """设置缩略图字节"""
        self._thumbnail_bytes = thumbnail
        return self
    
    def get_thumbnail_bytes(self) -> bytes:
        """获取缩略图字节"""
        return self._thumbnail_bytes
    
    def set_thumbnail_bytes(self, thumbnail: bytes):
        """设置缩略图字节"""
        self._thumbnail_bytes = thumbnail
    
    def remote_media_url(self, url: str):
        """设置远程媒体URL"""
        self._remote_media_url = url
        return self
    
    def get_remote_media_url(self) -> str:
        """获取远程媒体URL"""
        return self._remote_media_url
    
    def set_remote_media_url(self, url: str):
        """设置远程媒体URL"""
        self._remote_media_url = url
    
    def get_content_type(self) -> int:
        return ContentType.Image
    
    def get_persist_flag(self) -> int:
        return PersistFlag.Persist_And_Count
    
    def encode(self) -> MessagePayload:
        payload = super().encode()
        payload.mediaType = 1  # IMAGE
        payload.remoteMediaUrl = self._remote_media_url
        if self._thumbnail_bytes:
            payload.base64edData = base64.b64encode(self._thumbnail_bytes).decode('utf-8')
        return payload
    
    def decode(self, payload: MessagePayload):
        super().decode(payload)
        self._remote_media_url = payload.remoteMediaUrl if payload.remoteMediaUrl else ""
        if payload.base64edData:
            try:
                self._thumbnail_bytes = base64.b64decode(payload.base64edData)
            except:
                pass


class VideoMessageContent(MessageContent):
    """视频消息内容类"""
    
    def __init__(self):
        super().__init__()
        self._thumbnail_bytes = b""
        self._duration = 0
        self._remote_media_url = ""
    
    def thumbnail_bytes(self, thumbnail: bytes):
        """设置缩略图字节"""
        self._thumbnail_bytes = thumbnail
        return self
    
    def get_thumbnail_bytes(self) -> bytes:
        return self._thumbnail_bytes
    
    def set_thumbnail_bytes(self, thumbnail: bytes):
        self._thumbnail_bytes = thumbnail
    
    def duration(self, duration: int):
        """设置时长"""
        self._duration = duration
        return self
    
    def get_duration(self) -> int:
        return self._duration
    
    def set_duration(self, duration: int):
        self._duration = duration
    
    def remote_media_url(self, url: str):
        """设置远程媒体URL"""
        self._remote_media_url = url
        return self
    
    def get_remote_media_url(self) -> str:
        return self._remote_media_url
    
    def set_remote_media_url(self, url: str):
        self._remote_media_url = url
    
    def get_content_type(self) -> int:
        return ContentType.Video
    
    def get_persist_flag(self) -> int:
        return PersistFlag.Persist_And_Count
    
    def encode(self) -> MessagePayload:
        payload = super().encode()
        payload.mediaType = 3  # VIDEO
        payload.remoteMediaUrl = self._remote_media_url
        payload.content = str(self._duration)
        if self._thumbnail_bytes:
            payload.base64edData = base64.b64encode(self._thumbnail_bytes).decode('utf-8')
        return payload
    
    def decode(self, payload: MessagePayload):
        super().decode(payload)
        self._remote_media_url = payload.remoteMediaUrl if payload.remoteMediaUrl else ""
        try:
            self._duration = int(payload.content) if payload.content else 0
        except:
            self._duration = 0
        if payload.base64edData:
            try:
                self._thumbnail_bytes = base64.b64decode(payload.base64edData)
            except:
                pass


class FileMessageContent(MessageContent):
    """文件消息内容类"""
    
    def __init__(self):
        super().__init__()
        self._name = ""
        self._size = 0
        self._remote_media_url = ""
    
    def name(self, name: str):
        """设置文件名"""
        self._name = name
        return self
    
    def get_name(self) -> str:
        return self._name
    
    def set_name(self, name: str):
        self._name = name
    
    def size(self, size: int):
        """设置文件大小"""
        self._size = size
        return self
    
    def get_size(self) -> int:
        return self._size
    
    def set_size(self, size: int):
        self._size = size
    
    def remote_media_url(self, url: str):
        """设置远程媒体URL"""
        self._remote_media_url = url
        return self
    
    def get_remote_media_url(self) -> str:
        return self._remote_media_url
    
    def set_remote_media_url(self, url: str):
        self._remote_media_url = url
    
    def get_content_type(self) -> int:
        return ContentType.File
    
    def get_persist_flag(self) -> int:
        return PersistFlag.Persist_And_Count
    
    def encode(self) -> MessagePayload:
        payload = super().encode()
        payload.mediaType = 4  # FILE
        payload.remoteMediaUrl = self._remote_media_url
        payload.searchableContent = self._name
        payload.content = str(self._size)
        return payload
    
    def decode(self, payload: MessagePayload):
        super().decode(payload)
        self._remote_media_url = payload.remoteMediaUrl if payload.remoteMediaUrl else ""
        self._name = payload.searchableContent if payload.searchableContent else ""
        try:
            self._size = int(payload.content) if payload.content else 0
        except:
            self._size = 0


class LocationMessageContent(MessageContent):
    """位置消息内容类"""
    
    def __init__(self):
        super().__init__()
        self._thumbnail_byte = b""
        self._title = ""
        self._latitude = 0.0
        self._longitude = 0.0
    
    def thumbnail_byte(self, thumbnail: bytes):
        """设置缩略图字节"""
        self._thumbnail_byte = thumbnail
        return self
    
    def title(self, title: str):
        """设置标题"""
        self._title = title
        return self
    
    def latitude(self, latitude: float):
        """设置纬度"""
        self._latitude = latitude
        return self
    
    def longitude(self, longitude: float):
        """设置经度"""
        self._longitude = longitude
        return self
    
    def get_content_type(self) -> int:
        return ContentType.Location
    
    def get_persist_flag(self) -> int:
        return PersistFlag.Persist_And_Count
    
    def encode(self) -> MessagePayload:
        payload = super().encode()
        payload.searchableContent = self._title
        payload.content = f"{self._latitude},{self._longitude}"
        if self._thumbnail_byte:
            payload.base64edData = base64.b64encode(self._thumbnail_byte).decode('utf-8')
        return payload
    
    def decode(self, payload: MessagePayload):
        super().decode(payload)
        self._title = payload.searchableContent if payload.searchableContent else ""
        if payload.content:
            try:
                parts = payload.content.split(',')
                if len(parts) >= 2:
                    self._latitude = float(parts[0])
                    self._longitude = float(parts[1])
            except:
                pass
        if payload.base64edData:
            try:
                self._thumbnail_byte = base64.b64decode(payload.base64edData)
            except:
                pass


class StickerMessageContent(MessageContent):
    """动态表情消息内容类"""
    
    def __init__(self):
        super().__init__()
        self._width = 0
        self._height = 0
        self._remote_media_url = ""
    
    def width(self, width: int):
        self._width = width
        return self
    
    def height(self, height: int):
        self._height = height
        return self
    
    def remote_media_url(self, url: str):
        self._remote_media_url = url
        return self
    
    def get_content_type(self) -> int:
        return ContentType.Sticker
    
    def get_persist_flag(self) -> int:
        return PersistFlag.Persist_And_Count
    
    def encode(self) -> MessagePayload:
        payload = super().encode()
        payload.remoteMediaUrl = self._remote_media_url
        payload.content = f"{self._width},{self._height}"
        return payload
    
    def decode(self, payload: MessagePayload):
        super().decode(payload)
        self._remote_media_url = payload.remoteMediaUrl if payload.remoteMediaUrl else ""
        if payload.content:
            try:
                parts = payload.content.split(',')
                if len(parts) >= 2:
                    self._width = int(parts[0])
                    self._height = int(parts[1])
            except:
                pass


class LinkMessageContent(MessageContent):
    """链接消息内容类"""
    
    def __init__(self):
        super().__init__()
        self._title = ""
        self._content_digest = ""
        self._url = ""
        self._thumbnail_url = ""
    
    def title(self, title: str):
        self._title = title
        return self
    
    def content_digest(self, digest: str):
        self._content_digest = digest
        return self
    
    def url(self, url: str):
        self._url = url
        return self
    
    def thumbnail_url(self, url: str):
        self._thumbnail_url = url
        return self
    
    def get_content_type(self) -> int:
        return ContentType.Link
    
    def get_persist_flag(self) -> int:
        return PersistFlag.Persist_And_Count
    
    def encode(self) -> MessagePayload:
        payload = super().encode()
        payload.searchableContent = self._title
        payload.content = self._content_digest
        json_str = json.dumps({"url": self._url, "thumb": self._thumbnail_url}, ensure_ascii=False)
        payload.base64edData = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
        return payload
    
    def decode(self, payload: MessagePayload):
        super().decode(payload)
        self._title = payload.searchableContent if payload.searchableContent else ""
        self._content_digest = payload.content if payload.content else ""
        if payload.base64edData:
            try:
                json_str = base64.b64decode(payload.base64edData).decode('utf-8')
                data = json.loads(json_str)
                self._url = data.get("url", "")
                self._thumbnail_url = data.get("thumb", "")
            except:
                pass


class CardMessageContent(MessageContent):
    """名片消息内容类"""
    
    def __init__(self):
        super().__init__()
        self._type = 0  # 0用户，1群组，2聊天室，3频道
        self._target = ""
        self._name = ""
        self._portrait = ""
        self._display_name = ""
        self._from = ""
    
    def type(self, type_val: int):
        self._type = type_val
        return self
    
    def target(self, target: str):
        self._target = target
        return self
    
    def name(self, name: str):
        self._name = name
        return self
    
    def portrait(self, portrait: str):
        self._portrait = portrait
        return self
    
    def display_name(self, display_name: str):
        self._display_name = display_name
        return self
    
    def from_user(self, from_user: str):
        self._from = from_user
        return self
    
    def get_content_type(self) -> int:
        return ContentType.Name_Card
    
    def get_persist_flag(self) -> int:
        return PersistFlag.Persist_And_Count
    
    def encode(self) -> MessagePayload:
        payload = super().encode()
        payload.content = self._target
        json_str = json.dumps({
            "t": self._type,
            "n": self._name,
            "d": self._display_name,
            "p": self._portrait,
            "f": self._from
        }, ensure_ascii=False)
        payload.base64edData = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
        return payload
    
    def decode(self, payload: MessagePayload):
        super().decode(payload)
        self._target = payload.content if payload.content else ""
        if payload.base64edData:
            try:
                json_str = base64.b64decode(payload.base64edData).decode('utf-8')
                data = json.loads(json_str)
                self._type = data.get("t", 0)
                self._name = data.get("n", "")
                self._display_name = data.get("d", "")
                self._portrait = data.get("p", "")
                self._from = data.get("f", "")
            except:
                pass


class TipNotificationMessageContent(MessageContent):
    """提醒消息内容类"""
    
    def __init__(self, tip: str = ""):
        super().__init__()
        self._tip = tip
    
    def tip(self, tip: str):
        self._tip = tip
        return self
    
    def get_tip(self) -> str:
        return self._tip
    
    def set_tip(self, tip: str):
        self._tip = tip
    
    def get_content_type(self) -> int:
        return ContentType.Tip
    
    def get_persist_flag(self) -> int:
        return PersistFlag.Persist
    
    def encode(self) -> MessagePayload:
        payload = super().encode()
        payload.content = self._tip
        return payload
    
    def decode(self, payload: MessagePayload):
        super().decode(payload)
        self._tip = payload.content if payload.content else ""


class TypingMessageContent(MessageContent):
    """正在输入消息内容类"""
    
    def __init__(self, typing_type: int = 0):
        super().__init__()
        self._typing_type = typing_type
    
    def get_content_type(self) -> int:
        return ContentType.Typing
    
    def get_persist_flag(self) -> int:
        return PersistFlag.NOT_PERSIST
    
    def encode(self) -> MessagePayload:
        payload = super().encode()
        payload.content = str(self._typing_type)
        return payload
    
    def decode(self, payload: MessagePayload):
        super().decode(payload)
        try:
            self._typing_type = int(payload.content) if payload.content else 0
        except:
            self._typing_type = 0


class RecallMessageContent(MessageContent):
    """撤回消息内容类"""
    
    def __init__(self):
        super().__init__()
        self._message_uid = 0
    
    def get_content_type(self) -> int:
        return ContentType.Recall
    
    def get_persist_flag(self) -> int:
        return PersistFlag.Persist
    
    def encode(self) -> MessagePayload:
        payload = super().encode()
        payload.content = str(self._message_uid)
        return payload
    
    def decode(self, payload: MessagePayload):
        super().decode(payload)
        try:
            self._message_uid = int(payload.content) if payload.content else 0
        except:
            self._message_uid = 0


class DeleteMessageContent(MessageContent):
    """删除消息内容类"""
    
    def __init__(self):
        super().__init__()
        self._message_uid = 0
    
    def get_content_type(self) -> int:
        return ContentType.Delete
    
    def get_persist_flag(self) -> int:
        return PersistFlag.Persist
    
    def encode(self) -> MessagePayload:
        payload = super().encode()
        payload.content = str(self._message_uid)
        return payload
    
    def decode(self, payload: MessagePayload):
        super().decode(payload)
        try:
            self._message_uid = int(payload.content) if payload.content else 0
        except:
            self._message_uid = 0


class RichNotificationMessageContent(MessageContent):
    """富通知消息内容类"""
    
    def __init__(self, title: str = "", content: str = "", url: str = ""):
        super().__init__()
        self._title = title
        self._content = content
        self._url = url
        self._remark = ""
        self._ex_name = ""
        self._app_id = ""
        self._items = []
    
    def title(self, title: str):
        self._title = title
        return self
    
    def content(self, content: str):
        self._content = content
        return self
    
    def url(self, url: str):
        self._url = url
        return self
    
    def remark(self, remark: str):
        self._remark = remark
        return self
    
    def ex_name(self, ex_name: str):
        self._ex_name = ex_name
        return self
    
    def app_id(self, app_id: str):
        self._app_id = app_id
        return self
    
    def add_item(self, key: str, value: str, color: str = ""):
        self._items.append({"key": key, "value": value, "color": color})
        return self
    
    def get_content_type(self) -> int:
        return ContentType.Rich_Notification
    
    def get_persist_flag(self) -> int:
        return PersistFlag.Persist_And_Count
    
    def encode(self) -> MessagePayload:
        payload = super().encode()
        payload.searchableContent = self._title
        payload.pushContent = self._content
        data = {
            "url": self._url,
            "remark": self._remark,
            "exName": self._ex_name,
            "appId": self._app_id,
            "items": self._items
        }
        json_str = json.dumps(data, ensure_ascii=False)
        payload.base64edData = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
        return payload
    
    def decode(self, payload: MessagePayload):
        super().decode(payload)
        self._title = payload.searchableContent if payload.searchableContent else ""
        self._content = payload.pushContent if payload.pushContent else ""
        if payload.base64edData:
            try:
                json_str = base64.b64decode(payload.base64edData).decode('utf-8')
                data = json.loads(json_str)
                self._url = data.get("url", "")
                self._remark = data.get("remark", "")
                self._ex_name = data.get("exName", "")
                self._app_id = data.get("appId", "")
                self._items = data.get("items", [])
            except:
                pass


class StreamTextGeneratingMessageContent(MessageContent):
    """流式文本生成中消息内容类"""
    
    def __init__(self, text: str = "", stream_id: str = ""):
        super().__init__()
        self._text = text
        self._stream_id = stream_id
    
    def get_content_type(self) -> int:
        return ContentType.StreamingText_Generationg
    
    def get_persist_flag(self) -> int:
        return PersistFlag.Persist_And_Count
    
    def encode(self) -> MessagePayload:
        payload = super().encode()
        payload.content = json.dumps({"text": self._text, "streamId": self._stream_id}, ensure_ascii=False)
        return payload
    
    def decode(self, payload: MessagePayload):
        super().decode(payload)
        if payload.content:
            try:
                data = json.loads(payload.content)
                self._text = data.get("text", "")
                self._stream_id = data.get("streamId", "")
            except:
                pass


class StreamTextGeneratedMessageContent(MessageContent):
    """流式文本生成完成消息内容类"""
    
    def __init__(self, text: str = "", stream_id: str = ""):
        super().__init__()
        self._text = text
        self._stream_id = stream_id
    
    def get_content_type(self) -> int:
        return ContentType.StreamingText_Generated
    
    def get_persist_flag(self) -> int:
        return PersistFlag.Persist_And_Count
    
    def encode(self) -> MessagePayload:
        payload = super().encode()
        payload.content = json.dumps({"text": self._text, "streamId": self._stream_id}, ensure_ascii=False)
        return payload
    
    def decode(self, payload: MessagePayload):
        super().decode(payload)
        if payload.content:
            try:
                data = json.loads(payload.content)
                self._text = data.get("text", "")
                self._stream_id = data.get("streamId", "")
            except:
                pass


class ArticleContent(MessageContent):
    """文章消息内容类（频道使用）"""
    
    def __init__(self, title: str = "", cover: str = "", digest: str = "", content: str = "", url: str = "", is_original: bool = True):
        super().__init__()
        self._title = title
        self._cover = cover
        self._digest = digest
        self._content = content
        self._url = url
        self._is_original = is_original
        self._sub_articles = []
    
    def add_sub_article(self, title: str, cover: str, digest: str, content: str, url: str, is_original: bool = False):
        """添加子文章"""
        self._sub_articles.append({
            "title": title,
            "cover": cover,
            "digest": digest,
            "content": content,
            "url": url,
            "isOriginal": is_original
        })
        return self
    
    def get_content_type(self) -> int:
        return ContentType.Articles
    
    def get_persist_flag(self) -> int:
        return PersistFlag.Persist_And_Count
    
    def encode(self) -> MessagePayload:
        payload = super().encode()
        payload.searchableContent = self._title
        
        data = {
            "title": self._title,
            "cover": self._cover,
            "digest": self._digest,
            "content": self._content,
            "url": self._url,
            "isOriginal": self._is_original,
            "subArticles": self._sub_articles
        }
        json_str = json.dumps(data, ensure_ascii=False)
        payload.base64edData = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
        return payload
    
    def decode(self, payload: MessagePayload):
        super().decode(payload)
        self._title = payload.searchableContent if payload.searchableContent else ""
        if payload.base64edData:
            try:
                json_str = base64.b64decode(payload.base64edData).decode('utf-8')
                data = json.loads(json_str)
                self._cover = data.get("cover", "")
                self._digest = data.get("digest", "")
                self._content = data.get("content", "")
                self._url = data.get("url", "")
                self._is_original = data.get("isOriginal", True)
                self._sub_articles = data.get("subArticles", [])
            except:
                pass


class UnknownMessageContent(MessageContent):
    """未知消息内容类"""
    
    def __init__(self):
        super().__init__()
    
    def get_content_type(self) -> int:
        return ContentType.Unknown
    
    def get_persist_flag(self) -> int:
        return PersistFlag.Persist
