#!/usr/bin/env python3
"""
Test constraints for Beowulf digital models.

Collection of validation rules and data integrity checks for ensuring
the quality and consistency of Beowulf text data.
"""

import json
import pytest
from typing import Dict, List, Optional, Self, TypedDict

from numbering import FITT_BOUNDARIES


@pytest.fixture
def beowulf_data():
    """Load Beowulf text data for testing."""
    with open("data/fitts/maintext.json", 'r', encoding='utf-8') as f:
        return json.load(f)


def test_line_numbering_sequential(beowulf_data):
    """Line numbers should be sequential starting from 0."""
    for i, line_data in enumerate(beowulf_data):
        assert line_data['line'] == i, f"Line {i} has wrong number: {line_data['line']}"


def test_total_line_count(beowulf_data):
    """Total line count should match expected value."""
    expected_count = 3183
    actual_count = len(beowulf_data)
    assert actual_count == expected_count, f"Expected {expected_count} lines, got {actual_count}"


def test_fitt_boundaries_valid(beowulf_data):
    """Fitt boundaries should be within valid line ranges."""
    max_line = len(beowulf_data) - 1
    for i, (start, end, name) in enumerate(FITT_BOUNDARIES):
        if i == 24:  # Skip non-existent fitt 24
            continue
        assert 0 <= start <= max_line, f"Fitt {i} start {start} out of range"
        assert 0 <= end <= max_line, f"Fitt {i} end {end} out of range"
        assert start <= end, f"Fitt {i} start {start} > end {end}"


def test_required_fields_present(beowulf_data):
    """Each line must have 'line', 'OE', and 'ME' fields."""
    required_fields = {'line', 'OE', 'ME'}
    for i, line_data in enumerate(beowulf_data):
        missing = required_fields - set(line_data.keys())
        assert not missing, f"Line {i} missing fields: {missing}"


def test_line_zero_empty(beowulf_data):
    """Line 0 should have empty OE and ME text."""
    line_0 = beowulf_data[0]
    assert line_0['line'] == 0, "First entry should be line 0"
    assert line_0['OE'] == "", "Line 0 OE text should be empty"
    assert line_0['ME'] == "", "Line 0 ME text should be empty"


def test_famous_opening_line(beowulf_data):
    """Line 1 should contain the famous 'Hwæt!' opening."""
    line_1 = beowulf_data[1]
    assert line_1['line'] == 1, "Second entry should be line 1"
    assert 'Hwæt!' in line_1['OE'], "Line 1 should contain 'Hwæt!'"
    assert 'Listen!' in line_1['ME'], "Line 1 translation should contain 'Listen!'"


def test_no_empty_text_after_line_zero(beowulf_data):
    """Lines 1+ should not have empty OE or ME text."""
    for line_data in beowulf_data[1:]:
        line_num = line_data['line']
        assert line_data['OE'].strip(), f"Line {line_num} has empty OE text"
        assert line_data['ME'].strip(), f"Line {line_num} has empty ME text"


def test_fitt_coverage_complete(beowulf_data):
    """All lines 1-3182 should be covered by fitt boundaries."""
    covered_lines = set()
    for i, (start, end, name) in enumerate(FITT_BOUNDARIES):
        if i == 24:  # Skip non-existent fitt 24
            continue
        covered_lines.update(range(start, end + 1))
    
    expected_lines = set(range(1, 3183))
    missing = expected_lines - covered_lines
    assert not missing, f"Lines not covered by fitts: {sorted(missing)[:10]}..."
