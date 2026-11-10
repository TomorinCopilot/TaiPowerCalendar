#!/usr/bin/env python3
"""Validate annual CSV files and build the static calendar API."""
import csv
import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'source'
OUTPUT = ROOT / 'docs' / 'data'
TYPES = {'weekday', 'saturday', 'sunday_holiday'}


def build(path):
    if len(path.stem) != 4 or not path.stem.isascii() or not path.stem.isdigit():
        raise ValueError(f'Invalid year filename: {path.name}')
    year = int(path.stem)
    with path.open(encoding='utf-8-sig', newline='') as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != ['date', 'day_type']:
            raise ValueError(f'{path}: expected date,day_type headers')
        rows = list(reader)
    expected = dt.date(year, 1, 1)
    for row in rows:
        if set(row) != {'date', 'day_type'} or row['day_type'] not in TYPES:
            raise ValueError(f'{path}: invalid row: {row}')
        try:
            date = dt.date.fromisoformat(row['date'])
        except (ValueError, TypeError) as error:
            raise ValueError(f'{path}: invalid date: {row["date"]}') from error
        if row['date'] != date.isoformat() or date != expected:
            raise ValueError(f'{path}: expected {expected}, got {row["date"]}')
        expected += dt.timedelta(days=1)
    if expected != dt.date(year + 1, 1, 1):
        raise ValueError(f'{path}: missing or extra dates')
    return year, rows


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    files = sorted(SOURCE.glob('*.csv'))
    if not files:
        raise ValueError('No CSV files found')
    calendars = [build(path) for path in files]
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for year, rows in calendars:
        write_json(OUTPUT / f'{year}.json', rows)
    write_json(OUTPUT / 'years.json', [year for year, _ in calendars])
    print(f'Validated and built {len(calendars)} years: {", ".join(str(y) for y, _ in calendars)}')


if __name__ == '__main__':
    main()
