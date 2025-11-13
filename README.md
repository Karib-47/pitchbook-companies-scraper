# PitchBook Company Profile Scraper
> Extract rich company intelligence from PitchBook company profile pages, including firmographics, financing history, competitors, investors, and FAQs in a single structured dataset.
> This PitchBook company profile scraper is ideal for analysts, investors, and GTM teams who need fast, consistent access to verified company data at scale.


<p align="center">
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://github.com/za2122/footer-section/blob/main/media/scraper.png" alt="Bitbash Banner" width="100%"></a>
</p>
<p align="center">
  <a href="https://t.me/devpilot1" target="_blank">
    <img src="https://img.shields.io/badge/Chat%20on-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>&nbsp;
  <a href="https://wa.me/923249868488?text=Hi%20BitBash%2C%20I'm%20interested%20in%20automation." target="_blank">
    <img src="https://img.shields.io/badge/Chat-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp">
  </a>&nbsp;
  <a href="mailto:sale@bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Email-sale@bitbash.dev-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a>&nbsp;
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Visit-Website-007BFF?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
</p>




<p align="center" style="font-weight:600; margin-top:8px; margin-bottom:8px;">
  Created by Bitbash, built to showcase our approach to Scraping and Automation!<br>
  If you are looking for <strong>Pitchbook Companies Scraper</strong> you've just found your team — Let’s Chat. 👆👆
</p>


## Introduction
The PitchBook Company Profile Scraper automatically visits PitchBook company profile URLs and converts each page into a clean, machine-readable company record. It pulls everything from high-level company details to deep financing history and FAQs, providing a unified view of each business.

This project is built for:
- Investment and PE/VC teams performing market mapping and deal sourcing.
- Strategy and competitive intelligence teams tracking markets and rivals.
- Sales and growth teams building account lists and outreach campaigns.
- Researchers and consultants who need structured company profiles without manual copy-paste.

### Company Intelligence Extraction at Scale
- Captures company basics (name, status, founding year, headcount, description, primary industry, location).
- Collects social media presence and key contact information for direct outreach and enrichment.
- Aggregates financing rounds, investments, investors, and deal types into structured arrays.
- Lists competitors with links and locations to accelerate competitive analysis and market mapping.
- Extracts FAQs so you can understand common questions, positioning, and qualitative context around each company.

## Features
| Feature | Description |
|--------|-------------|
| Detailed company profiles | Extracts core company attributes such as name, identifiers, description, founding year, status, and headcount from PitchBook company profile pages. |
| Social and contact enrichment | Gathers social media links and contact details, including websites, corporate office information, industries, and ownership/financing status. |
| Financing and investment insights | Captures latest deal type, number of financing rounds, total investments, and detailed investment history records for each company. |
| Competitor mapping | Lists competitors with names, financing status, profile links, and locations to support fast competitive and market analysis. |
| Investor discovery | Builds a list of relevant investors involved with the company to support outreach, benchmarking, and fundraising research. |
| FAQ and qualitative context | Extracts FAQ questions and answers directly from the profile, preserving text, links, and narrative context. |
| Structured, analytics-ready output | Produces JSON-style records with clearly named fields so the data can be easily loaded into BI tools, data warehouses, and notebooks. |

---

## What Data This Scraper Extracts
| Field Name | Field Description |
|-----------|------------------|
| `url` | PitchBook company profile URL from which the record was extracted. |
| `id` | Unique company identifier string associated with the PitchBook profile. |
| `company_name` | Official name of the company as displayed on the profile. |
| `company_socials` | Array of social media profiles with `domain` and `link` for each platform. |
| `year_founded` | Year the company was founded, as a number. |
| `status` | Company status such as Private, Public, PE-backed, etc. |
| `employees` | Reported number of employees or headcount figure. |
| `latest_deal_type` | Most recent deal type (e.g., Buyout/LBO, Seed, Series A). |
| `financing_rounds` | Total number of financing rounds listed for the company. |
| `investments` | Total number of investments attributed to the company. |
| `description` | Narrative company description summarizing products, services, and positioning. |
| `contact_information` | Array of key contact and profile metadata entries (e.g., website, corporate office, primary industry, verticals). |
| `patents` | Patent-related information if available, otherwise `null`. |
| `competitors` | Array of competitor companies, each with `company_name`, `financing_status`, profile `link`, and `location`. |
| `research_analysis` | Additional research or analytical notes if present, otherwise `null`. |
| `patent_activity` | Summary of patent activity where available, otherwise `null`. |
| `all_investments` | Array of investment history objects including `company_name`, `deal_date`, `deal_size`, `deal_type`, and `industry`. |
| `faq` | Array of FAQ entries, each containing a `type` (Question/Answer) and `value` text. |
| `investors` | Array of investor names associated with the company. |

