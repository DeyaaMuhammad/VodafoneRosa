#!/usr/bin/env python
# -- coding: UTF-8 --
import re
import json
import requests
from user_agent import generate_user_agent

try:
    # Fix UTF8 output issues on Windows console.
    from win_unicode_console import enable
    enable()
except ImportError:
    pass

__API__ = json.loads(
            open('api.json').read()
        )


class API(object):
    """docstring for API."""
    def __init__(self, **args):

        self.request = None
        self.response = None
        self.api = None

        self.variables = {
                "msisdn": "",
                "access-token": "",
                "ua": "",
                "cookie": "",
                "customerId": "",
                "userType": "",
                }

        self.variables['ua'] = generate_user_agent()

        for arg in args:

            if arg in self.variables and args[arg] is not None:
                self.variables[arg] = args[arg]

            if hasattr(self, arg):
                setattr(self, arg, args[arg])



    def findVARS(self,raw):
        return re.findall(r'\[(.*?)\]', raw)


    def renderVARS(self,raw):
        ''' Render variables in __API__ elements'''
        buffer = raw
        VARS = self.findVARS(raw)

        if len(VARS) > 0:
            for VAR in VARS:
                if VAR in self.variables:
                    buffer = buffer.replace('['+VAR+']', self.variables[VAR])

        return buffer


    def buildRequest(self,api='token'):
        '''Change request parameters "URL,HEADERS,PAYLOAD" with proper data'''
        METHOD = __API__[api]['METHOD'].lower()
        URL = self.renderVARS(__API__[api]['URL'])
        HEADERS = json.loads(self.renderVARS(json.dumps(__API__[api]['HEADERS'])))
        PAYLOAD = self.renderVARS(__API__[api]['PAYLOAD'])
        REQUEST = {
            "METHOD": METHOD,
            "URL": URL,
            "HEADERS": HEADERS,
            "PAYLOAD": PAYLOAD
        }
        self.request = REQUEST
        return REQUEST


    def sendRequest(self,api='token'):
        '''Send request using requests lib and change method based-on METHOD'''
        REQUEST = self.buildRequest(api)
        RESPONSE = getattr(requests, REQUEST['METHOD'])(
            url=REQUEST['URL'],
            headers=REQUEST['HEADERS'],
            data=REQUEST['PAYLOAD'],
        )
        self.response = RESPONSE
        return RESPONSE


    def call(self, api='token'):
        return self.sendRequest(api)
