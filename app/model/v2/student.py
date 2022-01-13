"""
    :copyright: © 2020 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, String

from app.exception.api import BookNotFound


class Student(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    parent = Column(String(30), default="未名")
    phone = Column(String(50))
    address = Column(String(5000))
