"""Student-authored Stage 6 service tests.

Each test builds a fresh SmartCareDataStore through the fixture below, so
no test depends on another test's state or on execution order. Requirement
and acceptance-criterion IDs refer to SmartCare A3 Requirements Baseline
2026 revision 2.
"""

from datetime import datetime
from types import SimpleNamespace

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


# Blank, whitespace-only and non-text IDs all break the public ID contract.
INVALID_IDS = ['', '   ', None, 101]
NINE_AM = datetime(2026, 10, 1, 9, 0)
TEN_AM = datetime(2026, 10, 1, 10, 0)


@pytest.fixture
def clinic() -> SimpleNamespace:
    """Return one fresh shared store with services, two registered
    synthetic patients and two registered synthetic practitioners.
    """
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)
    alex = patients.register_patient('P1', 'Alex Example')
    sam = patients.register_patient('P2', 'Sam Example')
    taylor = practitioners.register_practitioner(
        'D1',
        'Taylor Example',
        'General practice',
    )
    morgan = practitioners.register_practitioner(
        'D2',
        'Morgan Example',
        'Physiotherapy',
    )
    return SimpleNamespace(
        data_store=data_store,
        patients=patients,
        practitioners=practitioners,
        appointments=appointments,
        alex=alex,
        sam=sam,
        taylor=taylor,
        morgan=morgan,
    )


# FR-02 Patient Search: AC-02.1 known lookup, AC-02.2 unknown lookup,
# plus the revision 2 ID contract (trimmed, non-blank, case-sensitive).

def test_find_patient_returns_the_registered_object(clinic) -> None:
    """AC-02.1: lookup returns the stored object itself, not a copy."""
    found = clinic.patients.find_patient('P1')

    assert found is clinic.alex
    assert found.patient_id == 'P1'
    assert found.name == 'Alex Example'


def test_find_patient_selects_the_requested_record(clinic) -> None:
    """AC-02.1: a second registered patient is not returned for P1."""
    assert clinic.patients.find_patient('P2') is clinic.sam
    assert clinic.patients.find_patient('P1') is not clinic.sam


def test_find_patient_trims_surrounding_whitespace(clinic) -> None:
    """ID contract: surrounding whitespace is trimmed before lookup."""
    assert clinic.patients.find_patient('  P1  ') is clinic.alex


def test_find_patient_is_case_sensitive(clinic) -> None:
    """ID contract: p1 is a different, unregistered ID, so it is absent
    and the failed lookup leaves the stored patients unchanged.
    """
    before = clinic.data_store.list_patients()

    with pytest.raises(LookupError):
        clinic.patients.find_patient('p1')

    assert clinic.data_store.list_patients() == before


def test_unknown_patient_raises_lookup_error(clinic) -> None:
    """AC-02.2: a valid but unregistered ID reports absence."""
    before = clinic.data_store.list_patients()

    with pytest.raises(LookupError, match='Patient not found'):
        clinic.patients.find_patient('P404')

    assert clinic.data_store.list_patients() == before
    assert clinic.data_store.find_patient('P404') is None


@pytest.mark.parametrize('bad_id', INVALID_IDS)
def test_invalid_patient_id_raises_value_error(clinic, bad_id) -> None:
    """ID contract: an invalid ID is a ValueError, distinct from absence."""
    before = clinic.data_store.list_patients()

    with pytest.raises(ValueError):
        clinic.patients.find_patient(bad_id)

    assert clinic.data_store.list_patients() == before


# FR-03 supporting operation: practitioner lookup over registered
# practitioners, using the same LookupError/ValueError contract.

def test_find_practitioner_returns_the_registered_object(clinic) -> None:
    """Lookup returns the stored practitioner with its registered fields."""
    found = clinic.practitioners.find_practitioner('D1')

    assert found is clinic.taylor
    assert found.name == 'Taylor Example'
    assert found.specialty == 'General practice'
    assert clinic.practitioners.find_practitioner('D2') is clinic.morgan


def test_find_practitioner_trims_surrounding_whitespace(clinic) -> None:
    """ID contract: surrounding whitespace is trimmed before lookup."""
    assert clinic.practitioners.find_practitioner(' D1 ') is clinic.taylor


def test_find_practitioner_is_case_sensitive(clinic) -> None:
    """ID contract: d1 is a different, unregistered ID, so it is absent
    and the failed lookup leaves the stored practitioners unchanged.
    """
    before = clinic.data_store.list_practitioners()

    with pytest.raises(LookupError):
        clinic.practitioners.find_practitioner('d1')

    assert clinic.data_store.list_practitioners() == before


def test_unknown_practitioner_raises_lookup_error(clinic) -> None:
    """A valid but unregistered practitioner ID reports absence."""
    before = clinic.data_store.list_practitioners()

    with pytest.raises(LookupError, match='Practitioner not found'):
        clinic.practitioners.find_practitioner('D404')

    assert clinic.data_store.list_practitioners() == before


def test_patient_id_is_not_found_as_a_practitioner(clinic) -> None:
    """BR-01/02: IDs are unique per entity type, so P1 is not a
    practitioner even though a patient P1 exists.
    """
    with pytest.raises(LookupError):
        clinic.practitioners.find_practitioner('P1')


