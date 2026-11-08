import pytest
from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


@pytest.fixture
def services():
    store = SmartCareDataStore()
    return (
        PatientService(store),
        PractitionerService(store),
        AppointmentService(store),
    )


@pytest.fixture
def booked(services):
    patients, practitioners, appointments = services
    patients.register_patient('P1', 'Alex Example')
    practitioners.register_practitioner('DR1', 'Taylor Example', 'General practice')
    practitioners.register_practitioner('DR2', 'Sam Example', 'Cardiology')
    a1 = appointments.book_appointment('A1', 'P1', 'DR1', datetime(2026, 10, 1, 9, 0))
    a2 = appointments.book_appointment('A2', 'P1', 'DR2', datetime(2026, 10, 1, 9, 0))
    return appointments, a1, a2


# QRY-04 known practitioner, no matches -> empty list
def test_qry04_known_empty(services):
    patients, practitioners, appointments = services
    patients.register_patient('P1', 'Alex Example')
    practitioners.register_practitioner('DR1', 'Taylor Example', 'General practice')
    assert appointments.list_practitioner_appointments('DR1') == []


# QRY-04 valid unknown practitioner -> LookupError
def test_qry04_unknown(services):
    _, _, appointments = services
    with pytest.raises(LookupError):
        appointments.list_practitioner_appointments('DR9')


# QRY-04 blank/invalid ID -> ValueError
@pytest.mark.parametrize('bad_id', ['', '   ', None, 123])
def test_qry04_invalid_id(services, bad_id):
    _, _, appointments = services
    with pytest.raises(ValueError):
        appointments.list_practitioner_appointments(bad_id)


# QRY-04 non-enum status -> ValueError (not treated as no matches)
def test_qry04_non_enum_status(booked):
    appointments, _, _ = booked
    with pytest.raises(ValueError):
        appointments.list_practitioner_appointments('DR1', 'scheduled')


# QRY-01 practitioner isolation via service
def test_qry01_service_isolation(booked):
    appointments, a1, a2 = booked
    result = appointments.list_practitioner_appointments('DR1')
    assert a1 in result
    assert a2 not in result


# QRY-02 default all statuses via service
def test_qry02_service_default_all(booked):
    appointments, a1, a2 = booked
    appointments.cancel_appointment('A1')
    result = appointments.list_practitioner_appointments('DR1')
    assert a1 in result
    assert a1.status is AppointmentStatus.CANCELLED


# Whitespace: registered ID with surrounding spaces still works
def test_service_uses_registered_id(services):
    patients, practitioners, appointments = services
    patients.register_patient('P1', 'Alex Example')
    practitioners.register_practitioner('DR1', 'Taylor Example', 'General practice')
    appointments.book_appointment('A1', 'P1', 'DR1', datetime(2026, 10, 1, 9, 0))
    result = appointments.list_practitioner_appointments('  DR1  ')
    assert len(result) == 1


# AC-05.2 / FR-07 retained history via service
def test_cancel_retained_history(booked):
    appointments, a1, _ = booked
    cancelled = appointments.cancel_appointment('A1')
    assert cancelled is a1
    assert cancelled.status is AppointmentStatus.CANCELLED
    assert appointments.find_appointment('A1') is a1
    all_status = appointments.list_practitioner_appointments('DR1')
    assert a1 in all_status
    scheduled_only = appointments.list_practitioner_appointments(
        'DR1', AppointmentStatus.SCHEDULED
    )
    assert a1 not in scheduled_only




# Integrated sequence covering booking, conflict, different practitioner,
# cancel, retrieve, listing, freed slot
def test_ui01_sequence(services):
    patients, practitioners, appointments = services
    patients.register_patient('P1', 'Alex Example')
    practitioners.register_practitioner('D1', 'Taylor Example', 'General practice')
    practitioners.register_practitioner('D2', 'Sam Example', 'Cardiology')

    a1 = appointments.book_appointment('A1', 'P1', 'D1', datetime(2026, 10, 1, 9, 0))
    assert a1.status is AppointmentStatus.SCHEDULED

    with pytest.raises(ValueError):
        appointments.book_appointment('A2', 'P1', 'D1', datetime(2026, 10, 1, 9, 0))
    assert appointments.data_store.find_appointment('A2') is None  # not reserved

    a2 = appointments.book_appointment('A2', 'P1', 'D2', datetime(2026, 10, 1, 9, 0))
    assert a2.status is AppointmentStatus.SCHEDULED  # different practitioner allowed

    cancelled = appointments.cancel_appointment('A1')
    assert cancelled is a1
    assert cancelled.status is AppointmentStatus.CANCELLED
    assert appointments.find_appointment('A1') is a1

    all_d1 = appointments.list_practitioner_appointments('D1')
    assert a1 in all_d1
    sched_d1 = appointments.list_practitioner_appointments('D1', AppointmentStatus.SCHEDULED)
    assert a1 not in sched_d1

    a3 = appointments.book_appointment('A3', 'P1', 'D1', datetime(2026, 10, 1, 9, 0))
    assert a3.status is AppointmentStatus.SCHEDULED  # freed slot reused


# Rejection leaves no partial state
def test_rejection_no_partial_state(services):
    patients, practitioners, appointments = services
    patients.register_patient('P1', 'Alex Example')
    practitioners.register_practitioner('D1', 'Taylor Example', 'General practice')
    appointments.book_appointment('A1', 'P1', 'D1', datetime(2026, 10, 1, 9, 0))

    # legitimate state change happens BEFORE the snapshot
    appointments.cancel_appointment('A1')

    def snapshot():
        return [
            (a.appointment_id, a.date_time, a.status, a.patient, a.practitioner)
            for a in appointments.data_store.list_appointments()
        ]

    before = snapshot()

    # only failed operations from here on
    with pytest.raises(ValueError):        # duplicate ID, free time
        appointments.book_appointment('A1', 'P1', 'D1', datetime(2026, 10, 1, 10, 0))
    with pytest.raises(LookupError):       # unknown patient
        appointments.book_appointment('A9', 'P9', 'D1', datetime(2026, 10, 1, 10, 0))
    with pytest.raises(ValueError):        # repeat cancel (already CANCELLED)
        appointments.cancel_appointment('A1')
    with pytest.raises(ValueError):        # blank practitioner ID on listing
        appointments.list_practitioner_appointments('')
    with pytest.raises(ValueError):        # non-enum status
        appointments.list_practitioner_appointments('D1', 'scheduled')

    after = snapshot()

    assert after == before
    assert appointments.data_store.find_appointment('A9') is None
    assert len(appointments.data_store.list_appointments()) == 1