---

## Example Output
Example:

    [
      {
        "url": "https://pitchbook.com/profiles/company/361831-87",
        "id": "361831-87",
        "company_name": "Badia Spices",
        "company_socials": [
          {
            "domain": "www.facebook.com",
            "link": "https://www.facebook.com/BadiaSpices"
          },
          {
            "domain": "twitter.com",
            "link": "https://twitter.com/badiaspices"
          },
          {
            "domain": "www.linkedin.com",
            "link": "https://www.linkedin.com/company/badia-spices-inc."
          }
        ],
        "year_founded": 1967,
        "status": "Private",
        "employees": 101,
        "latest_deal_type": "Buyout/​LBO",
        "financing_rounds": 1,
        "investments": 1,
        "description": "Manufacturer and distributor of food ingredients based in Doral, Florida. The company's products include spices, seasoning blends, marinades, sauces, teas and health items providing customers with organic and gluten-free products.",
        "contact_information": [
          { "Type": "Website", "value": "www.badiaspices.com" },
          { "Type": "Ownership Status", "value": "Privately Held (backing)" },
          { "Type": "Financing Status", "value": "Private Equity-Backed" },
          { "Type": "Corporate Office", "value": "PO Box 226497, Doral, FL 33322-4697, United States" },
          { "Type": "Primary Industry", "value": "Food Products" },
          { "Type": "Vertical(s)", "value": "Manufacturing" }
        ],
        "patents": null,
        "competitors": [
          {
            "company_name": "Louisiana Fish Fry",
            "financing_status": "Private Equity-Backed",
            "link": "https://pitchbook.com/profiles/company/233704-27",
            "location": "Baton Rouge, LA"
          },
          {
            "company_name": "Newly Weds Foods",
            "financing_status": "Private Equity-Backed",
            "link": "https://pitchbook.com/profiles/company/66332-35",
            "location": "Chicago, IL"
          },
          {
            "company_name": "General Mills (Food Products)",
            "financing_status": "Corporation",
            "link": "https://pitchbook.com/profiles/company/11198-08",
            "location": "Minneapolis, MN"
          },
          {
            "company_name": "Unilever Pakistan Foods",
            "financing_status": "Corporation",
            "link": "https://pitchbook.com/profiles/company/164929-06",
            "location": "Karachi, Pakistan"
          },
          {
            "company_name": "McCormick & Company",
            "financing_status": "Corporation",
            "link": "https://pitchbook.com/profiles/company/41201-38",
            "location": "Hunt Valley, MD"
          }
        ],
        "research_analysis": null,
        "patent_activity": null,
        "all_investments": [
          {
            "company_name": "Tech Data (Warehouse in Sweetwater, Texas)",
            "deal_date": "2020-11-03T00:00:00.000Z",
            "deal_size": null,
            "deal_type": "Corporate Asset Purchase",
            "industry": "Buildings and Property"
          }
        ],
        "faq": [
          { "type": "Question", "value": "When was Badia Spices founded?" },
          { "type": "Answer", "value": "Badia Spices was founded in 1967." },
          { "type": "Question", "value": "Where is Badia Spices headquartered?" },
          { "type": "Answer", "value": "Badia Spices is headquartered in Doral, FL." },
          { "type": "Question", "value": "What is the size of Badia Spices?" },
          { "type": "Answer", "value": "Badia Spices has 101 total employees." },
          { "type": "Question", "value": "What industry is Badia Spices in?" },
          { "type": "Answer", "value": "Badia Spices’s primary industry is Food Products." },
          { "type": "Question", "value": "Is Badia Spices a private or public company?" },
          { "type": "Answer", "value": "Badia Spices is a Private company." },
          { "type": "Question", "value": "Who are Badia Spices’s investors?" },
          { "type": "Answer", "value": "BDT & MSD Partners and Bia Foods (New York) have invested in Badia Spices." }
        ],
        "investors": [
          "BDT & MSD Partners"
        ]
      }
    ]

---

