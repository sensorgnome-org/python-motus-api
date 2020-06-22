
# python-motus-api

Python library implementing the Motus API, currently a work in progress for Sensorgnome use. Currently a work in progress, with only the basic API endpoints needed to support the Sensorgnome-Server implemented.

## Installation

Install the requirements using `pipenv install`. To develop the library, use `pipenv install --dev`.

## Tests

Tests use pytest and can be run with `python -m pytest` if development depen

## Usage

As noted, this library is at present incomplete and only covers the functions used by the Sensorgnome Server.

Create a `SGMotusAPI` object, setting the `motus_password` and `motus_username` properties if authentication needs to be used. \
**Note**: Presently, this is pointed at sandbox.motus.org during testing.

The following are the currently supported endpoints:

### Motus.org

- `/api/receivers/`: Returns a list of SGReceiver objects representing all Motus receivers.
  - Called with `list_receivers()`.
- `/api/projects/`: Returns a list of SGProject objects representint all Motus Projects.
  - Called with `list_projects()`.
