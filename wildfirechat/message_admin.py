"""
消息管理类
对应Java SDK中的 cn.wildfirechat.sdk.MessageAdmin
"""
from typing import List
from .api_path import APIPath
from .http_utils import AdminHttpUtils
from .models import (
    IMResult, Conversation, MessagePayload, SendMessageData, SendMessageResult,
    RecallMessageData, DeleteMessageData, UpdateMessageContentData, BroadMessageData,
    BroadMessageResult, MulticastMessageData, MultiMessageResult, RecallMultiCastMessageData,
    OutputMessageData, OutputTimestamp, InputClearUserMessages, InputUserConversation,
    InputMessageUid, InputGetConvReadTime, InputUserId
)


class MessageAdmin:
    """消息管理类"""
    
    @staticmethod
    def send_message(sender: str, conversation: Conversation, payload: MessagePayload,
                     to_users: List[str] = None, is_user_message: bool = False) -> IMResult:
        """
        发送消息
        
        :param sender: 发送者用户ID
        :param conversation: 会话信息
        :param payload: 消息内容
        :param to_users: 接收用户ID列表，None表示发送给会话中所有用户
        :param is_user_message: 是否为用户消息
        :return: 发送结果，包含消息ID
        """
        path = APIPath.Msg_Send
        message_data = SendMessageData(
            sender=sender,
            conv=conversation,
            payload=payload,
            toUsers=to_users if to_users else [],
            userMessage=is_user_message
        )
        
        # 检查文本消息的payload格式
        if payload.type == 1 and (not payload.searchableContent or payload.searchableContent == ""):
            print("Payload错误，Payload格式应该跟客户端消息encode出来的Payload对齐，这样客户端才能正确识别。"
                  "比如文本消息，文本需要放到searchableContent属性。请与客户端同事确认Payload的格式，"
                  "或去 https://gitee.com/wfchat/android-chat/tree/master/client/src/main/java/cn/wildfirechat/message "
                  "找到消息encode的实现方法！")
        
        return AdminHttpUtils.http_json_post(path, message_data, SendMessageResult)
    
    @staticmethod
    def recall_message(operator: str, message_uid: int) -> IMResult:
        """
        撤回消息
        
        :param operator: 操作者用户ID
        :param message_uid: 消息UID
        :return: 撤回结果
        """
        path = APIPath.Msg_Recall
        message_data = RecallMessageData(operator=operator, messageUid=message_uid)
        return AdminHttpUtils.http_json_post(path, message_data, str)
    
    @staticmethod
    def delete_message(message_uid: int) -> IMResult:
        """
        删除消息（仅专业版支持）
        
        :param message_uid: 消息UID
        :return: 删除结果
        """
        path = APIPath.Msg_Delete
        delete_message_data = DeleteMessageData(messageUid=message_uid)
        return AdminHttpUtils.http_json_post(path, delete_message_data, type(None))
    
    @staticmethod
    def clear_user_messages(user_id: str, conversation: Conversation,
                            from_time: int, to_time: int) -> IMResult:
        """
        清除用户消息（仅专业版支持）
        
        :param user_id: 用户ID
        :param conversation: 会话信息
        :param from_time: 起始时间
        :param to_time: 结束时间
        :return: 清除结果
        """
        path = APIPath.Msg_Clear_By_User
        clear_user_messages = InputClearUserMessages(
            userId=user_id,
            conversation=conversation,
            fromTime=from_time,
            toTime=to_time
        )
        return AdminHttpUtils.http_json_post(path, clear_user_messages, type(None))
    
    @staticmethod
    def update_message_content(operator: str, message_uid: int, payload: MessagePayload,
                               distribute: bool) -> IMResult:
        """
        更新消息内容（仅专业版支持）
        
        :param operator: 操作者用户ID
        :param message_uid: 消息UID
        :param payload: 新的消息内容
        :param distribute: 是否分发更新
        :return: 更新结果
        """
        path = APIPath.Msg_Update
        update_message_content_data = UpdateMessageContentData(
            operator=operator,
            messageUid=message_uid,
            payload=payload,
            distribute=1 if distribute else 0,
            updateTimestamp=0
        )
        return AdminHttpUtils.http_json_post(path, update_message_content_data, type(None))
    
    @staticmethod
    def clear_conversation(user_id: str, conversation: Conversation) -> IMResult:
        """
        清除会话（仅专业版支持）
        
        :param user_id: 用户ID
        :param conversation: 会话信息
        :return: 清除结果
        """
        path = APIPath.Conversation_Delete
        input_data = InputUserConversation(userId=user_id, conversation=conversation)
        return AdminHttpUtils.http_json_post(path, input_data, type(None))
    
    @staticmethod
    def get_message(message_uid: int) -> IMResult:
        """
        获取单条消息
        
        :param message_uid: 消息UID
        :return: 消息数据
        """
        path = APIPath.Msg_GetOne
        input_message_uid = InputMessageUid(messageUid=message_uid)
        return AdminHttpUtils.http_json_post(path, input_message_uid, OutputMessageData)
    
    @staticmethod
    def recall_broadcast_message(operator: str, message_uid: int) -> IMResult:
        """
        撤回广播消息（仅专业版支持）
        
        :param operator: 操作者用户ID
        :param message_uid: 消息UID
        :return: 撤回结果
        """
        path = APIPath.Msg_RecallBroadCast
        message_data = RecallMessageData(operator=operator, messageUid=message_uid)
        return AdminHttpUtils.http_json_post(path, message_data, type(None))
    
    @staticmethod
    def recall_multicast_message(operator: str, message_uid: int, receivers: List[str]) -> IMResult:
        """
        撤回群发消息
        
        :param operator: 操作者用户ID
        :param message_uid: 消息UID
        :param receivers: 接收者ID列表
        :return: 撤回结果
        """
        path = APIPath.Msg_RecallMultiCast
        message_data = RecallMultiCastMessageData(
            operator=operator,
            messageUid=message_uid,
            receivers=receivers
        )
        return AdminHttpUtils.http_json_post(path, message_data, type(None))
    
    @staticmethod
    def delete_broadcast_message(operator: str, message_uid: int) -> IMResult:
        """
        删除广播消息（仅专业版支持）
        
        :param operator: 操作者用户ID
        :param message_uid: 消息UID
        :return: 删除结果
        """
        path = APIPath.Msg_DeleteBroadCast
        message_data = RecallMessageData(operator=operator, messageUid=message_uid)
        return AdminHttpUtils.http_json_post(path, message_data, type(None))
    
    @staticmethod
    def delete_multicast_message(operator: str, message_uid: int, receivers: List[str]) -> IMResult:
        """
        删除群发消息
        
        :param operator: 操作者用户ID
        :param message_uid: 消息UID
        :param receivers: 接收者ID列表
        :return: 删除结果
        """
        path = APIPath.Msg_DeleteMultiCast
        message_data = RecallMultiCastMessageData(
            operator=operator,
            messageUid=message_uid,
            receivers=receivers
        )
        return AdminHttpUtils.http_json_post(path, message_data, type(None))
    
    @staticmethod
    def broadcast_message(sender: str, line: int, payload: MessagePayload) -> IMResult:
        """
        广播消息（仅专业版支持）
        
        :param sender: 发送者用户ID
        :param line: 线路
        :param payload: 消息内容
        :return: 广播结果
        """
        path = APIPath.Msg_Broadcast
        message_data = BroadMessageData(sender=sender, line=line, payload=payload)
        return AdminHttpUtils.http_json_post(path, message_data, BroadMessageResult)
    
    @staticmethod
    def multicast_message(sender: str, receivers: List[str], line: int,
                          payload: MessagePayload) -> IMResult:
        """
        群发消息
        
        :param sender: 发送者用户ID
        :param receivers: 接收者ID列表
        :param line: 线路
        :param payload: 消息内容
        :return: 群发结果
        """
        path = APIPath.Msg_Multicast
        message_data = MulticastMessageData(
            sender=sender,
            targets=receivers,
            line=line,
            payload=payload
        )
        return AdminHttpUtils.http_json_post(path, message_data, MultiMessageResult)
    
    @staticmethod
    def get_conversation_read_timestamp(user_id: str, conversation: Conversation) -> IMResult:
        """
        获取会话已读时间戳
        
        :param user_id: 用户ID
        :param conversation: 会话信息
        :return: 已读时间戳
        """
        path = APIPath.Msg_ConvRead
        input_data = InputGetConvReadTime(
            userId=user_id,
            conversationType=conversation.type,
            target=conversation.target,
            line=conversation.line
        )
        return AdminHttpUtils.http_json_post(path, input_data, OutputTimestamp)
    
    @staticmethod
    def get_message_delivery(user_id: str) -> IMResult:
        """
        获取消息投递时间戳
        
        :param user_id: 用户ID
        :return: 投递时间戳
        """
        path = APIPath.Msg_Delivery
        input_data = InputUserId(userId=user_id)
        return AdminHttpUtils.http_json_post(path, input_data, OutputTimestamp)
