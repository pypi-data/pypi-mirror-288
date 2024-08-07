import pytest
from nemo_library import NemoLibrary
from datetime import datetime


def test_getProjectList():
    nl = NemoLibrary()
    df = nl.getProjectList()
    print(df)
    assert len(df) > 0
    first_row = df.iloc[0]
    assert first_row["id"] == "00000000-0000-0000-0000-000000000001"


def test_getProjectID():
    nl = NemoLibrary()
    assert (
        nl.getProjectID("Business Processes") == "00000000-0000-0000-0000-000000000001"
    )


def test_getProjectProperty():
    nl = NemoLibrary()
    val = nl.getProjectProperty(
        projectname="Business Processes", propertyname="ExpDateFrom"
    )

    assert val is not None, "API call did not return any value"

    try:
        date_val = datetime.strptime(val, "%Y-%m-%d")
    except ValueError:
        pytest.fail(f"Returned value ({val}) is not in the format YYYY-MM-DD")

    assert (
        2000 <= date_val.year <= 2100
    ), "Year is out of the acceptable range (2000-2100)"


def test_ReUploadFile():
    nl = NemoLibrary()

    IC_PROJECT_NAME = "Intercompany pA --> hit"
    nl.ReUploadFile(
        projectname=IC_PROJECT_NAME,
        filename="./tests/intercompany_NEMO.csv",
    )

    val = nl.getProjectProperty(
        projectname=IC_PROJECT_NAME, propertyname="ExpNumberOfRecords"
    )
    assert int(val) == 34957, "number of records do not match"


def test_LoadReport():
    nl = NemoLibrary()
    df = nl.LoadReport(
        projectname="21 CRM",
        report_guid="66b6e2f5-d3f5-40fa-98e3-b4e7097b5c4d",
    )

    assert len(df) == 13
