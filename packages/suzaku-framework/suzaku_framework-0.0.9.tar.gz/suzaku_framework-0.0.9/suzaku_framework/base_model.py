# -*- encoding: utf-8 -*-

'''
Author     :Phailin
Datetime   :2023-08-01 09:00:00
E-Mail     :phailin791@hotmail.com
'''

from typing import Optional
from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import (declared_attr, declarative_mixin, Mapped, mapped_column)

from suzaku_framework.database import Base # noqa

@declarative_mixin
class ModelMixin:

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
    __table_args__ = {'mysql_engine': 'InnoDB'}
    __mapper_args__= {'always_refresh': True}

    id: Mapped[int] = mapped_column(primary_key=True, sort_order=-1, comment="id")
    created_by: Mapped[Optional[int]] = mapped_column(comment="创建人")
    created_at: Mapped[Optional[datetime]] = mapped_column(comment="创建时间")
    updated_by: Mapped[Optional[int]] = mapped_column(comment="更新人")
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=datetime.now, comment="更新时间")
    comment: Mapped[Optional[str]] = mapped_column(String(64), comment="备注")
    deleted: Mapped[Optional[bool]] = mapped_column(default=False, comment="逻辑删除:False=>未删除,True=>已删除", doc="逻辑删除")