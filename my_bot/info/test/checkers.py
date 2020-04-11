from unittest import TestCase
from ..checkers import empty_content


class CheckersTest(TestCase):
    """ Test case for Checkers """

    def setUp(self):
        """ Init tests with a list and a tuple """
        self.list_objs = [1, 2, 3]
        self.tuple_objs = (1, 2, 3)

    def test_empty_content(self):
        """ Test empty content """
        # list
        location = 'Guild test'
        obj_type = 'member test'
        result = empty_content(self.list_objs, 'Guild', 'member')
        self.assertListEqual(result, [1, 2, 3])
        result = empty_content([], location, obj_type)
        self.assertEqual(result, "Guild test: No member test")
        # tuple
        result = empty_content(self.tuple_objs, 'Guild', 'member')
        self.assertTupleEqual(result, (1, 2, 3))
        result = empty_content((), location, obj_type)
        self.assertEqual(result, "Guild test: No member test")
