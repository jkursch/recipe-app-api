'''
Test custome Django management commands
'''

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# Add a decorator (@patch())
@patch('core.management.commands.wait_for_db.Command.check')  # the command that we will be mocking
class CommandsTests(SimpleTestCase):
  """Test commands."""

  def test_wait_for_db_ready(self, patched_check):
    """Test waiting for database if database ready."""
    patched_check.return_value = True  # when the command in the decorator is called inside our test case, return the true value

    call_command('wait_for_db')  # also tests that the command is set up correctly and can be called in the project
    
    patched_check.assert_called_once_with(databases=['default'])

  @patch('time.sleep')
  def test_wait_for_db_delay(self, patched_sleep, patched_check):
    """Test waiting for database when getting operational error"""
    patched_check.side_effect = [Psycopg2Error] * 2 + \
      [OperationalError] * 3 + [True]  # First raise two Psycopg2 OperationErrors then 3 Django OperationErrors then return True
    
    call_command('wait_for_db')

    self.assertEqual(patched_check.call_count, 6)
    patched_check.assert_called_with(databases=['default'])