# -*- coding: utf-8 -*-

import uuid
import logging
from logging import handlers
from sqlalchemy import String, Index, Column  # Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class HealthSchema(Base):
    __tablename__ = 'ASSETS_HEALTH'

    UID = Column(String(50), primary_key=True)
    IP = Column(String(15), nullable=False)
    MAC = Column(String(17), nullable=True)
    HOSTNAME = Column(String(50), nullable=True)
    STATUS = Column(String(10), nullable=False)
    CHECK_TIME = Column(String(14), nullable=False)

    # Index Setting
    __table_args__ = (Index(__tablename__ + '_IDX01', 'CHECK_TIME'),)

    def __init__(self, IP=None, MAC=None, HOSTNAME=None, STATUS=None, CHECK_TIME=None):
        self.IP = IP
        self.MAC = MAC
        self.HOSTNAME = HOSTNAME
        self.STATUS = STATUS
        self.CHECK_TIME = CHECK_TIME
        self.UID = self._generate_uuid()

    def _generate_uuid(self):
        return str(uuid.uuid4())
