# -*- coding: utf-8 -*-

import sys
import time
import json
import logging
from logging import handlers
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from nmap_scan import ScanManager
from database.health_schema import HealthSchema
from database.data_schema import DataSchema
from db_manager import DbManager


def health_mod(config, scan_list):
    # DB 연결 시작
    db = DbManager(config['db_string'], HealthSchema())
    # DB 연결 재시도
    if db.db_connect() == False:
        max = 10
        for num in range(max):
            time.sleep(1)
            if db.db_connect() == False:
                logging.error("Database Connection Retry: {cnt}".format(cnt=num+1))
            else:
                break
            # DB 연결 max만큼 시도 후 연결 안 될 시 프로세스 종료
            if max == num + 1:
                logging.error("===========Health Check Proccess Stop===========")
                sys.exit()

    # Scanner 객체 Load
    scan = ScanManager()

    # Ping Check Loop Start
    logging.info("Ping Check Loop Start")
    while True:
        for host in scan_list:
            scan.address = [host]
            data = scan.ping_check()
            if data != False and data:
                # DB Data Insert
                db.health_insert(data)
            else:
                # DB에 넣을 데이터가 없으면 시도 안함
                logging.info("Insert Data Null Not Start")

        # Loop 주기
        logging.info("Health Cycle Sleep: {val}s".format(val=config['health_cycle']))
        time.sleep(config['health_cycle'])

        # Loop 주기 마다 DB 연결 상태 확인
        status = db.db_status()
        if status == None:
            logging.error("Table Create Start")
            db.table_create()
        elif status == False:
            logging.error("Database Connection Refresh")
            db.db_close()
            db.db_connect()



def data_mod(config, scan_list):
    # DB 연결 시작
    db = DbManager(config['db_string'], DataSchema())
    # DB 연결 재시도
    if db.db_connect() == False:
        max = 10
        for num in range(max):
            time.sleep(1)
            if db.db_connect() == False:
                logging.error("Database Connection Retry: {cnt}".format(cnt=num+1))
            else:
                break
            # DB 연결 max만큼 시도 후 연결 안 될 시 프로세스 종료
            if max == num + 1:
                logging.error("===========Port Scan Proccess Stop===========")
                sys.exit()

    # Scanner 객체 Load
    scan = ScanManager()
    # Data Format Load
    scan.json_load()

    # Ping Check Loop Start
    logging.info("Port Scan Loop Start")
    while True:
        for host in scan_list:
            scan.address = [host]
            data = scan.port_scan()
            if data != False and data:
                # DB Data Insert
                db.port_insert(data)
            else:
                # DB에 넣을 데이터가 없으면 시도 안함
                logging.info("Insert Data Null Not Start")

        # Loop 주기
        logging.info("Port Scan Cycle Sleep: {val}s".format(val=config['data_cycle']))
        time.sleep(config['data_cycle'])

        # Loop 주기 마다 DB 연결 상태 확인
        status = db.db_status()
        if status == None:
            logging.error("Table Create Start")
            db.table_create()
        elif status == False:
            logging.error("Database Connection Refresh")
            db.db_close()
            db.db_connect()


