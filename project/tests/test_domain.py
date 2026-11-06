"""Student-authored Stage 7 domain tests (revision 2 contracts)."""

from datetime import datetime, timezone

import pytest

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)

NINE_AM = datetime(2026, 10, 1, 9, 0)


def make_appointment(status=AppointmentStatus.SCHEDULED) -> Appointment:
    """Fresh synthetic participants and appointment for each test."""
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General practice')
    return Appointment('A1', patient, practitioner, NINE_AM, status)


def test_patient_stores_trimmed_id_and_name() -> None:
    """TEST-01: valid input is stored, surrounding whitespace trimmed."""
    patient = Patient('  P1  ', '  Alex Example  ')

    assert patient.patient_id == 'P1'
    assert patient.name == 'Alex Example'


@pytest.mark.parametrize('bad_id', ['', '   ', None, 101])
def test_blank_or_non_text_patient_id_is_rejected(bad_id) -> None:
    """TEST-02: invalid patient IDs raise ValueError."""
    with pytest.raises(ValueError):
        Patient(bad_id, 'Alex Example')


@pytest.mark.parametrize('bad_name', ['', '   ', None])
def test_blank_or_non_text_patient_name_is_rejected(bad_name) -> None:
    """TEST-03: the patient name is required."""
    with pytest.raises(ValueError):
        Patient('P1', bad_name)


def test_practitioner_stores_trimmed_fields() -> None:
    """TEST-04: valid practitioner fields are stored, trimmed."""
    practitioner = Practitioner(' D1 ', ' Taylor Example ', ' General practice ')

    assert practitioner.practitioner_id == 'D1'
    assert practitioner.name == 'Taylor Example'
    assert practitioner.specialty == 'General practice'


@pytest.mark.parametrize('practitioner_id, name, specialty', [
    ('', 'Taylor Example', 'General practice'),
    ('D1', '   ', 'General practice'),
    ('D1', 'Taylor Example', ''),
])
def test_practitioner_requires_id_name_and_specialty(
    practitioner_id, name, specialty,
) -> None:
    """TEST-05: each required practitioner field is validated."""
    with pytest.raises(ValueError):
        Practitioner(practitioner_id, name, specialty)


def test_patient_id_cannot_be_reassigned() -> None:
    """TEST-06: identity is read-only after construction."""
    patient = Patient('P1', 'Alex Example')

    with pytest.raises(AttributeError):
        patient.patient_id = 'P2'

    assert patient.patient_id == 'P1'


def test_new_appointment_is_scheduled_with_given_participants() -> None:
    """TEST-07: initial status and stored participants and time."""
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General practice')

    appointment = Appointment('A1', patient, practitioner, NINE_AM)

    assert appointment.status is AppointmentStatus.SCHEDULED
    assert appointment.patient is patient
    assert appointment.practitioner is practitioner
    assert appointment.date_time == NINE_AM


def test_cancel_changes_status_to_cancelled() -> None:
    """TEST-08: AC-05.1 at domain level."""
    appointment = make_appointment()

    appointment.cancel()

    assert appointment.status is AppointmentStatus.CANCELLED


def test_repeated_cancel_is_rejected_and_status_kept() -> None:
    """TEST-09: AC-05.3 at domain level."""
    appointment = make_appointment()
    appointment.cancel()

    with pytest.raises(ValueError):
        appointment.cancel()

    assert appointment.status is AppointmentStatus.CANCELLED


def test_completed_appointment_cannot_be_cancelled() -> None:
    """TEST-10: only SCHEDULED may be cancelled (BR-06)."""
    appointment = make_appointment(AppointmentStatus.COMPLETED)

    with pytest.raises(ValueError):
        appointment.cancel()

    assert appointment.status is AppointmentStatus.COMPLETED


def test_appointment_status_cannot_be_set_directly() -> None:
    """TEST-11: status changes only through guarded operations."""
    appointment = make_appointment()

    with pytest.raises(AttributeError):
        appointment.status = AppointmentStatus.CANCELLED

    assert appointment.status is AppointmentStatus.SCHEDULED


@pytest.mark.parametrize('bad_id', ['', '   ', None])
def test_blank_appointment_id_is_rejected(bad_id) -> None:
    """TEST-12: the appointment ID is required."""
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General practice')

    with pytest.raises(ValueError):
        Appointment(bad_id, patient, practitioner, NINE_AM)


def test_appointment_requires_participant_objects() -> None:
    """TEST-13: IDs or the wrong type are not accepted as participants."""
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General practice')

    with pytest.raises(ValueError):
        Appointment('A1', 'P1', practitioner, NINE_AM)
    with pytest.raises(ValueError):
        Appointment('A1', patient, 'D1', NINE_AM)
    with pytest.raises(ValueError):
        Appointment('A1', practitioner, patient, NINE_AM)


@pytest.mark.parametrize('bad_time', [
    datetime(2026, 10, 1, 9, 0, 30),
    datetime(2026, 10, 1, 9, 0, 0, 5),
    datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc),
    '2026-10-01 09:00',
])
def test_appointment_time_must_be_naive_minute_precision(bad_time) -> None:
    """TEST-14: seconds, microseconds, timezone and non-datetime fail."""
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General practice')

    with pytest.raises(ValueError):
        Appointment('A1', patient, practitioner, bad_time)


def test_appointment_status_must_be_an_enum_member() -> None:
    """TEST-15: a plain string is not a valid status."""
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General practice')

    with pytest.raises(ValueError):
        Appointment('A1', patient, practitioner, NINE_AM, 'scheduled')