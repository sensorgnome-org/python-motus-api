import json
import requests
from datetime import datetime
from dataclasses import dataclass


class MotusAPIError(Exception):
    """
    Base class for Motus API exceptions.
    """

    pass


class URLLengthError(MotusAPIError):
    """
    Raised when the URL is over 2,000 characters.
    Attributes:
        length: actual length of the url.
    """

    def __init__(self, message):
        self.message = message


class HTTPStatusError(MotusAPIError):
    """ Base class for HTTP related errors. """

    def __init__(self, reason=""):
        self.reason = reason

    def __str__(self):
        return self.reason


class HTTP400Error(HTTPStatusError):
    def __str__(self):
        if not self.reason:
            return "Bad request, parameter missing or invalid."
        else:
            return f"Bad request, {self.reason}."


class HTTP401Error(HTTPStatusError):
    def __str__(self):
        if not self.reason:
            return "API authentication needs to be supplied or is incorrect."
        else:
            return f"Authentication error: {self.reason}."


class HTTP404Error(HTTPStatusError):
    def __str__(self):
        if not self.reason:
            return "API endpoint not found."
        else:
            return f"API endpoint not found: {self.reason}."


class HTTP409Error(HTTPStatusError):
    def __str__(self):
        if not self.reason:
            return "A conflict occurred with the current state of the resource."
        else:
            return f"A conflict occurred: {self.reason}."


class HTTP500Error(HTTPStatusError):
    def __str__(self):
        if not self.reason:
            return "An internal server error occurred."
        else:
            return f"Server error: {self.reason}."


class MotusAPI:
    """
    API for interacting with Motus (motus.org).
    """

    def __init__(self):
        self._base_url = ""
        self.motus_username = ""
        self.motus_password = ""
        self.auth = True if self.motus_password and self.motus_username else False
        self.url_max_length = 2000

    def date(self):
        """
        Returns the current date in the form "YYYYMMDDhhmmss" as needed by the API.
        """
        ds = "%Y%m%d%H%M%S"
        return datetime.strftime(datetime.utcnow(), ds)

    def _get(self, endpoint, request_params={}, api_key="", serial_number=""):
        """
        Do an HTTP GET request.
        Note that as URLs should be under 2000 characters, will raise an exception if the request is longer.
        Args:
            endpoint (str): API endpoint to make the request to. For example, projects.
            request_params (dict, optional): Dictionary to store request parameters. Default: {}.
            api_key (str, optional): API key that certain API calls need. Default: ''.
            serial_number (str, optional): Serial number of the sensorgnome that certain API calls need. Default: ''.
        Returns:
            Python representation of the JSON returned from the API call.
        Raises:
            In error cases, will raise the pertinent exception.
        """
        request_params["date"] = self.date()
        if self.auth:
            request_params["login"] = self.motus_username
            request_params["pword"] = self.motus_password
        if api_key:
            request_params["hash"] = api_key
        if serial_number:
            request_params["serno"] = serial_number
        full_request = f"{self._base_url}{endpoint}/?json={json.dumps(request_params, separators=(',', ':'))}"
        if len(full_request) > self.url_max_length:
            raise URLLengthError(
                f"URL length {len(full_request)} longer than {self.url_max_length}."
            )
        print(full_request)
        res = self.handle_result(requests.get(full_request))
        # print(res)
        return res

    def handle_result(self, result):
        """
        Takes care of raising specific exceptions in a request.
        Args:
            result (requests.request): Result from reguests.get/requets.post
        """
        status_code = result.status_code
        try:
            reason = json.loads(result.content)["errorMsg"]
        except KeyError:
            reason = ""
        if status_code in (200, 201, 202):
            return json.loads(result.content)
        elif status_code == 400:
            raise HTTP401Error(reason)
        elif status_code == 401:
            raise HTTP401Error(reason)
        elif status_code == 404:
            raise HTTP404Error(reason)
        elif status_code == 409:
            raise HTTP409Error(reason)
        elif status_code == 500:
            raise HTTP500Error(reason)
        else:
            raise HTTPStatusError(
                f"Status code: {status_code} received from server unexpectedly."
            )


class SGMotusAPI(MotusAPI):
    """Interaction with Sensorgnome specific APIs"""

    def __init__(self):
        super().__init__()
        self._base_url = "https://sandbox.motus.org/api/"
        self.timestamp_format = "%Y-%m-%d %H:%M:%S %z"

    def to_datetime(self, time_stamp):
        """
        Converts a timestamp to tz aware datetime object.
        """
        return datetime.strptime(time_stamp, self.timestamp_format)

    def list_receivers(self):
        """Gets metadata related to all Motus receivers."""
        endpoint = "receivers"
        result = self._get(endpoint)["data"]
        return SGReceiver(result)

    def list_projects(self):
        endpoint = "projects"
        result = self._get(endpoint)["data"]
        return SGProject(result)


@dataclass(init=False)
class SGReceiver(SGMotusAPI):
    def __init__(self, recv):
        super().__init__()
        self.deployment_name = recv["deploymentName"]
        self.deployment_status = recv["deploymentStatus"]
        self.motus_receiver_id = int(recv["motusRecvID"])
        self.project_receiver_id = int(recv["recvProjectID"])
        self.deployment_start = self.to_datetime(recv["dtStart"])
        self.receiver_type = recv["receiverType"]
        self.receiver_id = recv["receiverID"]
        self.device_id = int(recv["deviceID"])
        self.mac_address = recv["macAddress"]


@dataclass(init=False)
class SGProject(SGMotusAPI):
    def __init__(self, proj):
        super().__init__()
        print(proj)
        self.project_id = int(proj["id"])
        self.name = proj["name"]
        self.code = proj["code"]
        self.permissions_tag = int(proj["tagPermissions"])
        self.permissions_sensor = int(proj["sensorPermissions"])
