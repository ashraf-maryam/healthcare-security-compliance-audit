"""Fictional clinic records and access checks. No real patient information."""
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class User:
    uid: str
    role: str
    enabled: bool = True
    mfa_enabled: bool = True

class SyntheticClinic:
    def __init__(self):
        self.users = {
            'doc01': User('doc01', 'doctor'),
            'nurse01': User('nurse01', 'nurse'),
            'patient01': User('patient01', 'patient'),
            'former01': User('former01', 'nurse', enabled=False),
            'admin01': User('admin01', 'administrator', mfa_enabled=False),
        }
        self.records = {'P-100': {'patient_uid': 'patient01', 'clinical_note': 'SYNTHETIC TEST ONLY'}}
        self.audit_events = []
        self.permissions = {
            'doctor': {'read_record'},
            'nurse': {'read_record'},
            'patient': {'read_own_record'},
            'administrator': {'manage_users'},
        }

    def access_record(self, uid, record_id):
        user = self.users.get(uid)
        record = self.records.get(record_id)
        allowed = bool(user and user.enabled and record and (
            'read_record' in self.permissions[user.role] or
            ('read_own_record' in self.permissions[user.role] and record['patient_uid'] == uid)
        ))
        self.audit_events.append({
            'at': datetime.now(timezone.utc).isoformat(),
            'actor': uid,
            'action': 'read_record',
            'record_id': record_id,
            'decision': 'ALLOW' if allowed else 'DENY',
        })
        return allowed

    def users_without_mfa(self):
        return sorted(uid for uid, user in self.users.items() if user.enabled and not user.mfa_enabled)

    def disabled_users(self):
        return sorted(uid for uid, user in self.users.items() if not user.enabled)
