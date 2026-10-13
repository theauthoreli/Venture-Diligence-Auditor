# Scientia Venture Diligence Auditor

> **Automated SAFE & Term Sheet Risk Scoring Engine for Founders & Emerging Fund Managers**  
> Built by **Scientia Partners** (UAE) · [hello@scientiapartners.com](mailto:hello@scientiapartners.com)  
> Permissive Open-Source Foundation: MIT Licensed

---

## Overview

Founders raising institutional venture capital often agree to aggressive investor covenants without understanding their long-term equity dilution impact.

`venture-diligence-auditor` scans investment agreements (Y Combinator SAFEs, NVCA term sheets, BVCA seed documents, and DIFC/ADGM convertible instruments) and performs an instant red-flag audit against founder-hostile terms:
- **Participating Preferred / Double-Dipping** liquidation preferences
- **Full Ratchet** anti-dilution clauses
- **Uncapped MFN (Most Favored Nation)** clauses
- **Overly Broad Bad-Leaver** equity forfeitures
- **Operational Budget Vetoes** that cripple founder autonomy

---

## Quickstart & Installation

```bash
git clone https://github.com/YOUR_USERNAME/venture-diligence-auditor.git
cd venture-diligence-auditor

pip install -r requirements.txt

# Run term sheet analysis
python diligence_auditor.py --company "Falcon AI Labs" --stage "Seed Round"
