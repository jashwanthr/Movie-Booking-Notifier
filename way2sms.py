#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 12:56:33 2019

@author: Jashwanth
"""
import requests, json


class WAY2SMS():

    def __init__(self):
        """Constructor : Initializes necessary variables."""
        self.URL = 'http://www.way2sms.com/api/v1/sendCampaign'

    def sendPostRequest(self, phoneNumber, textMessage):
        """Sends sms using Way2SMS API. Returns the response code from API."""
        req_params = {
            'apikey': '<Way2SMS API Key>',
            'secret': '<Secret key for above API Key>',
            'usetype': 'stage',
            'phone': phoneNumber,
            'message': textMessage,
            'senderid': '------'
        }
        response = requests.post(self.URL, req_params)
        return json.loads(response.text)['code']
