import pytest
import mock
from app.google_sheets import Google_Sheets


@pytest.fixture
def googlesheet_information():
    si = {
        "sheet_id": '1234',
        "range_start": 'A1',
        "range_end": 'A5'
    }
    return si


@pytest.fixture
def googlesheet_init(googlesheet_information):
    gsi = googlesheet_information
    google_sheet = Google_Sheets(
        gsi['sheet_id'], gsi['range_start'], gsi['range_end'])
    return google_sheet


def test_connectToSheets(googlesheet_init):

    mock.patch('googleapiclient.discovery.build', autospec=True)

    gs = googlesheet_init
    assert gs is not None
