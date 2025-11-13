from __future__ import annotations

from src.extractors.company_profile_parser import parse_company_profile
from src.extractors.investments_parser import parse_investments
from src.extractors.competitors_parser import parse_competitors
from src.extractors.faq_parser import parse_faq
from src.models.company_profile import CompanyProfile

def test_company_profile_parsing_basic():
    html = """
    <html>
      <head>
        <title>Badia Spices - PitchBook</title>
        <script type="application/ld+json">
        {
          "@context": "http://schema.org",
          "@type": "Organization",
          "@id": "361831-87",
          "name": "Badia Spices",
          "description": "Manufacturer and distributor of food ingredients based in Doral, Florida."
        }
        </script>
      </head>
      <body>
        <p data-test="company-description">Manufacturer and distributor of food ingredients based in Doral, Florida.</p>
        <table>
          <tr><th>Founded</th><td>1967</td></tr>
          <tr><th>Ownership Status</th><td>Private</td></tr>
          <tr><th>Employees</th><td>101</td></tr>
        </table>
        <a href="https://www.facebook.com/BadiaSpices">Facebook</a>
        <a href="https://twitter.com/badiaspices">Twitter</a>
        <a href="https://www.linkedin.com/company/badia-spices-inc.">LinkedIn</a>
        <ul>
          <li data-type="Website">www.badiaspices.com</li>
        </ul>
      </body>
    </html>
    """
    basics = parse_company_profile(html, "https://pitchbook.com/profiles/company/361831-87")
    assert basics["company_name"] == "Badia Spices"
    assert basics["year_founded"] == 1967
    assert basics["status"] == "Private"
    assert basics["employees"] == 101
    assert len(basics["company_socials"]) >= 3
    assert basics["contact_information"][0]["Type"] == "Website"

def test_investments_and_competitors_and_faq():
    html = """
    <html>
      <body>
        <div data-test="deal-summary">
          <span>Latest deal type: Buyout/​LBO</span>
        </div>
        <table>
          <tr>
            <th>Company</th><th>Date</th><th>Deal Size</th><th>Deal Type</th><th>Industry</th>
          </tr>
          <tr>
            <td>Tech Data (Warehouse in Sweetwater, Texas)</td>
            <td>2020-11-03</td>
            <td>n/a</td>
            <td>Corporate Asset Purchase</td>
            <td>Buildings and Property</td>
          </tr>
        </table>
        <table>
          <tr>
            <th>Competitor</th><th>Status</th><th>Location</th>
          </tr>
          <tr>
            <td><a href="https://pitchbook.com/profiles/company/233704-27">Louisiana Fish Fry</a></td>
            <td>Private Equity-Backed</td>
            <td>Baton Rouge, LA</td>
          </tr>
        </table>
        <section>
          <h2>FAQ</h2>
          <div data-test="faq-item">
            <h3 data-test="faq-question">When was Badia Spices founded?</h3>
            <p data-test="faq-answer">Badia Spices was founded in 1967.</p>
          </div>
        </section>
        <div data-test="investors">
          <a>BDT &amp; MSD Partners</a>
        </div>
      </body>
    </html>
    """

    summary, all_investments, investors = parse_investments(html)
    assert summary["latest_deal_type"].startswith("Buyout")
    assert summary["financing_rounds"] == 1
    assert len(all_investments) == 1
    assert investors == ["BDT & MSD Partners"]

    competitors = parse_competitors(html)
    assert len(competitors) == 1
    assert competitors[0]["company_name"] == "Louisiana Fish Fry"

    faq = parse_faq(html)
    assert any(entry["type"] == "Question" for entry in faq)
    assert any(entry["type"] == "Answer" for entry in faq)

    basics = {
        "url": "https://pitchbook.com/profiles/company/361831-87",
        "id": "361831-87",
        "company_name": "Badia Spices",
        "company_socials": [],
        "year_founded": 1967,
        "status": "Private",
        "employees": 101,
        "latest_deal_type": None,
        "financing_rounds": None,
        "investments": None,
        "description": "Manufacturer and distributor of food ingredients based in Doral, Florida.",
        "contact_information": [],
        "patents": None,
        "research_analysis": None,
        "patent_activity": None,
    }

    profile = CompanyProfile.from_parsed_parts(
        basics=basics,
        investments_summary=summary,
        competitors=competitors,
        all_investments=all_investments,
        faq=faq,
        investors=investors,
    )
    record = profile.to_dict()
    assert record["company_name"] == "Badia Spices"
    assert record["latest_deal_type"].startswith("Buyout")
    assert len(record["competitors"]) == 1
    assert len(record["all_investments"]) == 1
    assert len(record["faq"]) >= 2
    assert record["investors"] == ["BDT & MSD Partners"]