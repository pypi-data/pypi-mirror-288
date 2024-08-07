from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Inbound(_message.Message):
    __slots__ = ("metadata", "cmd", "payload")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CMD_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    metadata: _containers.ScalarMap[str, str]
    cmd: str
    payload: bytes
    def __init__(self, metadata: _Optional[_Mapping[str, str]] = ..., cmd: _Optional[str] = ..., payload: _Optional[bytes] = ...) -> None: ...

class Outbound(_message.Message):
    __slots__ = ("metadata", "payload", "code", "message")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    METADATA_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    metadata: _containers.ScalarMap[str, str]
    payload: bytes
    code: str
    message: str
    def __init__(self, metadata: _Optional[_Mapping[str, str]] = ..., payload: _Optional[bytes] = ..., code: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...
