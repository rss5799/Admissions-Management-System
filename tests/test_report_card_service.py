import pytest
from app.services.report_card_service import ReportCardService
import random

def test_report_card_service_load_matrix():
    reportCardService =  ReportCardService
    matrix = reportCardService._load_matrix(reportCardService)
    assert matrix is not None

def test_report_card_service_safe_int():
    reportCardService = ReportCardService
    input = random.randint(1, 100)
    value = reportCardService._safe_int(reportCardService, str(input))
    assert value is not None


def test_initialize_report_card_service():
    reportCardService = ReportCardService
    assert reportCardService.__init__ is not None