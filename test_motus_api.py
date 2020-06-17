import pytest
import requests
from datetime import datetime, timezone, timedelta
import motus_api


api_instance = motus_api.SGMotusAPI()


def test_date():
    # This does _not_ test whether or not the date is correct.
    date_format = "%Y%m%d%H%M%S"
    res = api_instance.date()
    # This will raise an exception if the output from the date() function is incorrect.
    _ = datetime.strptime(res, date_format)


time_conversion_test = [
    (
        "2019-07-27 12:05:15 -04:00",
        datetime(
            2019, 7, 27, 12, 5, 15, tzinfo=timezone(timedelta(days=-1, seconds=72000))
        ),
    ),
    ("2019-05-31 00:01:00 +00:00", datetime(2019, 5, 31, 0, 1, 0, tzinfo=timezone.utc)),
]


@pytest.mark.parametrize("test_input, expected_result", time_conversion_test)
def test_api_timestamp_conversion(test_input, expected_result):
    assert api_instance.to_datetime(test_input) == expected_result


def test_sg_receivers():
    """ Test creation of an SGReceiver object. """
    test_data = {
        "receiverID": "SG-5113BBBK0173",
        "motusRecvID": 383,
        "recvProjectID": 1,
        "deviceID": 251,
        "macAddress": "0",
        "receiverType": "SENSORGNOME",
        "dtStart": "2016-11-19 00:00:00 +00:00",
        "deploymentStatus": "active",
        "deploymentName": "Crysler Park Marina",
    }
    res = motus_api.SGReceiver(test_data)
    assert res.receiver_id == "SG-5113BBBK0173"
    assert res.motus_receiver_id == 383
    assert res.project_receiver_id == 1
    assert res.device_id == 251
    assert res.mac_address == "0"
    assert res.receiver_type == "SENSORGNOME"
    assert res.deployment_start == datetime(2016, 11, 19, 0, 0, tzinfo=timezone.utc)
    assert res.deployment_status == "active"
    assert res.deployment_name == "Crysler Park Marina"


def test_sg_projects():
    test_data = {
        "id": 1,
        "name": "Motus Ontario Array",
        "code": "MotusON",
        "tagPermissions": 2,
        "sensorPermissions": 2,
    }
    res = motus_api.SGProject(test_data)
    assert res.project_id == 1
    assert res.name == "Motus Ontario Array"
    assert res.code == "MotusON"
    assert res.permissions_tag == 2
    assert res.permissions_sensor == 2
