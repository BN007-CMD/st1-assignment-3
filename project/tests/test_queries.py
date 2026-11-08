import pytest

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)
from smartcare.queries import appointment_sort_key, select_appointments
from datetime import datetime


def make_appointment(apt_id, patient, practitioner, dt, status=AppointmentStatus.SCHEDULED):
    return Appointment(apt_id, patient, practitioner, dt, status)


@pytest.fixture
def p1():
    return Patient('P1', 'Alex Example')


@pytest.fixture
def dr1():
    return Practitioner('DR1', 'Taylor Example', 'General practice')


@pytest.fixture
def dr2():
    return Practitioner('DR2', 'Sam Example', 'Cardiology')


# QRY-01 practitioner isolation + control
def test_qry01_practitioner_isolation(p1, dr1, dr2):
    a1 = make_appointment('A1', p1, dr1, datetime(2026, 10, 1, 9, 0))
    a2 = make_appointment('A2', p1, dr2, datetime(2026, 10, 1, 9, 0))
    source = [a1, a2]
    result = select_appointments(source, 'DR1')
    assert all(a.practitioner.practitioner_id == 'DR1' for a in result)
    assert a1 in result
    assert a2 not in result  # control


# QRY-02 default all statuses
def test_qry02_default_all_statuses(p1, dr1):
    a1 = make_appointment('A1', p1, dr1, datetime(2026, 10, 1, 9, 0))
    a2 = make_appointment('A2', p1, dr1, datetime(2026, 10, 1, 9, 30), AppointmentStatus.CANCELLED)
    a3 = make_appointment('A3', p1, dr1, datetime(2026, 10, 1, 10, 0), AppointmentStatus.COMPLETED)
    result = select_appointments([a1, a2, a3], 'DR1')
    assert {a.status for a in result} == {
        AppointmentStatus.SCHEDULED,
        AppointmentStatus.CANCELLED,
        AppointmentStatus.COMPLETED,
    }


# QRY-02 each explicit status
@pytest.mark.parametrize('status', list(AppointmentStatus))
def test_qry02_each_status_filter(p1, dr1, status):
    a1 = make_appointment('A1', p1, dr1, datetime(2026, 10, 1, 9, 0))
    a2 = make_appointment('A2', p1, dr1, datetime(2026, 10, 1, 9, 30), AppointmentStatus.CANCELLED)
    a3 = make_appointment('A3', p1, dr1, datetime(2026, 10, 1, 10, 0), AppointmentStatus.COMPLETED)
    result = select_appointments([a1, a2, a3], 'DR1', status)
    assert all(a.status is status for a in result)


# QRY-02 no match -> empty list
def test_qry02_no_match_empty(p1, dr1):
    a1 = make_appointment('A1', p1, dr1, datetime(2026, 10, 1, 9, 0))
    result = select_appointments([a1], 'DR1', AppointmentStatus.CANCELLED)
    assert result == []
    assert isinstance(result, list)


# QRY-03 equal-time ID tie-break
def test_qry03_tie_break(p1, dr1):
    a2 = make_appointment('A2', p1, dr1, datetime(2026, 10, 1, 9, 0), AppointmentStatus.CANCELLED)
    a10 = make_appointment('A10', p1, dr1, datetime(2026, 10, 1, 9, 0), AppointmentStatus.COMPLETED)
    result = select_appointments([a2, a10], 'DR1')
    assert [a.appointment_id for a in result] == ['A10', 'A2']  # lexicographic tie-break


# FP-03 named key tested directly
def test_fp03_sort_key_direct(p1, dr1):
    a1 = make_appointment('A1', p1, dr1, datetime(2026, 10, 1, 9, 0))
    before = (a1.appointment_id, a1.date_time, a1.status, a1.patient, a1.practitioner)
    key = appointment_sort_key(a1)
    assert key == (datetime(2026, 10, 1, 9, 0), 'A1')
    assert (a1.appointment_id, a1.date_time, a1.status, a1.patient, a1.practitioner) == before


# FP-02 fresh lists: empty, already-sorted, unsorted
def test_fp02_fresh_lists(p1, dr1):
    empty = []
    assert select_appointments(empty, 'DR1') is not empty

    sorted_src = [
        make_appointment('A1', p1, dr1, datetime(2026, 10, 1, 9, 0)),
        make_appointment('A2', p1, dr1, datetime(2026, 10, 1, 10, 0)),
    ]
    r = select_appointments(sorted_src, 'DR1')
    assert r is not sorted_src
    assert all(a is b for a, b in zip(r, sorted_src))

    unsorted_src = [
        make_appointment('A2', p1, dr1, datetime(2026, 10, 1, 10, 0)),
        make_appointment('A1', p1, dr1, datetime(2026, 10, 1, 9, 0)),
    ]
    r = select_appointments(unsorted_src, 'DR1')
    assert r is not unsorted_src
    assert [a.appointment_id for a in r] == ['A1', 'A2']


# FP-01/FP-02 unchanged source order/fields + repeated calls
def test_fp_repeat_no_mutation(p1, dr1):
    src = [
        make_appointment('A3', p1, dr1, datetime(2026, 10, 1, 11, 0)),
        make_appointment('A1', p1, dr1, datetime(2026, 10, 1, 9, 0)),
        make_appointment('A2', p1, dr1, datetime(2026, 10, 1, 10, 0)),
    ]
    before_ids = [a.appointment_id for a in src]
    before_fields = [
        (a.appointment_id, a.date_time, a.status, a.patient, a.practitioner)
        for a in src
    ]

    first = select_appointments(src, 'DR1')
    second = select_appointments(src, 'DR1')

    assert [a.appointment_id for a in src] == before_ids
    assert [
        (a.appointment_id, a.date_time, a.status, a.patient, a.practitioner)
        for a in src
    ] == before_fields
    assert [a.appointment_id for a in first] == [a.appointment_id for a in second]
