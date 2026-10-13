#!/usr/bin/env python3
"""
Scientia Venture Diligence Auditor (v1.1.0)
Automated Term Sheet, SAFE Agreement, and Due Diligence Risk Scoring Engine.
Repurposed from open-source document intelligence (Docling / LlamaIndex pattern).

Scientia Partners · Independent Advisory & Engineering Hub · UAE
hello@scientiapartners.com
"""

import argparse
import json
import re
import sys
from typing import Dict, Any, List


class VentureDiligenceAuditor:
    def __init__(self, target_company: str, stage: str = "Seed / Series A"):
        self.target_company = target_company
        self.stage = stage

    def analyze_terms(self, contract_text: str) -> Dict[str, Any]:
        """
        Parses legal terms and identifies high/medium/low severity risks for founders.
        """
        findings: List[Dict[str, Any]] = []
        text_lower = contract_text.lower()

        # 1. Liquidation Preference Check
        if "participating preferred" in text_lower or "participating liquidation" in text_lower:
            findings.append({
                "category": "Liquidation Preference",
                "severity": "HIGH",
                "clause_detected": "Participating Preferred Stock detected",
                "risk_explanation": "Investors get their money back first AND participate pro-rata in remaining proceeds ('double-dipping'). Highly detrimental to founder exit value.",
                "recommendation": "Negotiate to 1x Non-Participating Preferred, which is standard venture market practice."
            })
        elif "2x" in text_lower or "3x" in text_lower:
            findings.append({
                "category": "Liquidation Preference",
                "severity": "HIGH",
                "clause_detected": "Multiple liquidation preference (>1x) found",
                "risk_explanation": "Multiple liquidation returns create a high hurdle before common shareholders/founders see liquidity.",
                "recommendation": "Cap liquidation preference at strictly 1.0x."
            })
        else:
            findings.append({
                "category": "Liquidation Preference",
                "severity": "LOW",
                "clause_detected": "Standard 1x Non-Participating or SAFE return",
                "risk_explanation": "Aligns with institutional seed/venture standards.",
                "recommendation": "Acceptable in current form."
            })

        # 2. Anti-Dilution Protection Check
        if "full ratchet" in text_lower:
            findings.append({
                "category": "Anti-Dilution",
                "severity": "CRITICAL",
                "clause_detected": "Full Ratchet Anti-Dilution clause identified",
                "risk_explanation": "In any down-round, investor shares re-price entirely to the lowest price, severely diluting common shareholders/founders.",
                "recommendation": "Remove immediately. Insist on Broad-Based Weighted Average anti-dilution only."
            })
        elif "weighted average" in text_lower:
            findings.append({
                "category": "Anti-Dilution",
                "severity": "LOW",
                "clause_detected": "Broad-Based Weighted Average",
                "risk_explanation": "Standard institutional protection formula.",
                "recommendation": "Maintain standard formula definitions."
            })

        # 3. Founder Vesting & IP Assignment
        if "immediate forfeiture" in text_lower or "bad leaver includes termination without cause" in text_lower:
            findings.append({
                "category": "Founder Vesting",
                "severity": "HIGH",
                "clause_detected": "Aggressive Bad Leaver forfeiture definitions",
                "risk_explanation": "Founders could lose vested equity even upon termination without fault.",
                "recommendation": "Restrict 'Bad Leaver' strictly to fraud, gross misconduct, or material felony conviction."
            })

        if "assignment of inventions" not in text_lower and "intellectual property assignment" not in text_lower:
            findings.append({
                "category": "IP & Intangibles",
                "severity": "MEDIUM",
                "clause_detected": "No explicit company IP assignment warranty",
                "risk_explanation": "Investors will halt funding until all founder/contractor IP is irrevocably assigned to the holding company.",
                "recommendation": "Include comprehensive Proprietary Information and Inventions Agreement (PIIA) schedule."
            })

        # 4. Governance & Protective Provisions
        if "supermajority" in text_lower or "veto right" in text_lower or "protective provisions" in text_lower:
            findings.append({
                "category": "Board Governance",
                "severity": "MEDIUM",
                "clause_detected": "Investor veto covenants on operating budgets",
                "risk_explanation": "Could restrict founder operational flexibility for day-to-day capital expenditure or hiring.",
                "recommendation": "Limit veto rights strictly to fundamental corporate transactions (M&A, liquidation, charter changes)."
            })

        # Calculate composite score (out of 100)
        high_count = sum(1 for f in findings if f["severity"] in ["CRITICAL", "HIGH"])
        medium_count = sum(1 for f in findings if f["severity"] == "MEDIUM")
        score = max(20, 100 - (high_count * 25) - (medium_count * 10))

        risk_level = "GREEN (Clean & Investible)" if score >= 80 else "AMBER (Negotiation Required)" if score >= 60 else "RED (High Founder Risk)"

        return {
            "target_company": self.target_company,
            "stage": self.stage,
            "overall_score": score,
            "risk_profile": risk_level,
            "critical_flags_count": high_count,
            "total_clauses_reviewed": len(findings),
            "findings": findings
        }


def main():
    parser = argparse.ArgumentParser(description="Scientia Venture Diligence Auditor CLI")
    parser.add_argument("--company", default="Kite Mobility Technologies", help="Target startup name")
    parser.add_argument("--stage", default="Seed Round", help="Investment stage")
    parser.add_argument("--file", help="Path to text or markdown term sheet")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    sample_contract = """
    TERM SHEET - SERIES SEED INVESTMENT
    Target Company: Kite Mobility Technologies (DIFC)
    Security: Series Seed Participating Preferred Shares.
    Liquidation Preference: 1.5x Participating Liquidation Preference with no cap.
    Anti-Dilution: Broad-Based Weighted Average.
    Founder Vesting: 4-year monthly vesting with 1-year cliff. Bad leaver includes termination without cause.
    Board Representation: Lead Investor holds negative veto rights over annual budgets exceeding $50k.
    """

    content = sample_contract
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()

    auditor = VentureDiligenceAuditor(target_company=args.company, stage=args.stage)
    result = auditor.analyze_terms(content)

    if args.json:
        print(json.dumps(result, indent=2))
        return

    print("=" * 72)
    print("  SCIENTIA PARTNERS · VENTURE DILIGENCE AUDITOR (TERM SHEET RISK)")
    print("=" * 72)
    print(f"Target Company:     {result['target_company']}")
    print(f"Stage:              {result['stage']}")
    print(f"Diligence Score:    {result['overall_score']}/100")
    print(f"Risk Profile:       {result['risk_profile']}")
    print(f"Critical Flags:     {result['critical_flags_count']}")
    print("-" * 72)
    for idx, f in enumerate(result['findings'], 1):
        print(f"[{f['severity']}] Clause {idx}: {f['category']} - {f['clause_detected']}")
        print(f"   Risk:           {f['risk_explanation']}")
        print(f"   Recommendation: {f['recommendation']}")
        print()
    print("=" * 72)


if __name__ == "__main__":
    main()