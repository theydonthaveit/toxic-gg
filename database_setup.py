import sys
import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from passlib.hash import pbkdf2_sha512

Base = declarative_base()

class BaseMixin(object):

    @declared_attr
    def id(self):

        return Column(Integer, primary_key=True, unique=True)

    @declared_attr
    def created_at(self):

        return Column(DateTime, default=datetime.datetime.utcnow)

    @declared_attr
    def updated_at(self):

        return Column(DateTime, default=datetime.datetime.utcnow)


class UserAccount(Base, BaseMixin):
    __tablename__ = 'user_account'

    name = Column(String(80), nullable=False)
    password = Column(String(1000), nullable=False)

    def decode_password(self, password):
        return pbkdf2_sha512.verify(password, self.password)



Engine = create_engine('postgresql://kwvotvwirlkwnf:ccc0bd82f23e9d025643416a83dae940ee07aaa5fbd5502fea7710941f5d3b50@ec2-54-75-244-248.eu-west-1.compute.amazonaws.com:5432/d6uacc3a5618st')
Base.metadata.create_all(Engine)