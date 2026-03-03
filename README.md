Install dependencies:
python -m pip install -r requirements.txt

Run all tests:
pytest

Run with verbose mode:
pytest -v

Run tests by marker:
pytest -m users

Run for specific environment:
pytest --env=UAT

Run tests by markers for specific environment:
pytest -m users --env=DEV

Run tests in parallel:
pytest -n 9

Run specific tests in parallel using markers:
pytest -n 2 -m albums

Generate HTMl report:
pytest --html=raport_api.html

Logs are written to:
api_framework.log
errors.log
last_run.log

Open the HTML report:
right-click the report_api.html file and select Open in -> Browser -> Chrome