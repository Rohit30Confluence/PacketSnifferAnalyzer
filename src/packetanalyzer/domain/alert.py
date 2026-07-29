"""AlertRule and AlertEvent domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any


class AlertSeverity(Enum):
    """Severity level of an alert."""

    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()


class AlertAction(Enum):
    """Output action for a triggered alert."""

    CONSOLE = auto()
    LOG = auto()
    WEBHOOK = auto()


@dataclass(frozen=True)
class AlertRule:
    """A user-defined alert rule evaluated against live traffic.

    Attributes:
        rule_id: Unique identifier for this rule.
        name: Human-readable name.
        description: What this rule detects.
        condition: The condition type (e.g., 'syn_flood', 'port_scan',
            'high_bandwidth', 'custom_bpf').
        threshold: The numeric threshold that triggers the alert.
        window_seconds: The time window over which the threshold is evaluated.
        severity: The severity level of the alert.
        actions: The set of output actions to take when triggered.
        webhook_url: HTTPS URL for webhook notifications (if WEBHOOK action).
        enabled: Whether this rule is active.
    """

    rule_id: str
    name: str
    description: str
    condition: str
    threshold: float
    window_seconds: int
    severity: AlertSeverity
    actions: frozenset[AlertAction]
    webhook_url: str | None = None
    enabled: bool = True


@dataclass
class AlertEvent:
    """A triggered alert event.

    Attributes:
        event_id: Unique identifier for this event.
        rule: The rule that triggered this alert.
        triggered_at: When the alert was triggered.
        observed_value: The value that exceeded the threshold.
        context: Additional context about the triggering condition.
        acknowledged: Whether the alert has been acknowledged by the user.
    """

    event_id: str
    rule: AlertRule
    triggered_at: datetime
    observed_value: float
    context: dict[str, Any] = field(default_factory=dict)
    acknowledged: bool = False
