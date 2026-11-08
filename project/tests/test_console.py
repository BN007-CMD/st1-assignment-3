# tests/test_console.py
import builtins
import pytest
from datetime import datetime

from smartcare import console

def test_parse_date_time_valid():
    assert console.parse_date_time('2026-10-01 09:00') == datetime(2026, 10, 1, 9, 0)


@pytest.mark.parametrize('bad', [
    '2026-10-01',            # missing time
    '2026-10-01 9:00',       # not two-digit hour
    '2026-13-01 09:00',      # impossible month
    '2026-02-30 09:00',      # impossible day
    'not a date',
    '',
    None,
])
def test_parse_date_time_invalid(bad):
    with pytest.raises(ValueError):
        console.parse_date_time(bad)

def run_menu_with(monkeypatch, capsys, inputs):
    """Feed inputs to run_menu and return captured stdout."""
    it = iter(inputs)
    monkeypatch.setattr(builtins, 'input', lambda prompt='': next(it))
    console.run_menu()
    return capsys.readouterr().out


def test_run_menu_register_book_list_exit(monkeypatch, capsys):
    out = run_menu_with(monkeypatch, capsys, [
        '1', 'P1', 'Alex Example',
        '3', 'D1', 'Taylor Example', 'General practice',
        '5', 'A1', 'P1', 'D1', '2026-10-01 09:00',
        '8', 'D1', '',
        '0',
    ])
    assert 'Patient registered.' in out
    assert 'Practitioner registered.' in out
    assert 'Appointment booked.' in out
    assert 'A1:' in out and 'scheduled' in out   # listing shows it
    assert 'Session data discarded.' in out


def test_run_menu_unknown_choice_recovers(monkeypatch, capsys):
    out = run_menu_with(monkeypatch, capsys, ['9', '0'])
    assert 'Unknown choice' in out
    assert 'Session data discarded.' in out      # menu continued to exit


def test_run_menu_blank_id_recovers(monkeypatch, capsys):
    out = run_menu_with(monkeypatch, capsys, [
        '2', '',          # find with blank ID -> ValueError caught
        '0',
    ])
    assert 'Error:' in out
    assert 'Session data discarded.' in out


def test_run_menu_rejected_booking_then_success(monkeypatch, capsys):
    out = run_menu_with(monkeypatch, capsys, [
        '1', 'P1', 'Alex Example',
        '3', 'D1', 'Taylor Example', 'General practice',
        '5', 'A1', 'P1', 'D1', '2026-10-01 09:00',
        '5', 'A2', 'P1', 'D1', '2026-10-01 09:00',   # conflict -> rejected
        '7', 'A2',                                     # still absent
        '0',
    ])
    assert 'Error:' in out                         # conflict message
    assert 'Appointment not found' in out          # A2 was not stored
    assert 'Session data discarded.' in out


def test_run_menu_invalid_status_recovers(monkeypatch, capsys):
    out = run_menu_with(monkeypatch, capsys, [
        '3', 'D1', 'Taylor Example', 'General practice',
        '8', 'D1', 'badstatus',      # invalid status -> ValueError
        '8', 'D1', '',               # blank status still works
        '0',
    ])
    assert 'Status must be blank' in out
    assert 'No appointments found.' in out