from dataclasses import dataclass, field
from enum import Enum

from . import _pb

__all__ = [
    "Action",
    "RuleAction",
    "SubSystemStatus",
    "ServerStatus",
]


class Action(Enum):
    """Actions available for various operations"""

    Add = 1
    Drop = 2
    Upsert = 3
    ClearExact = 4
    ClearFuzzy = 5
    Read = 6

    def _into(self) -> _pb.v2.Action:
        """Convert the object into its RPC counterpart"""
        return _pb.v2.Action(self.value)


class RuleAction(Enum):
    """Actions available for group rule operations"""

    Include = 1
    Exclude = 2
    RemoveRule = 99

    def _into(self) -> _pb.v2.RuleAction:
        """Convert the object into its RPC counterpart"""
        return _pb.v2.RuleAction(self.value)


@dataclass
class SubSystemStatus:
    """Subsystem status information"""

    name: str | None = None
    ok: bool = True
    fault_message: str | None = None

    @classmethod
    def _from(cls, inner: _pb.v2.SubSystemStatus):
        """Convert the object from its RPC counterpart"""
        return cls(
            name=inner.Name,
            ok=inner.OK,
            fault_message=inner.FaultMessage,
        )

    def _into(self) -> _pb.v2.SubSystemStatus:
        """Convert the object into its RPC counterpart"""
        return _pb.v2.SubSystemStatus(
            Name=self.name,
            OK=self.ok,
            FaultMessage=self.fault_message,
        )


@dataclass
class ServerStatus:
    """Server status information"""

    system_ok: bool = False
    first_failure: SubSystemStatus | None = None
    subsystems: list[SubSystemStatus] = field(default_factory=list)

    @classmethod
    def _from(cls, inner: _pb.v2.ServerStatus):
        """Convert the object from its RPC counterpart"""
        return cls(
            system_ok=inner.SystemOK,
            first_failure=SubSystemStatus._from(inner.FirstFailure),
            subsystems=[SubSystemStatus._from(s) for s in inner.SubSystems],
        )

    def _into(self) -> _pb.v2.ServerStatus:
        """Convert the object into its RPC counterpart"""
        return _pb.v2.ServerStatus(
            SystemOK=self.system_ok,
            FirstFailure=self.first_failure._into() if self.first_failure is not None else None,
            SubSystems=[s._into() for s in self.subsystems],
        )
