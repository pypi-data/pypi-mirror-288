"""AbstractDescriptor provides common boilerplate for descriptor classes. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.meta import BaseMetaclass
from worktoy.parse import maybe
from worktoy.text import monoSpace, typeMsg


class AbstractDescriptor(metaclass=BaseMetaclass):
  """AbstractDescriptor provides common boilerplate for descriptor
  classes. """

  __field_owner__ = None
  __field_name__ = None
  __get_subscribers__ = None
  __set_subscribers__ = None
  __del_subscribers__ = None

  def __set_name__(self, owner: type, name: str) -> None:
    """Set the name of the field and the owner of the field."""
    self.__field_owner__ = owner
    self.__field_name__ = name

  def getFieldName(self) -> str:
    """Getter-function for the field name."""
    if self.__field_name__ is None:
      e = """Instance of 'AttriBox' does not belong to class. This 
      typically indicates that the owning class is still being created."""
      raise RuntimeError(monoSpace(e))
    if isinstance(self.__field_name__, str):
      return self.__field_name__
    e = typeMsg('__field_name__', self.__field_name__, str)
    raise TypeError(monoSpace(e))

  def getFieldOwner(self) -> type:
    """Getter-function for the field owner."""
    if self.__field_owner__ is None:
      e = """Instance of 'AttriBox' does not belong to class. This 
      typically indicates that the owning class is still being created."""
      raise RuntimeError(monoSpace(e))
    if isinstance(self.__field_owner__, type):
      return self.__field_owner__
    e = typeMsg('__field_owner__', self.__field_owner__, type)
    raise TypeError(monoSpace(e))

  def notifyGet(self, instance: object, value: object) -> None:
    for callMeMaybe in self._getGetSubscribers():
      callMeMaybe(instance, value)

  def notifySet(self,
                instance: object,
                oldValue: object,
                newValue: object) -> None:
    for callMeMaybe in self._getSetSubscribers():
      callMeMaybe(instance, oldValue, newValue)

  def notifyDel(self, instance: object, value: object) -> None:
    for callMeMaybe in self._getDelSubscribers():
      callMeMaybe(instance, value)

  def _getGetSubscribers(self) -> list[callable]:
    return maybe(self.__get_subscribers__, [])

  def _getSetSubscribers(self) -> list[callable]:
    return maybe(self.__set_subscribers__, [])

  def _getDelSubscribers(self) -> list[callable]:
    return maybe(self.__del_subscribers__, [])

  def _addGetSubscriber(self, callMeMaybe: callable) -> None:
    """Subscribes the callable received to be notified when the field
    getter is called. The instance and the value are passed as arguments.
    If instance is None, the AttriBox is accessed through the owning class,
    which does not result in a notification.

    Similar to this method, the _addSetSubscriber and _addDelSubscriber
    methods are used to subscribe callables to be notified when the field
    is accessed. """
    getSubscribers = self._getGetSubscribers()
    self.__get_subscribers__ = [*getSubscribers, callMeMaybe]

  def _addSetSubscriber(self, callMeMaybe: callable) -> None:
    """Registers the callable for notification when field setter is
    called."""
    setSubscribers = self._getSetSubscribers()
    self.__set_subscribers__ = [*setSubscribers, callMeMaybe]

  def _addDelSubscriber(self, callMeMaybe: callable) -> None:
    """Registers the callable for notification when field deleter is
    called."""
    delSubscribers = self._getDelSubscribers()
    self.__del_subscribers__ = [*delSubscribers, callMeMaybe]

  def ONGET(self, callMeMaybe: callable) -> callable:
    """Decorator for subscribing to the getter."""
    self._addGetSubscriber(callMeMaybe)
    return callMeMaybe

  def ONSET(self, callMeMaybe: callable) -> callable:
    """Decorator for subscribing to the setter."""
    self._addSetSubscriber(callMeMaybe)
    return callMeMaybe

  def ONDEL(self, callMeMaybe: callable) -> callable:
    """Decorator for subscribing to the deleter."""
    self._addDelSubscriber(callMeMaybe)
    return callMeMaybe
