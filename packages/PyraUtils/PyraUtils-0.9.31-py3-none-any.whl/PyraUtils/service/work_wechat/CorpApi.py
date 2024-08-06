# -*- coding: utf-8 -*-

from .AbstractApi import AbstractApi
from .CorpApiType import *

class CorpApi(AbstractApi):
    def __init__(self, corpid, corpsecret):
        """初始化企业API，设置企业ID和秘钥"""
        super().__init__()
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.access_token = None

    def refreshAccessToken(self):
        """刷新访问令牌"""
        params = {
            'corpid': self.corpid,
            'corpsecret': self.corpsecret,
        }
        response = self.httpCall(CORP_API_TYPE['GET_ACCESS_TOKEN'], params)
        self.access_token = response.get('access_token')

    def getAccessToken(self):
        """获取访问令牌，如果没有则刷新"""
        if self.access_token is None:
            self.refreshAccessToken()
        return self.access_token

    def get_user(self, access_token, userid):
        params = {
            'access_token': access_token,
            'userid': userid
        }
        response = self.httpCall(CORP_API_TYPE['USER_GET'], params)
        return response

    def get_userid_by_email(self, access_token, email, email_type=1):
        params = {
            'access_token': access_token
        }
        body = {
            'email': email,
            'email_type': email_type
        }
        response = self.httpCall(CORP_API_TYPE['USERID_BY_EMAIL_POST'], params, req_body=body)
        return response

    def get_user_list_id(self, access_token):
        params = {
            'access_token': access_token
        }
        response = self.httpCall(CORP_API_TYPE['USER_LIST_ID'], params)
        return response

    def get_approval_detail(self, access_token, sp_no):
        params = {
            'access_token': access_token
        }
        body = {
            'sp_no': sp_no
        }
        response = self.httpCall(CORP_API_TYPE['APPROVAL_DETAIL'], params, req_body=body)
        return response

    def sendMessage(self, access_token, touser, agentid, msgtype="text", safe=0, **kwargs):
        params = {
            'access_token': access_token
        }
        body = {
            'touser': touser,
            'msgtype': msgtype,
            'agentid': agentid,
            'safe': safe,
            'enable_duplicate_check': 0,
            'duplicate_check_interval': 1800
        }
        if msgtype == "text":
            body['text'] = {'content': kwargs['msg_content']}
        elif msgtype == "markdown":
            body['markdown'] = {'content': kwargs['msg_content']}
        elif msgtype == "textcard":
            body['textcard'] = {
                'title': kwargs['msg_title'],
                'description': kwargs['msg_content'],
                'url': kwargs['msg_url'],
                'btntxt': '详情'
            }
        elif msgtype == "template_card":
            pass  # Add template card details here if needed
        response = self.httpCall(CORP_API_TYPE['MESSAGE_SEND'], params, req_body=body)
        return response
