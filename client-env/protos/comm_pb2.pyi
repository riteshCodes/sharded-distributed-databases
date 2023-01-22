from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Data(_message.Message):
    __slots__ = ["email", "name", "userID"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    email: str
    name: str
    userID: int
    def __init__(self, userID: _Optional[int] = ..., name: _Optional[str] = ..., email: _Optional[str] = ...) -> None: ...

class Dict(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[Data]
    def __init__(self, data: _Optional[_Iterable[_Union[Data, _Mapping]]] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetData(_message.Message):
    __slots__ = ["email", "name"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    email: str
    name: str
    def __init__(self, name: _Optional[str] = ..., email: _Optional[str] = ...) -> None: ...

class GetDictData(_message.Message):
    __slots__ = ["getdata"]
    GETDATA_FIELD_NUMBER: _ClassVar[int]
    getdata: _containers.RepeatedCompositeFieldContainer[GetData]
    def __init__(self, getdata: _Optional[_Iterable[_Union[GetData, _Mapping]]] = ...) -> None: ...

class Key(_message.Message):
    __slots__ = ["key"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: int
    def __init__(self, key: _Optional[int] = ...) -> None: ...

class KeyList(_message.Message):
    __slots__ = ["key_list"]
    KEY_LIST_FIELD_NUMBER: _ClassVar[int]
    key_list: _containers.RepeatedCompositeFieldContainer[Key]
    def __init__(self, key_list: _Optional[_Iterable[_Union[Key, _Mapping]]] = ...) -> None: ...

class MapDefault(_message.Message):
    __slots__ = ["key_value"]
    class KeyValueEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    KEY_VALUE_FIELD_NUMBER: _ClassVar[int]
    key_value: _containers.ScalarMap[str, str]
    def __init__(self, key_value: _Optional[_Mapping[str, str]] = ...) -> None: ...

class MapIntString(_message.Message):
    __slots__ = ["key_value"]
    class KeyValueEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: str
        def __init__(self, key: _Optional[int] = ..., value: _Optional[str] = ...) -> None: ...
    KEY_VALUE_FIELD_NUMBER: _ClassVar[int]
    key_value: _containers.ScalarMap[int, str]
    def __init__(self, key_value: _Optional[_Mapping[int, str]] = ...) -> None: ...

class MapStringInt(_message.Message):
    __slots__ = ["key_value"]
    class KeyValueEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    KEY_VALUE_FIELD_NUMBER: _ClassVar[int]
    key_value: _containers.ScalarMap[str, int]
    def __init__(self, key_value: _Optional[_Mapping[str, int]] = ...) -> None: ...

class Range(_message.Message):
    __slots__ = ["end", "start"]
    END_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    end: int
    start: int
    def __init__(self, start: _Optional[int] = ..., end: _Optional[int] = ...) -> None: ...

class StringMessage(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
