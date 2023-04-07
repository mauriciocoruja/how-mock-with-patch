import unittest
from datetime import datetime
from unittest.mock import patch, Mock

from requests import Timeout

from my_calendar import get_holidays, is_weekday


class MyCalendarCase(unittest.TestCase):

    def mock_ok_respose(self):
        response_mock = {
            "status_code": 200,
            "json.return_value": {"12/25": "Christmas", "9/7": "Independance Day"}}
        return Mock(**response_mock)

    def mock_nok_response(self):
        response_mock = {
            "status_code": 400,
            "return_value": None}
        return Mock(**response_mock)

    @patch("my_calendar.requests.get", side_effect=mock_ok_respose)
    def test_hollidays_sucess(self, monkeypatch):
        self.assertEqual(get_holidays()['12/25'], "Christmas")

        with self.assertRaises(KeyError):
            get_holidays()['12/26']
        self.assertIsNotNone(get_holidays())

    @patch("my_calendar.requests.get", side_effect=mock_nok_response)
    def test_hollidays_fail(self, monkeypatch):
        self.assertIsNone(get_holidays())

    @patch("my_calendar.requests.get", side_effect=Timeout)
    def test_timout_exception(self, monkeypatch):
        with self.assertRaises(Timeout):
            get_holidays()

    @patch("my_calendar.datetime")
    def test_is_work_day(self, monkeypatch):
        monkeypatch.today.return_value = datetime(2023, 3, 3)
        self.assertTrue(is_weekday())

    @patch("my_calendar.datetime")
    def test_is_not_work_day(self, mock_datetime):
        mock_datetime.today.return_value = datetime(2023, 3, 4)
        self.assertFalse(is_weekday())


if __name__ == '__main__':
    unittest.main()
