from dataclasses import dataclass, field
from enum import Enum

from . import _pb
from ._kv import (
    KVDict,
    from_KVData,
    to_KVData,
)


class Capability(Enum):
    """System capabilities"""

    GlobalRoot = 0
    CreateEntity = 10
    DestroyEntity = 11
    ModifyEntityMeta = 12
    ModifyEntityKeys = 13
    ChangeEntitySecret = 14
    LockEntity = 15
    UnlockEntity = 16
    CreateGroup = 20
    DestroyGroup = 21
    ModifyGroupMeta = 22
    ModifyGroupMembers = 23

    def _into(self) -> _pb.Capability:
        """Convert the object into its RPC counterpart"""
        return _pb.Capability(self.value)


class ExpansionMode(Enum):
    """Group expansion modes"""

    Include = 1
    Exclude = 2
    Drop = 99

    def _into(self) -> _pb.ExpansionMode:
        """Convert the object into its RPC counterpart"""
        return _pb.ExpansionMode(self.value)


@dataclass
class EntityMeta:
    """Entity metadata"""

    primary_group: str | None = None
    gecos: str | None = None
    legal_name: str | None = None
    display_name: str | None = None
    home: str | None = None
    shell: str | None = None
    graphical_shell: str | None = None
    badge_number: str | None = None
    locked: bool = False
    groups: list[str] = field(default_factory=list)
    capabilities: list[Capability] = field(default_factory=list)
    keys: list[str] = field(default_factory=list)
    untyped_meta: list[str] = field(default_factory=list)
    kv: KVDict = field(default_factory=dict)

    @classmethod
    def _from(cls, inner: _pb.EntityMeta):
        """Convert the object from its RPC counterpart"""
        return cls(
            primary_group=inner.PrimaryGroup,
            gecos=inner.GECOS,
            legal_name=inner.LegalName,
            display_name=inner.DisplayName,
            home=inner.Home,
            shell=inner.Shell,
            graphical_shell=inner.GraphicalShell,
            badge_number=inner.BadgeNumber,
            locked=inner.Locked,
            groups=list(inner.Groups),
            capabilities=[Capability(c) for c in inner.Capabilities],
            keys=list(inner.Keys),
            untyped_meta=list(inner.UntypedMeta),
            kv=from_KVData(list(inner.KV)),
        )

    def _into(self) -> _pb.EntityMeta:
        """Convert the object into its RPC counterpart"""
        return _pb.EntityMeta(
            PrimaryGroup=self.primary_group,
            GECOS=self.gecos,
            LegalName=self.legal_name,
            DisplayName=self.display_name,
            Home=self.home,
            Shell=self.shell,
            GraphicalShell=self.graphical_shell,
            BadgeNumber=self.badge_number,
            Locked=self.locked,
            Groups=self.groups,
            Capabilities=[c._into() for c in self.capabilities],
            Keys=self.keys,
            UntypedMeta=self.untyped_meta,
            KV=to_KVData(self.kv),
        )


@dataclass
class Entity:
    """Entity information"""

    id: str | None = None
    number: int | None = None
    secret: str | None = None
    meta: EntityMeta | None = None

    @classmethod
    def _from(cls, inner: _pb.Entity):
        """Convert the object from its RPC counterpart"""
        return cls(
            id=inner.ID,
            number=inner.Number,
            secret=inner.secret,
            meta=EntityMeta._from(inner.meta),
        )

    def _into(self) -> _pb.Entity:
        """Convert the object into its RPC counterpart"""
        return _pb.Entity(
            ID=self.id,
            Number=self.number,
            secret=self.secret,
            meta=self.meta._into() if self.meta is not None else None,
        )


@dataclass
class Group:
    """Group information"""

    name: str | None = None
    display_name: str | None = None
    number: int | None = None
    managed_by: str | None = None
    capabilities: list[Capability] = field(default_factory=list)
    expansions: list[str] = field(default_factory=list)
    untyped_meta: list[str] = field(default_factory=list)
    kv: KVDict = field(default_factory=dict)

    @classmethod
    def _from(cls, inner: _pb.Group):
        """Convert the object from its RPC counterpart"""
        return cls(
            name=inner.Name,
            display_name=inner.DisplayName,
            number=inner.Number,
            managed_by=inner.ManagedBy,
            capabilities=[Capability(c) for c in inner.Capabilities],
            expansions=list(inner.Expansions),
            untyped_meta=list(inner.UntypedMeta),
            kv=from_KVData(list(inner.KV)),
        )

    def _into(self) -> _pb.Group:
        """Convert the object into its RPC counterpart"""
        return _pb.Group(
            Name=self.name,
            DisplayName=self.display_name,
            Number=self.number,
            ManagedBy=self.managed_by,
            Capabilities=[c._into() for c in self.capabilities],
            Expansions=self.expansions,
            UntypedMeta=self.untyped_meta,
            KV=to_KVData(self.kv),
        )
