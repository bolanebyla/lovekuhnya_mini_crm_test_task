from enum import StrEnum


class DealStatuses(StrEnum):
    """Статусы сделок"""

    NEW = "new"
    IN_PROGRESS = "in_progress"
    WON = "won"
    LOST = "lost"


class DealStages(StrEnum):
    """Этапы воронки сделок"""

    QUALIFICATION = "qualification"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED = "closed"
