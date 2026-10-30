# Healthcare security assurance: sample assessment

**System:** Northstar Community Clinic (fictional)  
**Assessment:** Independent learning project, October 2026  
**Data:** Synthetic test accounts and record only

## Why I did this

I wanted to work through the steps of a security compliance assessment rather than only read about frameworks. I built a small Python access-control model, wrote repeatable tests, mapped selected observations to control objectives, and recorded findings with suggested fixes.

## Scope and results

I reviewed 12 control objectives: 5 passed within the limited program, 2 had observable gaps, and 5 could not be assessed with this environment. The 15 unit tests verify how the software behaves. They are not evidence of compliance with all mapped standards.

The mappings to NIST SP 800-53, HIPAA Security Rule provisions and ISO 27001 themes are illustrative. I did not assess an actual covered entity or perform a certification audit.

## Finding R-01: Administrator MFA missing

- **Control:** C-05
- **Evidence:** `admin01` is active but has `mfa_enabled=False`; the assessment script lists it as an exception.
- **Risk:** In a real application, privileged access without MFA could make account compromise more damaging.
- **Recommendation:** Require MFA for privileged accounts, track approved exceptions, and retest.
- **Limitation:** This is a stored configuration flag, not an actual authentication implementation.
- **Status:** Open.

## Finding R-02: Audit events are not retained

- **Control:** C-07
- **Evidence:** Access attempts produce events in `audit_events`, but a new program instance begins with an empty list.
- **Risk:** Logs could be unavailable for incident investigation and required reviews.
- **Recommendation:** Move events to protected persistent storage, define retention periods and access permissions, and test integrity.
- **Limitation:** No database or central logging service exists in this prototype.
- **Status:** Open.

## Next steps

1. Add simulated fixes for MFA enforcement and durable logging, then rerun control tests.
2. Expand scope to a deployed service before claiming anything about transport encryption or incident recovery.
3. Revisit applicability and evidence requirements for each framework before using this method in a real assessment.

## Supporting files

- [Control matrix](../controls/control_matrix.csv)
- [Risk register](../risks/risk_register.csv)
- [Assessment evidence](../evidence/assessment_results.json)
- [Scope](../scope/system_design.md)
- [Unit tests](../tests/test_controls.py)

## References

- [NIST SP 800-53 Rev. 5](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- [HHS HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html)
- [HIPAA technical safeguards, 45 CFR §164.312](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-C/section-164.312)
- [ISO/IEC 27001 overview](https://www.iso.org/standard/27001)
