import unittest
from unittest.mock import Mock, patch
from app import Application, MailSystem

class ApplicationTest(unittest.TestCase):

    @patch.object(Application, 'get_names')
    def setUp(self, mock_get_names: Mock):
        # stub
        mock_get_names.return_value = (
            ['William', 'Oliver', 'Henry', 'Liam'],
            ['William', 'Oliver', 'Henry'],
        )
        self.app = Application()

    # There should not be so many decorator here!
    # the app.py could be refactored.
    @patch.object(MailSystem, 'write')
    @patch.object(MailSystem, 'send')
    @patch.object(Application, 'get_random_person')
    def test_app(self, mock_get_random: Mock, mock_send: Mock, mock_write: Mock):
        # Test Application
        mock_get_random.side_effect = (person for person in self.app.people)
        selected_person = self.app.select_next_person()
        self.assertEqual(selected_person, 'Liam')
        print(f'{selected_person} selected')

        # Test MailSystem
        mock_write.side_effect = lambda name: 'Congrats, ' + name + '!'
        mock_send.side_effect = lambda _, ctx: print(ctx)
        self.app.notify_selected()
        self.assertEqual(mock_write.call_count, len(self.app.selected))
        self.assertEqual(mock_send.call_count, len(self.app.selected))
        print(f'\n\n{mock_write.mock_calls}\n{mock_send.mock_calls}')


if __name__ == "__main__":
    unittest.main()
