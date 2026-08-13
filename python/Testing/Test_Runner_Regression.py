# Regression tests for the Test_Here_Maps.py runner
#
# The runner is executed end to end against a stubbed `requests` module, so
# these tests need no HERE Maps / TollGuru API keys and make no network calls:
#
#     cd python && python Testing/Test_Runner_Regression.py

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from csv import reader
from pathlib import Path

TESTING_DIR = Path(__file__).resolve().parent

# Addresses taken from testCases.csv: the second case is made to fail geocoding
# and the third one is made to come back without tolls
UNGEOCODABLE = "Burlington"
TOLL_FREE = "Oklahoma City"

# Stand-in for the `requests` package. Geocoding, routing and toll responses are
# canned, so every branch of the runner can be exercised offline.
REQUESTS_STUB = '''
UNGEOCODABLE = "{ungeocodable}"
TOLL_FREE = "{toll_free}"

# A HERE flexible polyline for three points along the route
FLEX_POLYLINE = "BF4n7zHv24qOoqwBwogBglkDwkiG"

_state = {{"toll_free": False}}


class _Response:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code
        self.text = str(payload)

    def json(self):
        return self._payload


def get(url, params=None, **kwargs):
    if "geocode" in url:
        query = ((params or {{}}).get("q") or "") + url
        if UNGEOCODABLE in query:
            return _Response({{"items": []}})
        if TOLL_FREE in query:
            _state["toll_free"] = True
        return _Response({{"items": [{{"position": {{"lat": 39.9526, "lng": -75.1652}}}}]}})

    return _Response({{
        "routes": [{{
            "sections": [{{
                "polyline": FLEX_POLYLINE,
                "departure": {{"time": "2026-01-05T09:46:08+00:00"}},
                "actions": [
                    {{"offset": 0, "duration": 60}},
                    {{"offset": 1, "duration": 120}},
                ],
            }}]
        }}]
    }})


def post(url, json=None, headers=None, **kwargs):
    toll_free = _state["toll_free"]
    _state["toll_free"] = False
    if toll_free:
        return _Response({{"route": {{"costs": {{}}}}}})
    return _Response({{"route": {{"costs": {{"tag": 1.25, "cash": 2.5}}}}}})
'''.format(ungeocodable=UNGEOCODABLE, toll_free=TOLL_FREE)


class TestRunner(unittest.TestCase):
    """Runs Test_Here_Maps.py once and checks the CSV it produces"""

    @classmethod
    def setUpClass(cls):
        cls._workspace = tempfile.TemporaryDirectory()
        workspace = Path(cls._workspace.name)

        # Work on a copy, so the checked in test cases and results are untouched
        testing_copy = workspace / "python" / "Testing"
        shutil.copytree(TESTING_DIR, testing_copy)

        stub_dir = workspace / "stub"
        stub_dir.mkdir()
        (stub_dir / "requests.py").write_text(REQUESTS_STUB)

        environment = dict(
            os.environ,
            PYTHONPATH=str(stub_dir),
            HERE_API_KEY="stub-key",
            TOLLGURU_API_KEY="stub-key",
        )

        # Start it the way the README does, from the python/ directory
        cls.completed = subprocess.run(
            [sys.executable, os.path.join("Testing", "Test_Here_Maps.py")],
            cwd=workspace / "python",
            env=environment,
            capture_output=True,
            text=True,
        )
        cls.result_file = testing_copy / "testCases_result.csv"

    @classmethod
    def tearDownClass(cls):
        cls._workspace.cleanup()

    def rows(self):
        self.assertTrue(
            self.result_file.exists(),
            f"no results were written\n{self.completed.stdout}\n{self.completed.stderr}",
        )
        with open(self.result_file, "r") as f:
            return list(reader(f))

    def test_runs_from_the_python_directory(self):
        """`python Testing/Test_Here_Maps.py` finds its test cases"""
        self.assertEqual(
            self.completed.returncode, 0, f"runner failed\n{self.completed.stderr}"
        )

    def test_every_row_has_a_cell_per_header_column(self):
        """Result rows line up with the header, including toll free routes"""
        rows = self.rows()
        header = rows[0]
        for row in rows[1:]:
            self.assertEqual(
                len(row), len(header), f"row {row[0]} does not match the header"
            )

    def test_toll_free_route_leaves_both_cost_columns_empty(self):
        """A route without tolls writes a tag cell and a cash cell"""
        rows = self.rows()
        header = rows[0]
        tag = header.index("Tollguru_Tag_Cost")
        cash = header.index("Tollguru_Cash_Cost")

        toll_free_rows = [row for row in rows[1:] if TOLL_FREE in row[1]]
        self.assertTrue(toll_free_rows, "no toll free test case was run")
        for row in toll_free_rows:
            self.assertEqual(row[tag], "")
            self.assertEqual(row[cash], "")

    def test_failed_route_is_not_priced_with_the_previous_polyline(self):
        """A routing error leaves the costs empty instead of the last route's"""
        rows = self.rows()
        header = rows[0]
        polyline = header.index("Input_polyline")
        tag = header.index("Tollguru_Tag_Cost")
        cash = header.index("Tollguru_Cash_Cost")

        failed_rows = [row for row in rows[1:] if row[polyline] == "Routing Error"]
        self.assertTrue(failed_rows, "no routing error test case was run")
        for row in failed_rows:
            self.assertEqual(row[tag], "", "costs of another route were reported")
            self.assertEqual(row[cash], "", "costs of another route were reported")


if __name__ == "__main__":
    unittest.main()
