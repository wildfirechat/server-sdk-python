"""
群组管理类
对应Java SDK中的 cn.wildfirechat.sdk.GroupAdmin
"""
from typing import List, Optional
from .api_path import APIPath
from .http_utils import AdminHttpUtils
from .general_admin import GeneralAdmin
from .models import (
    IMResult, PojoGroupInfo, PojoGroupMember, PojoGroup, OutputCreateGroupResult,
    PojoGroupInfoList, OutputGroupMemberList, OutputGroupIds, InputCreateGroup,
    InputGetGroup, InputGetGroupMember, InputAddGroupMember, InputSetGroupManager,
    InputMuteGroupMember, InputKickoffGroupMember, InputQuitGroup, InputSetGroupMemberAlias,
    InputSetGroupMemberExtra, InputDismissGroup, InputTransferGroup, InputModifyGroupInfo,
    InputGetUserGroupByType, StringPairPojo, UserSettingPojo, MessagePayload
)


class GroupAdmin:
    """群组管理类"""
    
    @staticmethod
    def create_group(operator: str, group_info: PojoGroupInfo, members: List[PojoGroupMember],
                     member_extra: str = None, to_lines: List[int] = None,
                     notify_message: MessagePayload = None) -> IMResult:
        """
        创建群组
        
        :param operator: 操作者用户ID
        :param group_info: 群组信息
        :param members: 群组成员列表
        :param member_extra: 成员额外信息
        :param to_lines: 消息同步到的线路列表
        :param notify_message: 通知消息
        :return: 创建结果，包含群组ID
        """
        path = APIPath.Create_Group
        pojo_group = PojoGroup(group_info=group_info, members=members)
        create_group = InputCreateGroup(
            group=pojo_group,
            operator=operator,
            member_extra=member_extra if member_extra else "",
            to_lines=to_lines if to_lines else [],
            notify_message=notify_message
        )
        return AdminHttpUtils.http_json_post(path, create_group, OutputCreateGroupResult)
    
    @staticmethod
    def get_group_info(group_id: str) -> IMResult:
        """
        获取群组信息
        
        :param group_id: 群组ID
        :return: 群组信息
        """
        path = APIPath.Group_Get_Info
        input_data = InputGetGroup(groupId=group_id)
        return AdminHttpUtils.http_json_post(path, input_data, PojoGroupInfo)
    
    @staticmethod
    def batch_group_infos(group_ids: List[str]) -> IMResult:
        """
        批量获取群组信息
        
        :param group_ids: 群组ID列表
        :return: 群组信息列表
        """
        path = APIPath.Group_Batch_Info
        return AdminHttpUtils.http_json_post(path, group_ids, PojoGroupInfoList)
    
    @staticmethod
    def dismiss_group(operator: str, group_id: str, to_lines: List[int] = None,
                      notify_message: MessagePayload = None) -> IMResult:
        """
        解散群组
        
        :param operator: 操作者用户ID
        :param group_id: 群组ID
        :param to_lines: 消息同步到的线路列表
        :param notify_message: 通知消息
        :return: 解散结果
        """
        path = APIPath.Group_Dismiss
        dismiss_group = InputDismissGroup(
            operator=operator,
            group_id=group_id,
            to_lines=to_lines if to_lines else [],
            notify_message=notify_message
        )
        return AdminHttpUtils.http_json_post(path, dismiss_group, type(None))
    
    @staticmethod
    def transfer_group(operator: str, group_id: str, new_owner: str,
                       to_lines: List[int] = None, notify_message: MessagePayload = None) -> IMResult:
        """
        转让群组
        
        :param operator: 操作者用户ID
        :param group_id: 群组ID
        :param new_owner: 新群主用户ID
        :param to_lines: 消息同步到的线路列表
        :param notify_message: 通知消息
        :return: 转让结果
        """
        path = APIPath.Group_Transfer
        transfer_group = InputTransferGroup(
            operator=operator,
            group_id=group_id,
            new_owner=new_owner,
            to_lines=to_lines if to_lines else [],
            notify_message=notify_message
        )
        return AdminHttpUtils.http_json_post(path, transfer_group, type(None))
    
    @staticmethod
    def modify_group_info(operator: str, group_id: str, modify_type: int, value: str,
                          to_lines: List[int] = None, notify_message: MessagePayload = None) -> IMResult:
        """
        修改群组信息
        
        :param operator: 操作者用户ID
        :param group_id: 群组ID
        :param modify_type: 修改信息类型（ModifyGroupInfoType）
        :param value: 新值
        :param to_lines: 消息同步到的线路列表
        :param notify_message: 通知消息
        :return: 修改结果
        """
        path = APIPath.Group_Modify_Info
        modify_group_info = InputModifyGroupInfo(
            operator=operator,
            group_id=group_id,
            type=modify_type,
            value=value,
            to_lines=to_lines if to_lines else [],
            notify_message=notify_message
        )
        return AdminHttpUtils.http_json_post(path, modify_group_info, type(None))
    
    @staticmethod
    def get_group_members(group_id: str) -> IMResult:
        """
        获取群组成员列表
        
        :param group_id: 群组ID
        :return: 群组成员列表
        """
        path = APIPath.Group_Member_List
        input_data = InputGetGroup(groupId=group_id)
        return AdminHttpUtils.http_json_post(path, input_data, OutputGroupMemberList)
    
    @staticmethod
    def get_group_member(group_id: str, member_id: str) -> IMResult:
        """
        获取群组成员信息
        
        :param group_id: 群组ID
        :param member_id: 成员用户ID
        :return: 群组成员信息
        """
        path = APIPath.Group_Member_Get
        input_data = InputGetGroupMember(groupId=group_id, memberId=member_id)
        return AdminHttpUtils.http_json_post(path, input_data, PojoGroupMember)
    
    @staticmethod
    def add_group_members(operator: str, group_id: str, group_members: List[PojoGroupMember],
                          member_extra: str = None, to_lines: List[int] = None,
                          notify_message: MessagePayload = None) -> IMResult:
        """
        添加群组成员
        
        :param operator: 操作者用户ID
        :param group_id: 群组ID
        :param group_members: 要添加的成员列表
        :param member_extra: 成员额外信息
        :param to_lines: 消息同步到的线路列表
        :param notify_message: 通知消息
        :return: 添加结果
        """
        path = APIPath.Group_Member_Add
        add_group_member = InputAddGroupMember(
            operator=operator,
            group_id=group_id,
            members=group_members,
            memberExtra=member_extra if member_extra else "",
            to_lines=to_lines if to_lines else [],
            notify_message=notify_message
        )
        return AdminHttpUtils.http_json_post(path, add_group_member, type(None))
    
    @staticmethod
    def set_group_manager(operator: str, group_id: str, group_member_ids: List[str],
                          is_manager: bool, to_lines: List[int] = None,
                          notify_message: MessagePayload = None) -> IMResult:
        """
        设置或取消群组管理员
        
        :param operator: 操作者用户ID
        :param group_id: 群组ID
        :param group_member_ids: 成员用户ID列表
        :param is_manager: true-设置为管理员，false-取消管理员
        :param to_lines: 消息同步到的线路列表
        :param notify_message: 通知消息
        :return: 设置结果
        """
        path = APIPath.Group_Set_Manager
        input_data = InputSetGroupManager(
            operator=operator,
            group_id=group_id,
            members=group_member_ids,
            is_manager=is_manager,
            to_lines=to_lines if to_lines else [],
            notify_message=notify_message
        )
        return AdminHttpUtils.http_json_post(path, input_data, type(None))
    
    @staticmethod
    def mute_group_member(operator: str, group_id: str, group_member_ids: List[str],
                          is_mute: bool, to_lines: List[int] = None,
                          notify_message: MessagePayload = None) -> IMResult:
        """
        禁言或解禁群组成员
        
        :param operator: 操作者用户ID
        :param group_id: 群组ID
        :param group_member_ids: 成员用户ID列表
        :param is_mute: true-禁言，false-解禁
        :param to_lines: 消息同步到的线路列表
        :param notify_message: 通知消息
        :return: 禁言结果
        """
        path = APIPath.Group_Mute_Member
        input_data = InputMuteGroupMember(
            operator=operator,
            group_id=group_id,
            members=group_member_ids,
            is_manager=is_mute,
            to_lines=to_lines if to_lines else [],
            notify_message=notify_message
        )
        return AdminHttpUtils.http_json_post(path, input_data, type(None))
    
    @staticmethod
    def allow_group_member(operator: str, group_id: str, group_member_ids: List[str],
                           is_allow: bool, to_lines: List[int] = None,
                           notify_message: MessagePayload = None) -> IMResult:
        """
        允许或禁止群组成员发言
        
        :param operator: 操作者用户ID
        :param group_id: 群组ID
        :param group_member_ids: 成员用户ID列表
        :param is_allow: true-允许，false-禁止
        :param to_lines: 消息同步到的线路列表
        :param notify_message: 通知消息
        :return: 设置结果
        """
        path = APIPath.Group_Allow_Member
        input_data = InputMuteGroupMember(
            operator=operator,
            group_id=group_id,
            members=group_member_ids,
            is_manager=is_allow,
            to_lines=to_lines if to_lines else [],
            notify_message=notify_message
        )
        return AdminHttpUtils.http_json_post(path, input_data, type(None))
    
    @staticmethod
    def kickoff_group_members(operator: str, group_id: str, group_member_ids: List[str],
                              to_lines: List[int] = None, notify_message: MessagePayload = None) -> IMResult:
        """
        踢出群组成员
        
        :param operator: 操作者用户ID
        :param group_id: 群组ID
        :param group_member_ids: 要踢出的成员用户ID列表
        :param to_lines: 消息同步到的线路列表
        :param notify_message: 通知消息
        :return: 踢出结果
        """
        path = APIPath.Group_Member_Kickoff
        kickoff_group_member = InputKickoffGroupMember(
            operator=operator,
            group_id=group_id,
            members=group_member_ids,
            to_lines=to_lines if to_lines else [],
            notify_message=notify_message
        )
        return AdminHttpUtils.http_json_post(path, kickoff_group_member, type(None))
    
    @staticmethod
    def quit_group(operator: str, group_id: str, to_lines: List[int] = None,
                   notify_message: MessagePayload = None) -> IMResult:
        """
        退出群组
        
        :param operator: 操作者用户ID
        :param group_id: 群组ID
        :param to_lines: 消息同步到的线路列表
        :param notify_message: 通知消息
        :return: 退出结果
        """
        path = APIPath.Group_Member_Quit
        quit_group = InputQuitGroup(
            operator=operator,
            group_id=group_id,
            to_lines=to_lines if to_lines else [],
            notify_message=notify_message
        )
        return AdminHttpUtils.http_json_post(path, quit_group, type(None))
    
    @staticmethod
    def set_group_member_alias(operator: str, group_id: str, member_id: str, alias: str,
                               to_lines: List[int] = None, notify_message: MessagePayload = None) -> IMResult:
        """
        设置群组成员别名
        
        :param operator: 操作者用户ID
        :param group_id: 群组ID
        :param member_id: 成员用户ID
        :param alias: 别名
        :param to_lines: 消息同步到的线路列表
        :param notify_message: 通知消息
        :return: 设置结果
        """
        path = APIPath.Group_Set_Member_Alias
        input_data = InputSetGroupMemberAlias(
            operator=operator,
            group_id=group_id,
            memberId=member_id,
            alias=alias,
            to_lines=to_lines if to_lines else [],
            notify_message=notify_message
        )
        return AdminHttpUtils.http_json_post(path, input_data, type(None))
    
    @staticmethod
    def set_group_member_extra(operator: str, group_id: str, member_id: str, extra: str,
                               to_lines: List[int] = None, notify_message: MessagePayload = None) -> IMResult:
        """
        设置群组成员额外信息
        
        :param operator: 操作者用户ID
        :param group_id: 群组ID
        :param member_id: 成员用户ID
        :param extra: 额外信息
        :param to_lines: 消息同步到的线路列表
        :param notify_message: 通知消息
        :return: 设置结果
        """
        path = APIPath.Group_Set_Member_Extra
        input_data = InputSetGroupMemberExtra(
            operator=operator,
            group_id=group_id,
            memberId=member_id,
            extra=extra,
            to_lines=to_lines if to_lines else [],
            notify_message=notify_message
        )
        return AdminHttpUtils.http_json_post(path, input_data, type(None))
    
    @staticmethod
    def set_group_remark(user_id: str, group_id: str, remark: str) -> IMResult:
        """
        设置群组备注（用户个性化设置）
        
        :param user_id: 用户ID
        :param group_id: 群组ID
        :param remark: 备注内容
        :return: 设置结果
        """
        # 26 是群组备注的scope
        return GeneralAdmin.set_user_setting(user_id, 26, group_id, remark)
    
    @staticmethod
    def get_group_remark(user_id: str, group_id: str) -> IMResult:
        """
        获取群组备注（用户个性化设置）
        
        :param user_id: 用户ID
        :param group_id: 群组ID
        :return: 备注内容
        """
        im_result = GeneralAdmin.get_user_setting(user_id, 26, group_id)
        if im_result.code == 0:
            result = IMResult()
            result.code = im_result.code
            result.msg = im_result.msg
            result.result = im_result.result.value if im_result.result else ""
            return result
        return im_result
    
    @staticmethod
    def set_fav_group(user_id: str, group_id: str, fav: bool) -> IMResult:
        """
        设置群组是否收藏（用户个性化设置）
        
        :param user_id: 用户ID
        :param group_id: 群组ID
        :param fav: true-收藏，false-取消收藏
        :return: 设置结果
        """
        # 6 是收藏群组的scope
        return GeneralAdmin.set_user_setting(user_id, 6, group_id, "1" if fav else "0")
    
    @staticmethod
    def is_fav_group(user_id: str, group_id: str) -> IMResult:
        """
        检查群组是否收藏（用户个性化设置）
        
        :param user_id: 用户ID
        :param group_id: 群组ID
        :return: true-已收藏，false-未收藏
        """
        im_result = GeneralAdmin.get_user_setting(user_id, 6, group_id)
        if im_result.code == 0:
            result = IMResult()
            result.code = im_result.code
            result.msg = im_result.msg
            result.result = im_result.result.value == "1" if im_result.result else False
            return result
        return im_result
    
    @staticmethod
    def get_user_groups(user: str) -> IMResult:
        """
        获取用户的群组列表
        
        :param user: 用户ID
        :return: 用户所属的群组ID列表
        """
        path = APIPath.Get_User_Groups
        input_user_id = {"userId": user}
        return AdminHttpUtils.http_json_post(path, input_user_id, OutputGroupIds)
    
    @staticmethod
    def get_user_groups_by_type(user_id: str, group_member_types: List[int]) -> IMResult:
        """
        根据成员类型获取用户的群组列表
        
        :param user_id: 用户ID
        :param group_member_types: 群组成员类型列表（GroupMemberType）
        :return: 用户所属的群组ID列表
        """
        path = APIPath.Get_User_Groups_By_Type
        input_data = InputGetUserGroupByType(userId=user_id, groupMemberTypes=group_member_types)
        return AdminHttpUtils.http_json_post(path, input_data, OutputGroupIds)
    
    @staticmethod
    def get_common_groups(user1: str, user2: str) -> IMResult:
        """
        获取两个用户的共同群组
        
        :param user1: 用户1的ID
        :param user2: 用户2的ID
        :return: 共同群组ID列表
        """
        path = APIPath.Get_Common_Groups
        input_data = StringPairPojo(first=user1, second=user2)
        return AdminHttpUtils.http_json_post(path, input_data, OutputGroupIds)
