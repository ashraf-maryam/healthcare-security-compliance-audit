"""Generate evidence from the fictional clinic model."""
import json
from pathlib import Path
from src.clinic import SyntheticClinic

def main():
    clinic = SyntheticClinic()
    checks = {
        'doctor_allowed': clinic.access_record('doc01', 'P-100'),
        'patient_allowed': clinic.access_record('patient01', 'P-100'),
        'disabled_user_denied': not clinic.access_record('former01', 'P-100'),
        'administrator_denied': not clinic.access_record('admin01', 'P-100'),
        'unknown_user_denied': not clinic.access_record('unknown', 'P-100'),
        'audit_events_recorded': len(clinic.audit_events) == 5,
        'unique_test_user_ids': len(clinic.users) == len(set(clinic.users)),
        'all_enabled_users_have_mfa': len(clinic.users_without_mfa()) == 0,
        'inactive_accounts_identified': len(clinic.disabled_users()) > 0,
    }
    results = {
        'system': 'SyntheticClinic local in-memory demo',
        'data_classification': 'SYNTHETIC ONLY',
        'checks': checks,
        'mfa_exceptions': clinic.users_without_mfa(),
        'disabled_user_ids': clinic.disabled_users(),
        'audit_events': clinic.audit_events,
        'note': 'A failed check indicates a known demo gap, not a formal compliance finding.',
    }
    output = Path(__file__).resolve().parents[1] / 'evidence' / 'assessment_results.json'
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(results, indent=2) + '\n')
    print(f'Wrote {output}. Checks met: {sum(checks.values())}/{len(checks)}.')

if __name__ == '__main__':
    main()
