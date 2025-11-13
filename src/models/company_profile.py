from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class CompanyProfile:
    url: str
    id: Optional[str]
    company_name: Optional[str]
    company_socials: List[Dict[str, str]] = field(default_factory=list)
    year_founded: Optional[int] = None
    status: Optional[str] = None
    employees: Optional[int] = None
    latest_deal_type: Optional[str] = None
    financing_rounds: Optional[int] = None
    investments: Optional[int] = None
    description: Optional[str] = None
    contact_information: List[Dict[str, str]] = field(default_factory=list)
    patents: Optional[Any] = None
    competitors: List[Dict[str, Any]] = field(default_factory=list)
    research_analysis: Optional[Any] = None
    patent_activity: Optional[Any] = None
    all_investments: List[Dict[str, Any]] = field(default_factory=list)
    faq: List[Dict[str, Any]] = field(default_factory=list)
    investors: List[str] = field(default_factory=list)

    @classmethod
    def from_parsed_parts(
        cls,
        *,
        basics: Dict[str, Any],
        investments_summary: Dict[str, Any],
        competitors: List[Dict[str, Any]],
        all_investments: List[Dict[str, Any]],
        faq: List[Dict[str, Any]],
        investors: List[str],
    ) -> "CompanyProfile":
        return cls(
            url=basics.get("url"),
            id=basics.get("id"),
            company_name=basics.get("company_name"),
            company_socials=basics.get("company_socials", []),
            year_founded=basics.get("year_founded"),
            status=basics.get("status"),
            employees=basics.get("employees"),
            latest_deal_type=investments_summary.get("latest_deal_type")
            or basics.get("latest_deal_type"),
            financing_rounds=investments_summary.get("financing_rounds")
            or basics.get("financing_rounds"),
            investments=investments_summary.get("investments")
            or basics.get("investments"),
            description=basics.get("description"),
            contact_information=basics.get("contact_information", []),
            patents=basics.get("patents"),
            competitors=competitors or [],
            research_analysis=basics.get("research_analysis"),
            patent_activity=basics.get("patent_activity"),
            all_investments=all_investments or [],
            faq=faq or [],
            investors=investors or [],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "id": self.id,
            "company_name": self.company_name,
            "company_socials": self.company_socials,
            "year_founded": self.year_founded,
            "status": self.status,
            "employees": self.employees,
            "latest_deal_type": self.latest_deal_type,
            "financing_rounds": self.financing_rounds,
            "investments": self.investments,
            "description": self.description,
            "contact_information": self.contact_information,
            "patents": self.patents,
            "competitors": self.competitors,
            "research_analysis": self.research_analysis,
            "patent_activity": self.patent_activity,
            "all_investments": self.all_investments,
            "faq": self.faq,
            "investors": self.investors,
        }