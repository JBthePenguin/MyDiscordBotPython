from unittest import TestCase
from discord import Embed
from ..shaping import list_in_embed


class Obj():
    def __init__(self, id, name):
        self.id = id
        self.name = name


class ShaperTest(TestCase):
    """ Test case for format """

    def setUp(self):
        """ Init tests with a list and a tuple """
        self.objs = [Obj(154, 'Joe'), Obj(254, 'Bill'), Obj(398, 'Al')]
        self.embed_result = {
            'author': {
                'name': 'Guild name', 'icon_url': 'https://url.com/icon.png'},
            'fields': [
                {'inline': True, 'name': 'ID', 'value': '398\n254\n154'},
                {'inline': True, 'name': 'Name', 'value': 'Al\nBill\nJoe'}],
            'color': 1447446, 'type': 'rich', 'title': 'Members'}

    def test_list_in_embed(self):
        """ test list in embed """
        result = list_in_embed(
            self.objs, 'Guild name', 'https://url.com/icon.png', 'Members')
        self.assertIsInstance(result, Embed)
        embed_dict = result.to_dict()
        self.assertDictEqual(self.embed_result, embed_dict)
