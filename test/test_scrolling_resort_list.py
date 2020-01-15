from src.backend.scrolling_resort_list import ResortMasterList
from src.backend.config import ConfigFunctions
import unittest
from unittest.mock import MagicMock


class TestScrollingResortListNoSideEffects(unittest.TestCase):
    res_master_list: ResortMasterList = None

    def setUp(self) -> None:
        self.res_master_list = ResortMasterList(test_environ=True)

    def test_resort_master_list_instantiated_correctly(self):
        self.assertIsInstance(self.res_master_list, object)
        self.assertIsInstance(self.res_master_list.conf, ConfigFunctions)
        self.assertEqual(self.res_master_list.cur_index, 0)
        self.assertEqual(self.res_master_list.num_resorts, 2)
        self.assertEqual(len(self.res_master_list.resorts), 2)

    def test_get_current_index(self):
        self.assertEqual(self.res_master_list.get_current_index(), 0)

    def test_get_resort_amount(self):
        self.assertEqual(self.res_master_list.get_resort_amount(), 2)


class TestScrollingResortListWithSideEffects(unittest.TestCase):

    def test_get_resort_at_index(self):
        side_effect_resort_ml = ResortMasterList(test_environ=True)
        res_one = side_effect_resort_ml.get_resort_at_index(0)
        self.assertIsInstance(res_one, str)
        self.assertEqual(res_one, 'steamboat')
        self.assertEqual(side_effect_resort_ml.get_current_index(), 0)
        res_two = side_effect_resort_ml.get_resort_at_index(1)
        self.assertIsInstance(res_two, str)
        self.assertEqual(res_two, 'killington')
        self.assertEqual(side_effect_resort_ml.get_current_index(), 1)

    def test_get_next_resort(self):
        side_effect_resort_ml = ResortMasterList(test_environ=True)
        res_one = side_effect_resort_ml.get_next_resort()
        res_two = side_effect_resort_ml.get_next_resort()
        res_three = side_effect_resort_ml.get_next_resort()
        self.assertEqual(res_one, 'killington')
        self.assertEqual(res_two, 'steamboat')
        self.assertEqual(res_three, 'killington')

    def test_get_previous_resort(self):
        side_effect_resort_ml = ResortMasterList(test_environ=True)
        res_one = side_effect_resort_ml.get_previous_resort()
        res_two = side_effect_resort_ml.get_previous_resort()
        res_three = side_effect_resort_ml.get_previous_resort()
        self.assertEqual(res_one, 'killington')
        self.assertEqual(res_two, 'steamboat')
        self.assertEqual(res_three, 'killington')