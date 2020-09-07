# -*- coding: utf-8 -*-

import configparser


class ConfigSetting:
    def __init__(self, path):
        self.config_path = path
        self.config_info = {}
        
    def read_config(self):
        '''설정 파일 읽는 함수
        Args:
            config_path (str) 설정 파일 주소
        Return:
            설정 파일 읽어서 딕셔너리로 반환
        '''
        cfg = configparser.ConfigParser()
        cfg.read(self.config_path)

        # Config 가져오기
        self.config_info['health_cycle'] = cfg.getint('SYSTEM', 'HEALTH_CYCLE')
        self.config_info['data_cycle'] = cfg.getint('SYSTEM', 'DATA_CYCLE')
        self.config_info['log_level'] = cfg.get('SYSTEM', 'LOG_LEVEL')
        self.config_info['db_string'] = cfg.get('DB', 'DB_STRING')