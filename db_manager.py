# -*- coding: utf-8 -*-

import uuid
import json
import logging
from logging import handlers
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from database.health_schema import HealthSchema
from database.data_schema import DataSchema, PortSchema


class DbManager:

    def __init__(self, string=None, model=None):
        self.engine = None
        self.db_session = None
        self.string = string
        self.model = model

    def db_connect(self):
        try:
            self.engine = create_engine(self.string, convert_unicode=False,
                                        pool_size=1, pool_recycle=500, max_overflow=5, echo=True)
            # DB 세션 생셩
            self.db_session = scoped_session(sessionmaker(
                autocommit=False, autoflush=False, bind=self.engine))
            # 데이터베이스 테이블 생셩
            self.model.metadata.create_all(self.engine)
            logging.info("Database Connection Success: table={val}".format(
                val=self.model.__tablename__))
            return True
        except Exception as e:
            logging.error("Database Connection Fail: Table={tb}, Error={err}".format(
                tb=self.model.__tablename__, err=e))
            return False

    def db_close(self):
        try:
            self.db_session.close()
            logging.info("Database Connection Close Success: table={val}".format(
                val=self.model.__tablename__))
        except Exception as e:
            logging.error("Database Connection Close Fail: Table={tb}, Error={err}".format(
                tb=self.model.__tablename__, err=e))

    def table_create(self):
        self.model.metadata.create_all(self.engine)

    def db_status(self):
        try:
            table_list = inspect(self.engine).get_table_names()
            if self.model.__tablename__.lower() in table_list:
                # 테이블 존재함 True Return
                logging.info("Table Found: {val}".format(
                    val=self.model.__tablename__))
                return True
            else:
                # 테이블 존재하지 않음 None Return
                logging.error("Table Not Found: {val}".format(
                    val=self.model.__tablename__))
                return None
        except Exception as e:
                # 테이블 체크 에러 False Return
                logging.error("Status Check Error: {err}".format(err=e))
                return False

    def health_insert(self, data):
        try:
            logging.info("Database Insert Start: table={val}".format(
                val=self.model.__tablename__))

            # Ping Table Server 1개 입력
            for row in data:
                query = HealthSchema(
                    IP=row['ip'], MAC=row['mac'], HOSTNAME=row['hostname'], STATUS=row['status'], CHECK_TIME=row['time'])
                self.db_session.add(query)
                self.db_session.flush()
            # Data Commit  
            self.db_session.commit()
            logging.info("Database Insert Success: table={val}".format(
                val=self.model.__tablename__))

        except Exception as e:
            self.db_session.rollback()
            logging.error("Database Insert Fail: table={val}, Error={err}".format(
                val=self.model.__tablename__, err=e))

    def port_insert(self, data):
        try:
            logging.info("Database Insert Start: table={val}".format(
                val=self.model.__tablename__))

            # DATA Table Server 1개 입력
            for row in data:
                matching_key = self._generate_uuid()
                query = DataSchema(KEY=matching_key, IP=row['ip'], MAC=row['mac'], HOSTNAME=row['hostname'], OS=row['os'],
                                    MODEL=row['model'], STATUS=row['status'], CHECK_TIME=row['time'])
                self.db_session.add(query)
                self.db_session.flush()
                data = json.loads(row['port_data'])
                # PORT Table Server당 포트 입력
                for row2 in data['protocol'][0]['tcp']:
                    query2 = PortSchema(KEY=matching_key, PORT=row2['port'], STATUS=row2['status'],
                                        NAME=row2['name'], PRODUCT=row2['product'], VERSION=row2['version'])
                    self.db_session.add(query2)
                    self.db_session.flush()
            # Data Commit
            self.db_session.commit()
            logging.info("Database Insert Success: table={val}".format(
                val=self.model.__tablename__))

        except Exception as e:
            self.db_session.rollback()
            logging.error("Database Insert Fail: table={val}, Error={err}".format(
                val=self.model.__tablename__, err=e))

    def _generate_uuid(self):
        return str(uuid.uuid4())
