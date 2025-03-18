import unittest
from src.gui.pages import add_screen


class TestAddScreen(unittest.TestCase):

    def test_return(self):
        self.assertIsNotNone(add_screen.MainApp().run())

    def test_dict_access(self):
        self.assertEqual("Do Homework", add_screen.MainApp().run()["Title"])
