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


receiver_test_data = [
    (
        {
            "receiverID": "SG-5113BBBK0173",
            "motusRecvID": 383,
            "recvProjectID": 1,
            "deviceID": 251,
            "macAddress": "0",
            "receiverType": "SENSORGNOME",
            "dtStart": "2016-11-19 00:00:00 +00:00",
            "deploymentStatus": "active",
            "deploymentName": "Crysler Park Marina",
        },
        [
            "SG-5113BBBK0173",
            383,
            1,
            251,
            "0",
            "SENSORGNOME",
            datetime(2016, 11, 19, 0, 0, 0, tzinfo=timezone.utc),
            "active",
            "Crysler Park Marina",
        ],
    ),
    (
        {
            "receiverID": "TEMP16",
            "motusRecvID": 476,
            "recvProjectID": 5,
            "deviceID": None,
            "macAddress": None,
            "receiverType": None,
            "dtStart": "2014-05-29 00:00:00 +00:00",
            "deploymentStatus": "terminated",
            "deploymentName": "Hopewell",
        },
        [
            "TEMP16",
            476,
            5,
            None,
            None,
            None,
            datetime(2014, 5, 29, 0, 0, 0, tzinfo=timezone.utc),
            "terminated",
            "Hopewell",
        ],
    ),
]


@pytest.mark.parametrize("test_input, expected_result", receiver_test_data)
def test_sg_receivers(test_input, expected_result):
    """ Test creation of an SGReceiver object. """

    res = motus_api.SGReceiver(test_input)
    assert res.receiver_id == expected_result[0]
    assert res.motus_receiver_id == expected_result[1]
    assert res.project_receiver_id == expected_result[2]
    assert res.device_id == expected_result[3]
    assert res.mac_address == expected_result[4]
    assert res.receiver_type == expected_result[5]
    assert res.deployment_start == expected_result[6]
    assert res.deployment_status == expected_result[7]
    assert res.deployment_name == expected_result[8]


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
    assert res.permissions_tag == 2
