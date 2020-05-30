#!/usr/bin/python

'''
`.......        `....       `.. ..        `.       
`..    `..    `..    `..  `..    `..     `. ..     
`..    `..  `..        `.. `..          `.  `..    
`. `..      `..        `..   `..       `..   `..   
`..  `..    `..        `..      `..   `...... `..  
`..    `..    `..     `.. `..    `.. `..       `.. 
`..      `..    `....       `.. ..  `..         `..

'''

import os
import sys
import requests
import argparse
import logging
from logging import config



class Exploit(object):
    """docstring for Exploit"""
    def __init__(self, arg):
        super(Exploit, self).__init__()
        self.arg = arg

    def token(self):
        a = api.API(**self.args)
        return a.call('token').json()


class CLI(object):
    """docstring for CLI."""
    def __init__(self):

        self.logging()
        self.main()

    def banner(self):
        print __doc__


    def logging(self):

        ERROR_FORMAT = "%(levelname)s at %(asctime)s in %(funcName)s in %(filename) at line %(lineno)d: %(message)s"
        DEBUG_FORMAT = "[%(asctime)s]: %(message)s"
        INFO_FORMAT = "%(message)s"

        LOG_CONFIG = {
            'version':1,
            'formatters':{
                'error':{
                    'format':ERROR_FORMAT,
                    'datefmt': '%Y-%m-%d %H:%M:%S'
                },
                'debug':{
                    'format':DEBUG_FORMAT,
                    'datefmt': '%Y-%m-%d %H:%M:%S'
                },
                'info':{
                    'format':INFO_FORMAT,
                    'datefmt': '%Y-%m-%d %H:%M:%S'
                    }
            },
            'handlers':{
                'console':{
                    'class':'logging.StreamHandler',
                    'formatter':'info',
                    'level':logging.INFO
                },
                # 'file':{
                #     'class':'logging.FileHandler',
                #     'filename':'.log',
                #     'formatter':'debug',
                #     'level':logging.INFO
                # }
            },
            'root':{
                # 'handlers':['console','file'],
                'handlers':['console'],
                'level':'INFO'
            }
        }

        logging.config.dictConfig(LOG_CONFIG)


    def main(self):

        # Set formatter setting s to remove spaces
        os.environ['COLUMNS'] = "120"
        formatter = lambda prog: argparse.HelpFormatter(prog,max_help_position=52)
        parser = argparse.ArgumentParser(formatter_class=formatter)

        # Set args with Default values.
        parser.add_argument("-m","--msisdn",action="store",dest="msisdn",help="Target Phone Number.")

        parser.add_argument("--api",nargs='*',dest="api",default=['token','getBalance'],help="Set API Resource.")

        # parser.add_argument("-l","--log",action="store",dest="log",help="Logging to file")

        args = parser.parse_args()

        # Recognize args
        if len(sys.argv) == 1:
            self.banner()
            parser.parse_args(['--help'])

        # Call Exploit
        if args.msisdn:
            e = Exploit(args = args)
            e.results()


if __name__ == "__main__":
    CLI()
