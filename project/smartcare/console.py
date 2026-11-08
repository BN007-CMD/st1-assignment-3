"""Console helpers and a small runnable starting demonstration."""


import re
from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def parse_date_time(text: str) -> datetime:
    """Parse YYYY-MM-DD HH:MM; raise ValueError for invalid input."""
    if (
        not isinstance(text, str)
        or re.fullmatch(
            '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}', text
        ) is None
    ):
        raise ValueError('Use date/time format YYYY-MM-DD HH:MM')
    try:
        return datetime.strptime(text, '%Y-%m-%d %H:%M')
    except ValueError:
        raise ValueError(
            'Invalid calendar date/time; use YYYY-MM-DD HH:MM',
        ) from None


def format_appointment(appointment: Appointment) -> str:
    """Return readable synthetic appointment details without changing
    state.
    """
    return (
        f'{appointment.appointment_id}: '
        f'{appointment.patient.patient_id} with '
        f'{appointment.practitioner.practitioner_id}, '
        f'{appointment.date_time:%Y-%m-%d %H:%M}, {appointment.status.value}'
    )


def run_demo() -> None:
    """Demonstrate supplied registration and booking using synthetic
    records.
    """
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)
    patients.register_patient('P1', 'Alex Example')
    practitioners.register_practitioner(
        'DR1',
        'Taylor Example',
        'General practice',
    )
    try:
        appointments.book_appointment(
            'A1',
            'P1',
            'DR1',
            parse_date_time('2026-10-01 09:00'),
        )
        print(format_appointment(appointments.find_appointment('A1')))
    except (ValueError, LookupError) as error:
        print(f'Error: {error}')
    print('Session-only data: records are lost on exit.')


def run_menu() -> None:
    """Stage 9: implement the register/find/book/cancel/list/exit menu.

    Call services, recover from expected input errors, and keep this
    session's data until exit. main.py reports the incomplete menu
    without crashing.
    """
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)

    status_map = {
        '': None,
        'scheduled': AppointmentStatus.SCHEDULED,
        'cancelled': AppointmentStatus.CANCELLED,
        'completed': AppointmentStatus.COMPLETED,
    }

    while True:
        print(
            '\n1 Register patient  2 Find patient\n'
            '3 Register practitioner  4 Find practitioner\n'
            '5 Book appointment  6 Cancel appointment\n'
            '7 Find appointment  8 List practitioner appointments\n'
            '0 Exit'
        )
        choice = input('Choice: ').strip()

        try:
            if choice == '1':
                pid = input('Patient ID: ')
                name = input('Name: ')
                patients.register_patient(pid, name)
                print('Patient registered.')
            elif choice == '2':
                pid = input('Patient ID: ')
                p = patients.find_patient(pid)
                print(f'{p.patient_id}: {p.name}')
            elif choice == '3':
                prid = input('Practitioner ID: ')
                name = input('Name: ')
                spec = input('Specialty: ')
                practitioners.register_practitioner(prid, name, spec)
                print('Practitioner registered.')
            elif choice == '4':
                prid = input('Practitioner ID: ')
                p = practitioners.find_practitioner(prid)
                print(f'{p.practitioner_id}: {p.name}, {p.specialty}')
            elif choice == '5':
                aid = input('Appointment ID: ')
                pid = input('Patient ID: ')
                prid = input('Practitioner ID: ')
                dt = parse_date_time(input('Date/time (YYYY-MM-DD HH:MM): '))
                appointments.book_appointment(aid, pid, prid, dt)
                print('Appointment booked.')
            elif choice == '6':
                aid = input('Appointment ID: ')
                appointments.cancel_appointment(aid)
                print('Appointment cancelled.')
            elif choice == '7':
                aid = input('Appointment ID: ')
                print(format_appointment(appointments.find_appointment(aid)))
            elif choice == '8':
                prid = input('Practitioner ID: ')
                status_text = input(
                    'Status (blank=all, scheduled/cancelled/completed): '
                ).strip().lower()
                if status_text not in status_map:
                    raise ValueError('Status must be blank, scheduled, cancelled or completed')
                status = status_map[status_text]
                results = appointments.list_practitioner_appointments(prid, status)
                if not results:
                    print('No appointments found.')
                for a in results:
                    print(format_appointment(a))
            elif choice == '0':
                print('Session data discarded.')
                return
            else:
                print('Unknown choice; enter 0-8.')
        except (ValueError, LookupError) as error:
            print(f'Error: {error}')
