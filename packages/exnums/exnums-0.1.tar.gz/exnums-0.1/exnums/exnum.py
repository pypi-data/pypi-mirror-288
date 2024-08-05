# KiryxaTech (c) 2024

import math
import struct
from typing import Union

class ExNumber(float):
    def __new__(cls, value: Union[int, float]):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{type(value)} is not an int or float")
        instance = super().__new__(cls, value)
        return instance

    def __str__(self) -> str:
        return str(self.__value)
    
    def __int__(self) -> int:
        return int(self.__value)
    
    def __float__(self) -> float:
        return float(self.__value)
    
    def __bool__(self) -> bool:
        return bool(self.__value)
    
    def __bytes__(self) -> bytes:
        return bytes(str(self.__value), 'utf-8')

    def __gt__(self, other: 'ExNumber') -> bool:
        return self.__value > other.__value
    
    def __ge__(self, other: 'ExNumber') -> bool:
        return self.__value >= other.__value
        
    def __lt__(self, other: 'ExNumber') -> bool:
        return self.__value < other.__value
    
    def __le__(self, other: 'ExNumber') -> bool:
        return self.__value <= other.__value
    
    def __eq__(self, other: 'ExNumber') -> bool:
        return self.__value == other.__value
    
    def __ne__(self, other: 'ExNumber') -> bool:
        return self.__value != other.__value

    def __init__(self, value: Union[int, float]):
        self.__value = value

    def is_even(self) -> bool:
        return self.__value % 2 == 0
    
    def is_odd(self) -> bool:
        return self.__value % 2 == 1
    
    def round(self, ndigits: int) -> float:
        return round(self.__value, ndigits)

    def floor(self, ndigits: int = 0) -> float:
        factor = 10 ** ndigits
        return math.floor(self.__value * factor) / factor

    def ceil(self, ndigits: int = 0) -> float:
        factor = 10 ** ndigits
        return math.ceil(self.__value * factor) / factor
    
    def is_prime(self) -> bool:
        if isinstance(self.__value, float) or self.__value < 2:
            return False
        
        n = int(self.__value)
        if n <= 1:
            return False
        elif n <= 3:
            return True
        elif n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True
    
    def is_composite(self) -> bool:
        return not self.is_prime() and self.__value > 1
    
    @classmethod
    def to_bytes(cls, num: Union[int, float, 'ExNumber']) -> bytes:
        num = num if type(num) in (int, float) else float(num)
        return struct.pack('!f', num)
    
    @classmethod
    def from_bytes(cls, byte_data: bytes) -> 'ExNumber':
        value = struct.unpack('!f', byte_data)[0]
        return cls(value)
    
    @classmethod
    def to_hex(cls, num: Union[int, float, 'ExNumber']) -> str:
        byte_data = cls.to_bytes(num)
        return byte_data.hex()
    
    @classmethod
    def from_hex(cls, hex_str: str) -> 'ExNumber':
        byte_data = bytes.fromhex(hex_str)
        return cls.from_bytes(byte_data)