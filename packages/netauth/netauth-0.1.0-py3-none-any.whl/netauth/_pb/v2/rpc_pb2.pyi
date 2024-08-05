import netauth_pb2 as _netauth_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Action(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ADD: _ClassVar[Action]
    DROP: _ClassVar[Action]
    UPSERT: _ClassVar[Action]
    CLEAREXACT: _ClassVar[Action]
    CLEARFUZZY: _ClassVar[Action]
    READ: _ClassVar[Action]

class RuleAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INCLUDE: _ClassVar[RuleAction]
    EXCLUDE: _ClassVar[RuleAction]
    REMOVE_RULE: _ClassVar[RuleAction]
ADD: Action
DROP: Action
UPSERT: Action
CLEAREXACT: Action
CLEARFUZZY: Action
READ: Action
INCLUDE: RuleAction
EXCLUDE: RuleAction
REMOVE_RULE: RuleAction

class EntityRequest(_message.Message):
    __slots__ = ("Entity", "Data")
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    Entity: _netauth_pb2.Entity
    Data: _netauth_pb2.Entity
    def __init__(self, Entity: _Optional[_Union[_netauth_pb2.Entity, _Mapping]] = ..., Data: _Optional[_Union[_netauth_pb2.Entity, _Mapping]] = ...) -> None: ...

class GroupRequest(_message.Message):
    __slots__ = ("Group", "Data")
    GROUP_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    Group: _netauth_pb2.Group
    Data: _netauth_pb2.Group
    def __init__(self, Group: _Optional[_Union[_netauth_pb2.Group, _Mapping]] = ..., Data: _Optional[_Union[_netauth_pb2.Group, _Mapping]] = ...) -> None: ...

class KVRequest(_message.Message):
    __slots__ = ("Target", "Action", "Key", "Value")
    TARGET_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    Target: str
    Action: Action
    Key: str
    Value: str
    def __init__(self, Target: _Optional[str] = ..., Action: _Optional[_Union[Action, str]] = ..., Key: _Optional[str] = ..., Value: _Optional[str] = ...) -> None: ...

class KV2Request(_message.Message):
    __slots__ = ("Target", "Data")
    TARGET_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    Target: str
    Data: _netauth_pb2.KVData
    def __init__(self, Target: _Optional[str] = ..., Data: _Optional[_Union[_netauth_pb2.KVData, _Mapping]] = ...) -> None: ...

class ListOfEntities(_message.Message):
    __slots__ = ("Entities",)
    ENTITIES_FIELD_NUMBER: _ClassVar[int]
    Entities: _containers.RepeatedCompositeFieldContainer[_netauth_pb2.Entity]
    def __init__(self, Entities: _Optional[_Iterable[_Union[_netauth_pb2.Entity, _Mapping]]] = ...) -> None: ...

class ListOfGroups(_message.Message):
    __slots__ = ("Groups",)
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    Groups: _containers.RepeatedCompositeFieldContainer[_netauth_pb2.Group]
    def __init__(self, Groups: _Optional[_Iterable[_Union[_netauth_pb2.Group, _Mapping]]] = ...) -> None: ...

class ListOfStrings(_message.Message):
    __slots__ = ("Strings",)
    STRINGS_FIELD_NUMBER: _ClassVar[int]
    Strings: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, Strings: _Optional[_Iterable[str]] = ...) -> None: ...

class ListOfKVData(_message.Message):
    __slots__ = ("KVData",)
    KVDATA_FIELD_NUMBER: _ClassVar[int]
    KVData: _containers.RepeatedCompositeFieldContainer[_netauth_pb2.KVData]
    def __init__(self, KVData: _Optional[_Iterable[_Union[_netauth_pb2.KVData, _Mapping]]] = ...) -> None: ...

class AuthRequest(_message.Message):
    __slots__ = ("Entity", "Secret", "Token")
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    Entity: _netauth_pb2.Entity
    Secret: str
    Token: str
    def __init__(self, Entity: _Optional[_Union[_netauth_pb2.Entity, _Mapping]] = ..., Secret: _Optional[str] = ..., Token: _Optional[str] = ...) -> None: ...

class AuthResult(_message.Message):
    __slots__ = ("Token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    Token: str
    def __init__(self, Token: _Optional[str] = ...) -> None: ...

class SubSystemStatus(_message.Message):
    __slots__ = ("Name", "OK", "FaultMessage")
    NAME_FIELD_NUMBER: _ClassVar[int]
    OK_FIELD_NUMBER: _ClassVar[int]
    FAULTMESSAGE_FIELD_NUMBER: _ClassVar[int]
    Name: str
    OK: bool
    FaultMessage: str
    def __init__(self, Name: _Optional[str] = ..., OK: bool = ..., FaultMessage: _Optional[str] = ...) -> None: ...

class ServerStatus(_message.Message):
    __slots__ = ("SystemOK", "FirstFailure", "SubSystems")
    SYSTEMOK_FIELD_NUMBER: _ClassVar[int]
    FIRSTFAILURE_FIELD_NUMBER: _ClassVar[int]
    SUBSYSTEMS_FIELD_NUMBER: _ClassVar[int]
    SystemOK: bool
    FirstFailure: SubSystemStatus
    SubSystems: _containers.RepeatedCompositeFieldContainer[SubSystemStatus]
    def __init__(self, SystemOK: bool = ..., FirstFailure: _Optional[_Union[SubSystemStatus, _Mapping]] = ..., SubSystems: _Optional[_Iterable[_Union[SubSystemStatus, _Mapping]]] = ...) -> None: ...

class CapabilityRequest(_message.Message):
    __slots__ = ("Capability", "Direct", "Target", "Action")
    CAPABILITY_FIELD_NUMBER: _ClassVar[int]
    DIRECT_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    Capability: _netauth_pb2.Capability
    Direct: bool
    Target: str
    Action: Action
    def __init__(self, Capability: _Optional[_Union[_netauth_pb2.Capability, str]] = ..., Direct: bool = ..., Target: _Optional[str] = ..., Action: _Optional[_Union[Action, str]] = ...) -> None: ...

class GroupRulesRequest(_message.Message):
    __slots__ = ("Group", "Target", "RuleAction")
    GROUP_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    RULEACTION_FIELD_NUMBER: _ClassVar[int]
    Group: _netauth_pb2.Group
    Target: _netauth_pb2.Group
    RuleAction: RuleAction
    def __init__(self, Group: _Optional[_Union[_netauth_pb2.Group, _Mapping]] = ..., Target: _Optional[_Union[_netauth_pb2.Group, _Mapping]] = ..., RuleAction: _Optional[_Union[RuleAction, str]] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SearchRequest(_message.Message):
    __slots__ = ("expression",)
    EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    expression: str
    def __init__(self, expression: _Optional[str] = ...) -> None: ...
