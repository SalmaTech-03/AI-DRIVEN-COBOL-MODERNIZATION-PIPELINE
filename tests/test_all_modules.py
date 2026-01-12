import pytest
from src.cobol_parser import COBOLParser
from src.data_cleaner import DataCleaner

def test_parser_logic():
    parser = COBOLParser()
    sample = "       PROGRAM-ID. TEST-PROG."
    result = parser.parse(sample)
    assert result.name == "TEST-PROG"

def test_cleaner_comments():
    cleaner = DataCleaner()
    sample = "      * THIS IS A COMMENT\n       DISPLAY 'HELLO'."
    result = cleaner.clean(sample)
    assert "COMMENT" not in result

def test_complexity_calculation():
    parser = COBOLParser()
    # A program with an IF statement should have logic points
    sample = "       IF X = Y PERFORM Z."
    result = parser.parse(sample)
    assert result.logic_points > 0