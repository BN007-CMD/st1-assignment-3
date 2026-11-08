"""Stage 8 regression tests for the two prepared defects.

Each test builds its own fresh SmartCareDataStore with synthetic data, so
it does not depend on other tests or on execution order. Requirement IDs
refer to SmartCare A3 Requirements Baseline 2026 revision 2.
"""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


NINE_AM = datetime(2026, 10, 1, 9, 0)


@pytest.fixture
def store_and_appointments():
    """Return a fresh store and appointment service with P1, P2, D1, D2."""
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    patients.register_patient('P1', 'Alex Example')
    patients.register_patient('P2', 'Sam Example')
    practitioners.register_practitioner('D1', 'Taylor Example', 'General')
    practitioners.register_practitioner('D2', 'Morgan Example', 'Physio')
    return data_store, AppointmentService(data_store)


def test_f8_01_conflict_is_per_practitioner_at_exact_time(
    store_and_appointments,
) -> None:
    """F8-01, FR-05: AC-04.1 rejects the same practitioner at the same
    time and leaves the store unchanged; AC-04.2 allows a different
    practitioner at that time.
    """
    data_store, appointments = store_and_appointments
    first = appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)

    with pytest.raises(ValueError):
        appointments.book_appointment('A2', 'P2', 'D1', NINE_AM)

    assert data_store.list_appointments() == [first]
    assert data_store.find_appointment('A2') is None
    assert first.status is AppointmentStatus.SCHEDULED

    other = appointments.book_appointment('A3', 'P2', 'D2', NINE_AM)

    assert data_store.list_appointments() == [first, other]
    assert other.status is AppointmentStatus.SCHEDULED


def test_f8_02_cancelled_appointment_is_still_found(
    store_and_appointments,
) -> None:
    """F8-02, FR-06/07, BR-07, AC-05.2/05.3: a cancelled appointment is
    retained, found by the store and the service as the same object, and
    a repeated cancellation is rejected without change.
    """
    data_store, appointments = store_and_appointments
    booked = appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)

    appointments.cancel_appointment('A1')

    assert booked.status is AppointmentStatus.CANCELLED
    assert data_store.list_appointments() == [booked]
    assert data_store.find_appointment('A1') is booked
    assert appointments.find_appointment('A1') is booked

    with pytest.raises(ValueError):
        appointments.cancel_appointment('A1')

    assert booked.status is AppointmentStatus.CANCELLED
    assert data_store.list_appointments() == [booked]
