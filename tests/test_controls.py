import unittest
from src.clinic import SyntheticClinic

class ControlTests(unittest.TestCase):
    def setUp(self):
        self.clinic = SyntheticClinic()

    def test_authorized_doctor_can_read(self):
        self.assertTrue(self.clinic.access_record('doc01', 'P-100'))

    def test_patient_can_read_own_record(self):
        self.assertTrue(self.clinic.access_record('patient01', 'P-100'))

    def test_disabled_account_denied(self):
        self.assertFalse(self.clinic.access_record('former01', 'P-100'))

    def test_administrator_no_clinical_access(self):
        self.assertFalse(self.clinic.access_record('admin01', 'P-100'))

    def test_unknown_user_denied(self):
        self.assertFalse(self.clinic.access_record('unknown', 'P-100'))

    def test_access_decisions_are_audited(self):
        self.clinic.access_record('doc01', 'P-100')
        self.clinic.access_record('unknown', 'P-100')
        self.assertEqual([e['decision'] for e in self.clinic.audit_events], ['ALLOW', 'DENY'])
        self.assertTrue(all(e['actor'] and e['at'] for e in self.clinic.audit_events))

    def test_unique_test_identities(self):
        self.assertEqual(len(self.clinic.users), len(set(self.clinic.users.keys())))

    def test_known_mfa_gap_is_detected(self):
        # Detection passes; the security finding remains open.
        self.assertEqual(self.clinic.users_without_mfa(), ['admin01'])

    def test_disabled_account_recorded(self):
        self.assertEqual(self.clinic.disabled_users(), ['former01'])

    def test_nurse_can_read_record(self):
        self.assertTrue(self.clinic.access_record('nurse01', 'P-100'))

    def test_patient_cannot_read_another_patients_record(self):
        self.clinic.records['P-200'] = {
            'patient_uid': 'other_patient', 'clinical_note': 'SYNTHETIC TEST ONLY'
        }
        self.assertFalse(self.clinic.access_record('patient01', 'P-200'))

    def test_missing_record_denied(self):
        self.assertFalse(self.clinic.access_record('doc01', 'DOES-NOT-EXIST'))

    def test_denial_creates_audit_event(self):
        self.assertFalse(self.clinic.access_record('former01', 'P-100'))
        self.assertEqual(self.clinic.audit_events[-1]['decision'], 'DENY')
        self.assertEqual(self.clinic.audit_events[-1]['actor'], 'former01')

    def test_audit_log_is_not_durable(self):
        self.clinic.access_record('doc01', 'P-100')
        self.assertEqual(len(self.clinic.audit_events), 1)
        self.assertEqual(len(SyntheticClinic().audit_events), 0)

    def test_no_real_patient_information(self):
        self.assertIn('SYNTHETIC', self.clinic.records['P-100']['clinical_note'])

if __name__ == '__main__':
    unittest.main()
