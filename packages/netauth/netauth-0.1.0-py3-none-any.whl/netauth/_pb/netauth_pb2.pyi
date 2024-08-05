from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Capability(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GLOBAL_ROOT: _ClassVar[Capability]
    CREATE_ENTITY: _ClassVar[Capability]
    DESTROY_ENTITY: _ClassVar[Capability]
    MODIFY_ENTITY_META: _ClassVar[Capability]
    MODIFY_ENTITY_KEYS: _ClassVar[Capability]
    CHANGE_ENTITY_SECRET: _ClassVar[Capability]
    LOCK_ENTITY: _ClassVar[Capability]
    UNLOCK_ENTITY: _ClassVar[Capability]
    CREATE_GROUP: _ClassVar[Capability]
    DESTROY_GROUP: _ClassVar[Capability]
    MODIFY_GROUP_META: _ClassVar[Capability]
    MODIFY_GROUP_MEMBERS: _ClassVar[Capability]

class ExpansionMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INCLUDE: _ClassVar[ExpansionMode]
    EXCLUDE: _ClassVar[ExpansionMode]
    DROP: _ClassVar[ExpansionMode]
GLOBAL_ROOT: Capability
CREATE_ENTITY: Capability
DESTROY_ENTITY: Capability
MODIFY_ENTITY_META: Capability
MODIFY_ENTITY_KEYS: Capability
CHANGE_ENTITY_SECRET: Capability
LOCK_ENTITY: Capability
UNLOCK_ENTITY: Capability
CREATE_GROUP: Capability
DESTROY_GROUP: Capability
MODIFY_GROUP_META: Capability
MODIFY_GROUP_MEMBERS: Capability
INCLUDE: ExpansionMode
EXCLUDE: ExpansionMode
DROP: ExpansionMode

class KVData(_message.Message):
    __slots__ = ("Key", "Values")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    Key: str
    Values: _containers.RepeatedCompositeFieldContainer[KVValue]
    def __init__(self, Key: _Optional[str] = ..., Values: _Optional[_Iterable[_Union[KVValue, _Mapping]]] = ...) -> None: ...

class KVValue(_message.Message):
    __slots__ = ("Value", "Index")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    Value: str
    Index: int
    def __init__(self, Value: _Optional[str] = ..., Index: _Optional[int] = ...) -> None: ...

class Entity(_message.Message):
    __slots__ = ("ID", "Number", "secret", "meta")
    ID_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    ID: str
    Number: int
    secret: str
    meta: EntityMeta
    def __init__(self, ID: _Optional[str] = ..., Number: _Optional[int] = ..., secret: _Optional[str] = ..., meta: _Optional[_Union[EntityMeta, _Mapping]] = ...) -> None: ...

class EntityMeta(_message.Message):
    __slots__ = ("PrimaryGroup", "GECOS", "LegalName", "DisplayName", "Home", "Shell", "GraphicalShell", "BadgeNumber", "Locked", "Groups", "Capabilities", "Keys", "UntypedMeta", "KV")
    PRIMARYGROUP_FIELD_NUMBER: _ClassVar[int]
    GECOS_FIELD_NUMBER: _ClassVar[int]
    LEGALNAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAYNAME_FIELD_NUMBER: _ClassVar[int]
    HOME_FIELD_NUMBER: _ClassVar[int]
    SHELL_FIELD_NUMBER: _ClassVar[int]
    GRAPHICALSHELL_FIELD_NUMBER: _ClassVar[int]
    BADGENUMBER_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    UNTYPEDMETA_FIELD_NUMBER: _ClassVar[int]
    KV_FIELD_NUMBER: _ClassVar[int]
    PrimaryGroup: str
    GECOS: str
    LegalName: str
    DisplayName: str
    Home: str
    Shell: str
    GraphicalShell: str
    BadgeNumber: str
    Locked: bool
    Groups: _containers.RepeatedScalarFieldContainer[str]
    Capabilities: _containers.RepeatedScalarFieldContainer[Capability]
    Keys: _containers.RepeatedScalarFieldContainer[str]
    UntypedMeta: _containers.RepeatedScalarFieldContainer[str]
    KV: _containers.RepeatedCompositeFieldContainer[KVData]
    def __init__(self, PrimaryGroup: _Optional[str] = ..., GECOS: _Optional[str] = ..., LegalName: _Optional[str] = ..., DisplayName: _Optional[str] = ..., Home: _Optional[str] = ..., Shell: _Optional[str] = ..., GraphicalShell: _Optional[str] = ..., BadgeNumber: _Optional[str] = ..., Locked: bool = ..., Groups: _Optional[_Iterable[str]] = ..., Capabilities: _Optional[_Iterable[_Union[Capability, str]]] = ..., Keys: _Optional[_Iterable[str]] = ..., UntypedMeta: _Optional[_Iterable[str]] = ..., KV: _Optional[_Iterable[_Union[KVData, _Mapping]]] = ...) -> None: ...

class Group(_message.Message):
    __slots__ = ("Name", "DisplayName", "Number", "ManagedBy", "Capabilities", "Expansions", "UntypedMeta", "KV")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAYNAME_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    MANAGEDBY_FIELD_NUMBER: _ClassVar[int]
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    EXPANSIONS_FIELD_NUMBER: _ClassVar[int]
    UNTYPEDMETA_FIELD_NUMBER: _ClassVar[int]
    KV_FIELD_NUMBER: _ClassVar[int]
    Name: str
    DisplayName: str
    Number: int
    ManagedBy: str
    Capabilities: _containers.RepeatedScalarFieldContainer[Capability]
    Expansions: _containers.RepeatedScalarFieldContainer[str]
    UntypedMeta: _containers.RepeatedScalarFieldContainer[str]
    KV: _containers.RepeatedCompositeFieldContainer[KVData]
    def __init__(self, Name: _Optional[str] = ..., DisplayName: _Optional[str] = ..., Number: _Optional[int] = ..., ManagedBy: _Optional[str] = ..., Capabilities: _Optional[_Iterable[_Union[Capability, str]]] = ..., Expansions: _Optional[_Iterable[str]] = ..., UntypedMeta: _Optional[_Iterable[str]] = ..., KV: _Optional[_Iterable[_Union[KVData, _Mapping]]] = ...) -> None: ...
