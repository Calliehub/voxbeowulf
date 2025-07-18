#!/usr/bin/env python3
"""
Test constraints for Beowulf digital models.
Collection of validation rules and data integrity checks.
"""

import json
from numbering import FITT_BOUNDARIES


class BeowulfTestConstraints:
    """Test constraints for validating Beowulf digital text models."""
    
    def __init__(self, json_file="data/fitts/maintext.json"):
        """Initialize with the main text JSON file."""
        with open(json_file, 'r', encoding='utf-8') as f:
            self.lines = json.load(f)
    
    def test_line_numbering_sequential(self):
        """Lines must be numbered sequentially starting from 0."""
        for i, line in enumerate(self.lines):
            expected = i
            actual = line['line']
            assert actual == expected, f"Line {i}: expected {expected}, got {actual}"
        return True
    
    def test_total_line_count(self):
        """Total lines should match expected count (3183 including line 0)."""
        expected_count = 3183
        actual_count = len(self.lines)
        assert actual_count == expected_count, f"Expected {expected_count} lines, got {actual_count}"
        return True
    
    def test_fitt_boundaries_valid(self):
        """Fitt boundaries should be within valid line ranges."""
        max_line = len(self.lines) - 1
        for i, (start, end, name) in enumerate(FITT_BOUNDARIES):
            if i == 24:  # Skip non-existent fitt 24
                continue
            assert 0 <= start <= max_line, f"Fitt {i} start {start} out of range"
            assert 0 <= end <= max_line, f"Fitt {i} end {end} out of range"
            assert start <= end, f"Fitt {i} start {start} > end {end}"
        return True
    
    def test_required_fields_present(self):
        """Each line must have 'line', 'OE', and 'ME' fields."""
        required_fields = {'line', 'OE', 'ME'}
        for i, line_data in enumerate(self.lines):
            missing = required_fields - set(line_data.keys())
            assert not missing, f"Line {i} missing fields: {missing}"
        return True
    
    def test_line_zero_empty(self):
        """Line 0 should have empty OE and ME text."""
        line_0 = self.lines[0]
        assert line_0['line'] == 0, "First entry should be line 0"
        assert line_0['OE'] == "", "Line 0 OE should be empty"
        assert line_0['ME'] == "", "Line 0 ME should be empty"
        return True
    
    def test_famous_opening_line(self):
        """Line 1 should contain the famous 'Hwæt!' opening."""
        line_1 = self.lines[1]
        assert line_1['line'] == 1, "Second entry should be line 1"
        assert 'Hwæt!' in line_1['OE'], "Line 1 should contain 'Hwæt!'"
        assert 'Listen!' in line_1['ME'], "Line 1 translation should contain 'Listen!'"
        return True
    
    def test_no_empty_text_after_line_zero(self):
        """Lines 1+ should not have empty OE or ME text."""
        for line_data in self.lines[1:]:
            line_num = line_data['line']
            assert line_data['OE'].strip(), f"Line {line_num} has empty OE text"
            assert line_data['ME'].strip(), f"Line {line_num} has empty ME text"
        return True
    
    def test_fitt_coverage_complete(self):
        """All lines 1-3182 should be covered by fitt boundaries."""
        covered_lines = set()
        for i, (start, end, name) in enumerate(FITT_BOUNDARIES):
            if i == 24:  # Skip non-existent fitt 24
                continue
            covered_lines.update(range(start, end + 1))
        
        expected_lines = set(range(1, 3183))
        missing = expected_lines - covered_lines
        assert not missing, f"Lines not covered by fitts: {sorted(missing)[:10]}..."
        return True


def run_all_tests():
    """Run all test constraints and report results."""
    constraints = BeowulfTestConstraints()
    tests = [
        'test_line_numbering_sequential',
        'test_total_line_count', 
        'test_fitt_boundaries_valid',
        'test_required_fields_present',
        'test_line_zero_empty',
        'test_famous_opening_line',
        'test_no_empty_text_after_line_zero',
        'test_fitt_coverage_complete'
    ]
    
    results = {}
    for test_name in tests:
        try:
            test_method = getattr(constraints, test_name)
            result = test_method()
            results[test_name] = "PASS"
            print(f"✓ {test_name}")
        except Exception as e:
            results[test_name] = f"FAIL: {e}"
            print(f"✗ {test_name}: {e}")
    
    return results


if __name__ == "__main__":
    run_all_tests()