# Scope and system design

The fictional organization is Northstar Community Clinic. This exercise does not involve a real healthcare provider.

The Python program has five sample accounts: a doctor, a nurse, a patient, a disabled former employee, and an administrator. It contains one fake record and checks whether each user should be able to read it. Each attempted read creates an event in memory.

```text
[Tests / assessment script]
             |
             v
[Python access-control check] ---> [Fake patient record]
             |
             v
    [In-memory audit events]
```

**Included:** simplified role-based access decisions, disabled-account behavior, MFA configuration flags, test events, and a control matrix.

**Not included:** real login or MFA, an HTTP API, a database, encryption, cloud deployment, persistent logs, backups, physical safeguards, or an actual compliance audit.

I classified risks using likelihood × impact, each scored from 1 (low) to 5 (high). Scores of 1–4 are Low, 5–9 Medium, and 10–25 High. These are judgment-based sample scores, not measured probabilities.
