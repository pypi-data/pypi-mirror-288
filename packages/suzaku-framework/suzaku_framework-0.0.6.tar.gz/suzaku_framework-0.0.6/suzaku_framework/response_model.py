# -*- encoding: utf-8 -*-

'''
Author     :Phailin
Datetime   :2023-08-01 09:00:00
E-Mail     :phailin791@hotmail.com
'''

from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    total: int = 0  # type: ignore
    page: int = 1  # type: ignore
    page_size: int = 10  # type: ignore
    page_data: List[T] = [] # type: ignore

class RenderBase(BaseModel, Generic[T]):
    code: int = 10200  # first version api code,
    data: T = ""
    message: str = ""

class RenderPage(BaseModel, Generic[T]):
    code: int = 10200  # first version api code,
    data: Page[T] = ""
    message: str = ""