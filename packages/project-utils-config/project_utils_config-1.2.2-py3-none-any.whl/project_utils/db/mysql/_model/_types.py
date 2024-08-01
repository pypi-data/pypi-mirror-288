import enum

from typing import Union
from decimal import Decimal
from datetime import time, date, datetime
from sqlalchemy import (
    Column,
    SmallInteger,
    Integer,
    BigInteger,
    Float,
    Double,
    DECIMAL,
    Time,
    Date,
    DateTime,
    TIMESTAMP,
    CHAR,
    VARCHAR,
    Enum,
    Text,
    JSON
)

smallint = Union[Column, SmallInteger, int]
integer = Union[Column, Integer, int]
bigint = Union[Column, BigInteger, int]
float = Union[Column, Float, float]
double = Union[Column, Double, float]
decimal = Union[Column, DECIMAL, Decimal]
time = Union[Column, Time, time]
date = Union[Column, Date, date]
datetime = Union[Column, DateTime, datetime]
timestamp = Union[Column, TIMESTAMP, int]
char = Union[Column, CHAR, str]
varchar = Union[Column, VARCHAR, str]
enum = Union[Column, Enum, enum.Enum]
text = Union[Column, Text, str]
json = Union[Column, JSON, str]