@pytest.mark.parametrize('bad_id', INVALID_IDS)
def test_invalid_practitioner_id_raises_value_error(clinic, bad_id) -> None:
    """ID contract: an invalid ID is a ValueError, distinct from absence."""
    before = clinic.data_store.list_practitioners()

    with pytest.raises(ValueError):
        clinic.practitioners.find_practitioner(bad_id)

    assert clinic.data_store.list_practitioners() == before


# FR-06 cancel only SCHEDULED; FR-07 retain the same object as history.
# AC-05.1 status change, AC-05.2 retained history, AC-05.3 repeat rejected.

def test_cancel_returns_same_object_with_cancelled_status(clinic) -> None:
    """AC-05.1: cancelling a SCHEDULED appointment changes its status and
    returns the stored object rather than a replacement.
    """
    booked = clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)

    cancelled = clinic.appointments.cancel_appointment('A1')

    assert cancelled is booked
    assert cancelled.status is AppointmentStatus.CANCELLED


def test_cancelled_appointment_is_retained_as_history(clinic) -> None:
    """AC-05.2 / FR-07: the cancelled appointment is still found and listed
    as the same object, with its participants and time unchanged.
    """
    booked = clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)

    clinic.appointments.cancel_appointment('A1')

    assert clinic.appointments.find_appointment('A1') is booked
    assert clinic.data_store.find_appointment('A1') is booked
    assert clinic.data_store.list_appointments() == [booked]
    assert booked.patient is clinic.alex
    assert booked.practitioner is clinic.taylor
    assert booked.date_time == NINE_AM


def test_cancel_accepts_a_trimmed_appointment_id(clinic) -> None:
    """ID contract: surrounding whitespace identifies the same appointment."""
    booked = clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)

    assert clinic.appointments.cancel_appointment('  A1 ') is booked
    assert booked.status is AppointmentStatus.CANCELLED


def test_repeated_cancellation_is_rejected_without_change(clinic) -> None:
    """AC-05.3: a second cancellation raises ValueError; the appointment
    stays CANCELLED and retained.
    """
    booked = clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)
    clinic.appointments.cancel_appointment('A1')

    with pytest.raises(ValueError):
        clinic.appointments.cancel_appointment('A1')

    assert booked.status is AppointmentStatus.CANCELLED
    assert clinic.appointments.find_appointment('A1') is booked


def test_completed_appointment_cannot_be_cancelled(clinic) -> None:
    """FR-06 / BR-06: only SCHEDULED may be cancelled. COMPLETED is a
    supported test fixture state (BR-08), stored with registered objects.
    """
    completed = Appointment(
        'A9',
        clinic.alex,
        clinic.taylor,
        NINE_AM,
        AppointmentStatus.COMPLETED,
    )
    clinic.data_store.add_appointment(completed)

    with pytest.raises(ValueError):
        clinic.appointments.cancel_appointment('A9')

    assert completed.status is AppointmentStatus.COMPLETED
    assert clinic.appointments.find_appointment('A9') is completed


def test_cancel_unknown_appointment_raises_lookup_error(clinic) -> None:
    """A valid unknown ID raises LookupError and leaves existing
    appointments untouched.
    """
    booked = clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)

    with pytest.raises(LookupError, match='Appointment not found'):
        clinic.appointments.cancel_appointment('A404')

    assert booked.status is AppointmentStatus.SCHEDULED
    assert clinic.data_store.list_appointments() == [booked]


@pytest.mark.parametrize('bad_id', INVALID_IDS)
def test_cancel_with_invalid_id_raises_value_error(clinic, bad_id) -> None:
    """ID contract: an invalid ID raises ValueError, not LookupError, and
    nothing changes.
    """
    booked = clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)

    with pytest.raises(ValueError):
        clinic.appointments.cancel_appointment(bad_id)

    assert booked.status is AppointmentStatus.SCHEDULED
    assert clinic.data_store.list_appointments() == [booked]


def test_cancel_changes_only_the_requested_appointment(clinic) -> None:
    """FR-06: cancelling A1 must not alter another stored appointment."""
    first = clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)
    second = clinic.appointments.book_appointment('A2', 'P2', 'D1', TEN_AM)

    clinic.appointments.cancel_appointment('A1')

    assert first.status is AppointmentStatus.CANCELLED
    assert second.status is AppointmentStatus.SCHEDULED
    assert clinic.data_store.list_appointments() == [first, second]


def test_cancelled_slot_can_be_booked_again(clinic) -> None:
    """FR-05 / BR-05 still hold after cancellation: only a SCHEDULED
    appointment occupies a practitioner's time, and the cancelled record
    is kept alongside the new booking.
    """
    original = clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)
    clinic.appointments.cancel_appointment('A1')

    rebooked = clinic.appointments.book_appointment('A2', 'P2', 'D1', NINE_AM)

    assert rebooked.status is AppointmentStatus.SCHEDULED
    assert original.status is AppointmentStatus.CANCELLED
    assert clinic.data_store.list_appointments() == [original, rebooked]
