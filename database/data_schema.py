# -*- coding: utf-8 -*-

import uuid
import logging
from logging import handlers
from sqlalchemy import String, Index, Column  # Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DataSchema(Base):
    __tablename__ = 'ASSETS_DATA'

    UID = Column(String(50), primary_key=True)
    IP = Column(String(15), nullable=False)
    MAC = Column(String(17), nullable=True)
    HOSTNAME = Column(String(50), nullable=True)
    OS = Column(String(30), nullable=True)
    MODEL = Column(String(30), nullable=True)
    STATUS = Column(String(10), nullable=False)
    CHECK_TIME = Column(String(14), nullable=False)
    KEY = Column(String(50), nullable=False)

    # Index Setting
    __table_args__ = (Index(__tablename__ + '_IDX01', 'CHECK_TIME'),
                      Index(__tablename__ + '_IDX02', 'KEY'))

    def __init__(self, IP=None, MAC=None, HOSTNAME=None, OS=None, MODEL=None, STATUS=None, CHECK_TIME=None, KEY=None):
        self.UID = self._generate_uuid()
        self.IP = IP
        self.MAC = MAC
        self.HOSTNAME = HOSTNAME
        self.OS = OS
        self.MODEL = MODEL
        self.STATUS = STATUS
        self.CHECK_TIME = CHECK_TIME
        self.KEY = KEY

    def _generate_uuid(self):
        return str(uuid.uuid4())


class PortSchema(Base):
    __tablename__ = 'ASSETS_DATA_PORT'

    UID = Column(String(50), primary_key=True)
    PORT = Column(String(5), nullable=False)
    STATUS = Column(String(30), nullable=True)
    NAME = Column(String(200), nullable=True)
    PRODUCT = Column(String(200), nullable=True)
    VERSION = Column(String(50), nullable=True)
    KEY = Column(String(50), nullable=False)

    # Index Setting
    __table_args__ = (Index(__tablename__ + '_IDX01', 'KEY'),)

    def __init__(self, PORT=None, STATUS=None, NAME=None, PRODUCT=None, VERSION=None, KEY=None):
        self.UID = self._generate_uuid()
        self.PORT = PORT
        self.STATUS = STATUS
        self.NAME = NAME
        self.PRODUCT = PRODUCT
        self.VERSION = VERSION
        self.KEY = KEY

    def _generate_uuid(self):
        return str(uuid.uuid4())
