from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        # we want to mock the behavior of the getitem function
        # to simulate whether we have a connection to the db
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True  # simulates having a connection to the db
            call_command('wait_for_db')

            self.assertEqual(gi.call_count, 1)

    # mock the sleep function so that our tests run faster
    # can also use patch as a decorator
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db - calls the db 5 times, then connects
           on the 6th"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # raises the operational error the first five times you
            # call getitem
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')

            self.assertEqual(gi.call_count, 6)
