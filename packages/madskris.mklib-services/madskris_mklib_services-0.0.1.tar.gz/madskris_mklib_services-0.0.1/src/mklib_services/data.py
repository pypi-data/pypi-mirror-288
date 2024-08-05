from pandas import DataFrame
from typing import TypeVar
from .rows import Materiell

T = TypeVar("T", DataFrame, Materiell)

class DataResult[T]():
    
    def __init__(self, input: T|str) -> None:
        self.input: T|str = input

    @property
    def successful(self) -> bool:
        
        return isinstance(self.input, str) is False

    @property
    def error(self) -> str:
        
        if isinstance(self.input, str):
            return self.input
        
        return ""
    
    @property
    def data(self) -> T:
                
        if isinstance(self.input, str): 
            raise Exception("Tried to read null dataproperty")
        
        return self.input
    
    def __str__(self) -> str:
        
        if isinstance(self.input, str):
            return self.input
        
        return f"Should be successful"
    
    def __repr__(self) -> str:
        if isinstance(self.input, str):
            return self.input
        
        return f"Should be successful"
    