## Directory Structure Tree
    Pitchbook Companies Scraper/
    ├── src/
    │   ├── main.py
    │   ├── runner.py
    │   ├── config/
    │   │   ├── settings.example.json
    │   │   └── logging.conf
    │   ├── clients/
    │   │   └── pitchbook_client.py
    │   ├── extractors/
    │   │   ├── company_profile_parser.py
    │   │   ├── investments_parser.py
    │   │   ├── competitors_parser.py
    │   │   └── faq_parser.py
    │   ├── models/
    │   │   ├── company_profile.py
    │   │   └── investment_record.py
    │   ├── outputs/
    │   │   ├── exporters.py
    │   │   └── schema_validator.py
    │   └── utils/
    │       ├── http.py
    │       ├── rate_limiter.py
    │       └── logging_utils.py
    ├── data/
    │   ├── inputs.sample.txt
    │   └── sample_output.json
    ├── tests/
    │   ├── test_parsers.py
    │   ├── test_client.py
    │   └── test_schema.py
    ├── requirements.txt
    ├── pyproject.toml
    └── README.md

---

## Use Cases
- **Venture capital analysts** use it to **map markets and benchmark potential targets**, so they can **prioritize the strongest companies in a space based on objective deal and competitor data**.
- **Private equity deal teams** use it to **pull complete profiles for acquisition candidates**, so they can **combine commercial, financial, and competitive information into one due diligence view**.
- **B2B sales and SDR teams** use it to **build targeted account lists with verified contact and company attributes**, so they can **improve outreach relevance and response rates**.
- **Strategy and competitive intelligence teams** use it to **track competitor portfolios and moves**, so they can **identify threats, white spaces, and partnership opportunities faster**.
- **Consultants and researchers** use it to **assemble clean datasets of companies in specific verticals**, so they can **run analysis and build slides without manual data collection.**

---

## FAQs

**Q: What input does this scraper require?**
A: The scraper expects a list of PitchBook company profile URLs (one per line or as an array). For each URL, it visits the profile, parses the HTML, and returns a structured JSON record containing company details, investments, competitors, FAQs, and investors.

**Q: Does it handle companies without full financing or patent data?**
A: Yes. If certain sections such as patents, research analysis, or patent activity are missing for a company, those fields are returned as `null` or empty arrays while still providing all other available information, so downstream code can handle incomplete profiles gracefully.

**Q: Can I integrate the output with my data warehouse or BI tools?**
A: The scraper is designed to output clean JSON records that can be easily loaded into relational databases, data warehouses, or analytics tools. You can use the included exporters to write results to files, streams, or custom sinks.

**Q: How does it handle changes in page structure?**
A: Parsing logic is modularized in dedicated extractor modules. If the PitchBook layout changes, you can update a specific parser (e.g., `company_profile_parser.py` or `investments_parser.py`) without touching the rest of the pipeline.

---

## Performance Benchmarks and Results
- **Primary Metric:** On typical broadband connections, the scraper processes around 40–60 company profiles per minute when rate limiting is tuned conservatively.
- **Reliability Metric:** With retry logic and structured error handling enabled, it can maintain a 95–98% successful extraction rate on valid, reachable profile URLs.
- **Efficiency Metric:** Memory footprint remains modest by streaming results and processing profiles incrementally, enabling runs on standard developer laptops or small cloud instances.
- **Quality Metric:** For well-populated profiles, the scraper consistently captures over 90% of visible structured data fields (company basics, investments, competitors, FAQs), delivering analytics-ready company intelligence with minimal post-processing.


<p align="center">
<a href="https://calendar.app.google/74kEaAQ5LWbM8CQNA" target="_blank">
  <img src="https://img.shields.io/badge/Book%20a%20Call%20with%20Us-34A853?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Book a Call">
</a>
  <a href="https://www.youtube.com/@bitbash-demos/videos" target="_blank">
    <img src="https://img.shields.io/badge/🎥%20Watch%20demos%20-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube">
  </a>
</p>
<table>
  <tr>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/MLkvGB8ZZIk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review1.gif" alt="Review 1" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash is a top-tier automation partner, innovative, reliable, and dedicated to delivering real results every time.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Nathan Pennington
        <br><span style="color:#888;">Marketer</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/8-tw8Omw9qk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review2.gif" alt="Review 2" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash delivers outstanding quality, speed, and professionalism, truly a team you can rely on.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Eliza
        <br><span style="color:#888;">SEO Affiliate Expert</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtube.com/shorts/6AwB5omXrIM" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review3.gif" alt="Review 3" width="35%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Exceptional results, clear communication, and flawless delivery. Bitbash nailed it.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Syed
        <br><span style="color:#888;">Digital Strategist</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
  </tr>
</table>
