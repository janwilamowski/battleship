import unittest
from Field import Field


class FieldTest(unittest.TestCase):
    def test_show_hide(self):
        field = Field(None, (0, 0))
        assert not field.visible
        field.show()
        assert field.visible
        field.hide()
        assert not field.visible
