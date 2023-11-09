"""Сборник базовых классов и значений для домена."""
import datetime
from abc import ABC
from dataclasses import dataclass

from domain.shared.values import PrimaryKey, ToBeGenerated

modelclass = dataclass(eq=False, kw_only=True)


@modelclass
class Entity(ABC):
    """Сущность."""

    id: PrimaryKey | ToBeGenerated = ToBeGenerated
    created_at: datetime.datetime | ToBeGenerated = ToBeGenerated
