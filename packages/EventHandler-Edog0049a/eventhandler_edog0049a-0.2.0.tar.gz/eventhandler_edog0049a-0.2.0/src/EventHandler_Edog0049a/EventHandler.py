"""
    Event Handler

    .. codeauthor:: Eli Reid <EliR@EliReid.com>
"""
from enum import Enum
from typing import Callable
class EventHandler:
    """
    Event Handler
    """
    def __init__(self) -> None:
        self._events: dict[str, _event] = {}

    def emit(self, sender: any, event: str, obj: object = None, once: bool = False)->None:
        """ EventHandler.emit - Emits event to callback functions

            :param sender: what is responsible for the event
            :type sender: any

            :param event: name of event
            :type event: str

            :param obj: anything to pass to callback
            :type obj: object

            :param once: if it is a one time event
            :type once: bool

            :return: None
            :rtype: None

            :raise: TypeError if event isn't string
            :raise: TypeError if func isn't function pointer
        """
        
        if not isinstance(event, (str, int, Enum)):
            raise TypeError("event should of type str ")
        elif not isinstance(once, bool):
            raise TypeError("Requires callback function pointer ex: myCallback(sender, obj)")
        else:
            self._register(event)
            for func in self._events.get(event).getCallbackFuncs():
                func(sender, obj)
       
  
    def on(self, event: str, func: Callable)->None:
        """ EventHandler.on - sets callback functions to event

            :param event: name of event
            :type event: str

            :param func: pointer to callback function or method
            :type func: types.FunctionType or types.MethodType

            :return: None
            :rtype: None

            :raise: TypeError if event isn't string
            :raise: TypeError if func isn't function pointer
        """
        if not isinstance(event, (str, int, Enum)):
            raise TypeError("event should of type str ")
        elif not isinstance(func, Callable):
            raise TypeError("Requires callback function pointer ex: myCallback(sender, obj)")
        else:
            self._register(event)
            self._events[event].add(func)
       
  
    def removeEvent(self, event: str)->None:
        """ EventHandler.removeEvent - Removes event from system

            :param event: name of event
            :type event: str

            :return: True if event is registered
            :rtypr: bool

            :raise: TypeError if event isn't string
        """

        if self._isRegistered(event):
            del self._events[event]
         
  
    def removeFunc(self, event: str, func: Callable)->None:
        """ EventHandler.removeFunc - Removes callback fucntion from event

            :param event: name of event
            :type event: str

            :param func: pointer to callback function or method
            :type func: types.FunctionType or types.MethodType


            :return: True if event is registered
            :rtype: bool

            :raise: TypeError if event isn't string
            :raise: TypeError if func isn't function pointer
        """
        if not isinstance(event, (str, int, Enum)):
            raise TypeError("event should of type str ")
        elif not isinstance(func, Callable):
            raise TypeError("Requires callback function pointer ex: myCallback(sender, obj)")
        else:
            self._events[event].remove(func)
           
  
    def _isRegistered(self, event: str|int|Enum)->bool:
        """ EventHandler._isRegister - Checks if event exists 

            See if callback function already registered

            :param event: name of event
            :type event: str

            :return: True if event is registered
            :rtypr: bool

            :raise: TypeError if event isn't string
        """
        if not isinstance(event, (str, int, Enum)):
            raise TypeError("event should be of type str")
        else:
            return event in self._events.keys()
        
  
    def _register(self, event: str)->None:
        """ EventHandler._register - Creates new event            

            :param event: name of event
            :type event: str

            :return: None
            :rtypr: None

            :raise: TypeError if event isn't string
        """
        if not self._isRegistered(event):
            self._events[event] = _event()

  
    def getEvents(self)->list:
        """ EventHandler.getEvents -  Gets list of events

            :returns: list of event names
            :rtype: list[str] or list[]
        """
        return list(self._events)

  
    def getCallbackFuncs(self, event: str)->list:
        """ EventHandler.getCallbackFuncs - gets list of callback functions for event
            
            :returns: list of function pointers or empty list
            :rtype: list[types.FunctionType] or list[]

            :raise: TypeError if event isn't string
        """

        if not isinstance(event, (str, int, Enum)):
            raise TypeError("Event should be of type str") 
        else:
            return self._events.get(event).getCallbackFuncs()

class _event():
    """.. class:: _event

        Event object stores callback functions for an event
    """
    def __init__(self):
        #: Setup list for functions
        self._callbacks: list = []

    def add(self, func: Callable)->None:
        """ _event.add - Append function to list of functions for event

            :param func: A callback function pointer
            :type func: types.FunctionType

            :returns: None
            :rtype: None

            :raise: TypeError if func in not function type
        """
        if not isinstance(func, Callable):
            raise TypeError("Requires callback function pointer ex: myCallback(sender, obj)")
       
        if self._callbacks.count(func) == 0:
            self._callbacks.append(func)
            
    def remove(self, func: Callable)->None:
        """ _event.remove - Remove callback function from event

            :param func: A callback function pointer
            :type func: types.FunctionType

            :returns: None
            :rtype: None

            :raise: TypeError if func in not function type
        """

        if not isinstance(func, Callable):
            raise TypeError("Requires callback function pointer ex: myCallback(sender, obj)")
        
        #: Verify list has function before trying to remove function
        if self._callbacks.count(func) > 0:
            self._callbacks.remove(func)

    def getCallbackFuncs(self)->list:
        """ _event.getCallbackFuncs - get list of callback functions

            :returns: list of function pointers or empty list
            :rtype: list[types.FunctionType] or list[]
        """
        return list(self._callbacks)
