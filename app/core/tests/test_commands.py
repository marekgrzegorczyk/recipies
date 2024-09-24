from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError as DjangoOperationalError
from django.test import SimpleTestCase
from psycopg2 import OperationalError as Psycopg2OperationalError


@patch('core.management.commands.wait_for_db.Command.check')
# check is provied by BaseCommand class, and it is used to check
# if the database is available
class CommandTests(SimpleTestCase):

    def test_wait_for_db_ready(self, patched_check):
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        patched_check.side_effect = [Psycopg2OperationalError] * 2 + \
                                    [DjangoOperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)

        patched_check.assert_called_with(databases=['default'])
