from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

@dataclass
class InvestmentRecord:
    company_name: Optional[str]
    deal_date: Optional[str]
    deal_size: Optional[str]
    deal_type: Optional[str]
    industry: Optional[str]