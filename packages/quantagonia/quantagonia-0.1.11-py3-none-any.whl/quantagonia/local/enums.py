"""Enums that are only used internally and that are excluded from the pip-installed version."""

from enum import Enum


class HybridSolverConnectionType(Enum):
    CLOUD = 0
    LOCAL = 1
