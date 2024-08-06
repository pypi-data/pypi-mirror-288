
from typing import Any, Callable
# from evdschat.common.chatters import Retriever
from dataclasses import dataclass 

@dataclass 
class Retriever:
    ...
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass
    
    
    
def chat(prompt: str, getter: Callable = Retriever(), debug=False):
    """

    :param prompt: str
    :return: Result Instance < .data : DF  . metadata : DF  to_excel : Callable >
    """
    getter.debug = debug
    return getter(prompt)

def coming_soon():
    """evdschat"""
    print('evdschat is coming_soon' )