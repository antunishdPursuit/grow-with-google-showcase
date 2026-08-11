# Apex Engineers: Business Readiness Check

## UN Sustainable Development Goal

[Goal 9: Industry, Innovation, and Infrastructure](https://sdgs.un.org/goals/goal9)

## Problem Statement

Traditional mom-and-pop retail storefronts lack a simple, automated way to
assess and update their old administrative software.

## Overview

Apex Engineers is building a project to help small retail and e-commerce
businesses review the tools they use to run their business.

The Business Readiness Check focuses on four gaps supported by the team's
research: inventory synchronization, payments and checkout, customer email
capture, and online booking. It gives a non-technical owner a weighted risk
result and practical next steps in a few minutes.

The project does not replace a point-of-sale system, process payments, schedule
appointments, or perform a formal security or compliance audit.

## How the Solution Works

1. The owner optionally enters a business name and type.
2. The owner answers four questions with **Yes**, **No**, or **Not applicable**.
3. Python applies the research-derived question weights: 5, 4, 3, and 2.
4. The application calculates the applicable risk percentage.
5. Failed areas are ordered from highest to lowest weight.
6. The owner receives recommendations and can download a plain-text report.

The risk categories are project-designed interpretation bands:

| Percentage | Result |
| ---: | --- |
| 0-24% | Low |
| 25-49% | Moderate |
| 50-74% | High |
| 75-100% | Critical |

These categories are not externally validated standards. **Not applicable**
answers are excluded from the denominator. If every area is not applicable,
the tool returns no score instead of reporting zero risk.

## Current Features

- Four-question Streamlit assessment.
- Weighted scoring with applicable-question handling.
- Highest-priority gap identification.
- Ordered modernization recommendations.
- Downloadable plain-text results report.
- Input normalization, safe errors, a privacy notice, and a disclaimer.
- Automated tests for scoring, invalid input, priorities, and report output.

## Project Status

The minimum application is built, and all automated tests pass. A final
localhost review, public deployment, walkthrough video, commit, push, and pull
request remain incomplete.

## Team

- Ramya Kota - Data Analytics
- Dennys Antunish - IT Automation with Python
- Sukanya Karri - Cybersecurity
- Aishat Omolabake Ajibola - Advanced Data Analytics

Dennys Antunish implemented the application and repository deliverables. The
research and analysis supplied the problem framing and diagnostic criteria.

## Grow with Google Resources Used

- Google IT Automation with Python
- Python scripting and testing
- Git and GitHub collaboration
- Troubleshooting and secure automation practices

## Project Structure

```text
apex-engineers-business-readiness-check/
|-- app.py
|-- diagnostic.py
|-- requirements.txt
|-- README.md
|-- SECURITY.md
|-- LICENSE
|-- tests/
|   `-- test_diagnostic.py
`-- docs/
    |-- implementation-plan.md
    `-- project-summary.md
```

## Run Locally

Prerequisite: Python 3.10 or newer.

```bash
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Install the dependencies and start the application:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Streamlit will display the local application address in the terminal.

## Run the Tests

The test suite works with either command:

```bash
python -m unittest discover -s tests -v
python -m pytest -q
```

## Public Application

Public deployment is planned. The verified application URL will be added here
after deployment testing is complete.

## Project Walkthrough Video

The final walkthrough video, no longer than five minutes, will be linked here
after recording.

## Research and Limitations

The diagnostic questions and weights come from the team's project report and
analysis of a global e-commerce dataset. Supporting articles and surveys were
used to frame the challenges of small retailers.

The dataset is an illustrative e-commerce case study. It does not prove that
every traditional storefront experiences the same rates or problems. The tool
therefore provides general guidance rather than guaranteed outcomes.

- [Project report and diagnostic criteria](https://docs.google.com/document/d/1OFAOKCO0PFtaKKfRQRJTysoO7rNMozFNBWTMYOUmOcI/edit)
- [MMC BUILD Project Outline](https://docs.google.com/document/d/1InNWpho03JfFCXKAuMmXqKNMXpoGoRerdZamuqvCQ2M/edit?tab=t.0)

## Future Ideas

- Optional inventory and customer-data file checks.
- More diagnostic areas, including accounting and shipping.
- Carefully researched vendor comparisons.
- A longer modernization roadmap.
- User testing with small-business owners.

These ideas are outside the current submission scope.

## License

This project is available under the [MIT License](LICENSE).
