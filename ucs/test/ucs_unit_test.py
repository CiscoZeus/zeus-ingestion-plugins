from __future__ import absolute_import
import unittest

from mock import MagicMock
from zeus import client

from test.config.config import ZEUS_TOKEN, ZEUS_SERVER, LOG_LEVEL
from test.test_data.ucs_unit_test_data import dn_str, event_str_list, class_ids
from ucs_plugin import UCSPlugin


class UCSTest(unittest.TestCase):
    def setUp(self):
        self.ucs_plugin = UCSPlugin()
        self.ucs_plugin.set_log_level(LOG_LEVEL)
        self.ucs_plugin.zeus_client = client.ZeusClient(ZEUS_TOKEN, ZEUS_SERVER)
        self.original_get_dn_conf = UCSPlugin.get_dn_conf

    # test submit data to zeus.
    def test_submit(self):
        UCSPlugin.get_dn_conf = MagicMock()
        for class_id in class_ids:
            response = self.ucs_plugin.add_log("info", class_id, msg=dn_str)
            # if name checking is correct, assert the return
            # else, a error will occur
            if response:
                self.assertEqual(response[0], 200)

    # test submit async events
    def test_submit_event(self):
        event_str = ''
        for i in range(len(event_str_list)):
            event_str += event_str_list[i]

            str_list = event_str.split("\n", 1)
            length = int(str_list[0])
            self.ucs_plugin.submit_async_events(event_str_list[i])
            self.assertLessEqual(len(self.ucs_plugin.event_string), length,
                                 msg="Event's length must equal or less than"
                                     "length, otherwise,"
                                     "it should be sent already.")
            event_str = self.ucs_plugin.event_string

    def tearDown(self):
        # UCSPlugin.get_args = self.original_get_args
        UCSPlugin.get_dn_conf = self.original_get_dn_conf
