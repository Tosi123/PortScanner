# -*- coding: utf-8 -*-

import logging
from logging import handlers
from multiprocessing import Process

import process_mod
from read_config import ConfigSetting
from config import scan_area

if __name__ == '__main__':
    # Config 읽기
    config = ConfigSetting('./config/server.cfg')
    config.read_config()

    # log settings
    log_formatter = logging.Formatter(
        '%(asctime)s\t%(levelname)s\t%(filename)s:%(lineno)s\t%(message)s')

    # handler settings
    log_handler = handlers.TimedRotatingFileHandler(filename='./log/scanning.log', when='midnight', interval=1,
                                                    encoding='utf-8')
    log_handler.setFormatter(log_formatter)
    log_handler.suffix = "%Y%m%d"

    # logger set
    logger = logging.getLogger()

    # Log Level 지정
    if config.config_info['log_level'].lower() == 'debug':
        logger.setLevel(logging.DEBUG)
    elif config.config_info['log_level'].lower() == 'info':
        logger.setLevel(logging.INFO)
    elif config.config_info['log_level'].lower() == 'warning':
        logger.setLevel(logging.warning)
    elif config.config_info['log_level'].lower() == 'error':
        logger.setLevel(logging.ERROR)
    else:
        logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)

    logging.info("===========Health Check Proccess Start===========")
    health_process = Process(target=process_mod.health_mod, args=(
        config.config_info, scan_area.SCAN_LIST))
    health_process.start()

    logging.info("===========Data Scan Proccess Start===========")
    data_process = Process(target=process_mod.data_mod, args=(
        config.config_info, scan_area.SCAN_LIST))
    data_process.start()
