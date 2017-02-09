# -*- coding: utf-8 -*-
# Copyright 2017 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import re
from xml.etree.ElementTree import XML

import requests
from zeus import client


class UCSPlugin(object):
    def __init__(self, host, user, passwd):
        super(UCSPlugin, self).__init__()
        self.handlers = {}

        self.url = 'http://%s/nuova' % host
        self.user = user
        self.passwd = passwd
        self.cookie = ''
        self.session = None
        self.zeus_client = None
        self.zeus_server = ''
        self.token = ''

        self.class_ids = []
        self.fault = ["faultInst"]

        self.performance = ["swSystemStats",
                            "etherTxStats",
                            "etherPauseStats",
                            "etherRxStats",
                            "etherErrStats",
                            "adaptorVnicStats",
                            "equipmentPsuStats",
                            "processorEnvStats",
                            "computeMbTempStats",
                            "computeMbPowerStats",
                            "equipmentChassisStats"]

        self.inventory = ["firmwareRunning",
                          "storageLocalDisk",
                          "vnicEtherIf",
                          "lsServer",
                          "fabricVsan",
                          "fabricVlan",
                          "fabricEthLanPcEp",
                          "fabricEthLanPc",
                          "etherPIo",
                          "fabricDceSwSrvEp",
                          "computeBlade",
                          "equipmentPsu",
                          "equipmentChassis",
                          "equipmentSwitchCard",
                          "equipmentIOCard",
                          "topSystem",
                          "computeRackUnit"]

        self.class_ids.extend(self.fault)
        self.class_ids.extend(self.performance)
        self.class_ids.extend(self.inventory)

    def check_level(self, loglevel):
        level = getattr(logging, loglevel.upper(), None)
        if not isinstance(level, int):
            raise ValueError('Invalid log level: %s' % loglevel)
        return level

    def set_loglevel(self, loglevel):
        level = self.check_level(loglevel)
        logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                            level=level)
        self.logger = logging.getLogger("USC-Plugin")

    def add_log(self, loglevel, name, msg, *args):
        level = self.check_level(loglevel)
        if self.logger.isEnabledFor(level):
            self.logger._log(level, msg, args)

        # submit event to zeus
        self.submit_event(name, msg)

    def set_up(self, token, server):
        # set up a Zeus client to submit log to Zeus.
        self.token = token
        self.zeus_server = server
        self.zeus_client = client.ZeusClient(self.token, self.zeus_server)

        # set up a http client to UCS server.
        with requests.Session() as self.session:
            payload = """<aaaLogin inName="%s" inPassword="%s"/>""" % \
                      (self.user, self.passwd)
            res = self.send_request(payload)

            tree = XML(res.text)
            self.cookie = tree.get("outCookie")

            self.add_log('info', 'aaalogin', msg="Login: %s" % payload)
            self.add_log('info', 'aaalogin', msg="Login: %s" % res.text)

            # get all calsses's data before go into a loop.
            # self.configResolveClasses(self.class_ids)

            self.event_loop()

    def close(self):
        # close the connection
        payload = """<aaaLogout inCookie="%s"/>""" % self.cookie
        res = self.send_request(payload)

        self.add_log('info', 'aaalogout', msg="Logout: %s" % res.text)

    def send_request(self, payload):
        # send request to UCS server.
        return self.session.post(self.url, data=payload)

    def event_loop(self):
        # Maintain a client to listen to UCS's async notification.
        # when receive data, sent them to zeus.
        # todo, handle the async notification.
        try:
            # update notification in time.
            self.logger.info("subscribe to UCS events")
            # self.subscribe_events()
        except KeyboardInterrupt:
            self.add_log('info', 'KeyboardInterrupt',
                         msg="KeyboardInterrupt")
        finally:
            self.unsubscribe_events()

    def subscribe_events(self):
        payload = """<eventSubscribe
                     cookie="%s"></eventSubscribe>""" % self.cookie
        self.send_request(payload)

    def unsubscribe_events(self):
        payload = """<eventUnsubscribe
                     cookie="%s"></eventUnsubscribe>""" % self.cookie
        self.send_request(payload)

    def submit_event(self, name, msg, ):
        # check name: All log names must have only letter and numbers
        if re.match('^[A-Za-z0-9]+$', name):
            # send log to zeus.
            msg = [{"message": msg}]
            self.logger.info(self.zeus_client.sendLog(name, msg))
        else:
            self.logger.error("""Name error: %s.
                              All log names must have only letter
                              and numbers (A-Za-z0-9).""" % name)

    def refresh_session(self):
        # refresh the session to UCS server.
        payload = """< aaaRefresh inName="%s" inPassword="%s"
                  inCookie="%s"/ >""" % (self.user, self.passwd, self.cookie)

        res = self.send_request(payload)
        tree = XML(res.text)
        self.cookie = tree.get("outCookie")

        self.add_log('info', 'aaaRefresh', msg="Refresh: %s" % res.text)

    def configResolveClass(self, class_id, inHierarchical='false'):
        payload = """<configResolveClass cookie="%s"
                     inHierarchical="%s"
                     classId="%s"/>""" % \
                  (self.cookie, inHierarchical, class_id)
        res = self.send_request(payload)

        self.add_log('info', class_id, msg="configResolveClass: %s" % res.text)

    def configResolveClasses(self, class_ids, inHierarchical='false'):
        class_id_xml = ''
        for id in class_ids:
            class_id_xml += """<Id value="%s"/>""" % id

        payload = """<configResolveClasses cookie = "%s"
                      inHierarchical = "%s">
                      <inIds> %s</inIds></configResolveClasses>""" % \
                  (self.cookie, inHierarchical, class_id_xml)

        res = self.send_request(payload)
        self.add_log('info', "classes",
                     msg="configResolveClasses: %s" % res.text)


if __name__ == "__main__":
    ucs_plugin = UCSPlugin("172.16.86.142", "ucspe", "ucspe")
    ucs_plugin.set_loglevel('INFO')
    ucs_plugin.set_up(token='837t80wepepwvees1oylrpcef80ceteg',
                      server='https://data04.ciscozeus.io')

    ucs_plugin.close()
