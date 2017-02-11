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
import argparse
import logging
import re
from xml.etree.ElementTree import XML

import requests
from zeus import client


class UCSPlugin(object):
    def __init__(self):
        super(UCSPlugin, self).__init__()
        self.handlers = {}

        self.url = ''
        self.user = ''
        self.passwd = ''
        self.cookie = ''
        self.session = None
        self.zeus_client = None
        self.zeus_server = ''
        self.token = ''

        self.class_ids = []
        self.dn_list = set()
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

    def get_args(self):
        # read arguments from command line parameters
        parser = argparse.ArgumentParser()
        parser.add_argument("-c", "--ucs", nargs="?", type=str, default="0.0.0.0",
                            help="""IP or host name of unified computing server.
                                    \n(default: 0.0.0.0)""")
        parser.add_argument("-u", "--user", nargs="?", type=str,
                            default="ucspe",
                            help="User name of UCS. \n(default: ucspe)")
        parser.add_argument("-p", "--password", nargs="?", type=str,
                            default="ucspe",
                            help="Password of UCS \n(default: ucspe)")
        parser.add_argument("-l", "--log_level", nargs="?", type=str,
                            default="info",
                            help="Level of log. \n(default: info)")
        parser.add_argument("-t", "--token", nargs="?", type=str,
                            default="",
                            help="Token of ZEUS API.")
        parser.add_argument("-z", "--zeus", nargs="?", type=str,
                            default="127.0.0.1",
                            help="""IP or host name of ZEUS server.
                                    \n(default: 127.0.0.1)""")
        args = parser.parse_args()
        return args

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

    def set_up(self):
        # get arguments
        self.args = self.get_args()
        self.url = 'http://%s/nuova' % self.args.ucs
        self.token = self.args.token
        self.zeus_server = self.args.zeus
        self.user = self.args.user
        self.passwd = self.args.password

        # set log level
        self.set_loglevel(self.args.log_level)

        # set up a Zeus client to submit log to Zeus.
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
            # self.get_configResolveClasses(self.class_ids)
            #for class_id in self.class_ids:
            #    self.get_configResolveClass(class_id, inHierarchical='false')
            self.get_dn_config()
            self.event_loop()

    def close(self):
        # close the connection
        payload = """<aaaLogout inCookie="%s"/>""" % self.cookie
        res = self.send_request(payload)

        self.add_log('info', 'aaalogout', msg="Logout: %s" % res.text)

    def send_request(self, payload, json=None, **kwargs):
        # send request to UCS server.
        return self.session.post(self.url, data=payload, json=json, **kwargs)

    def event_loop(self):
        # Maintain a client to listen to UCS's async notification.
        # when receive data, sent them to zeus.
        # todo, handle the async notification.
        try:
            # update notification in time.
            self.logger.info("subscribe to UCS events")
            #self.subscribe_events()
        except KeyboardInterrupt:
            self.add_log('info', 'KeyboardInterrupt',
                         msg="KeyboardInterrupt")
        finally:
            self.unsubscribe_events()

    def handle_event(self, response, *args, **kwargs):
        print "event", response.text
        # self.submit_event(name, msg)

    def subscribe_events(self):
        payload = """<eventSubscribe
                     cookie="%s"></eventSubscribe>""" % self.cookie
        #self.send_request(payload, hooks=dict(response=self.handle_event))
        requests.post(self.url, payload, hooks=dict(response=self.handle_event))

    def unsubscribe_events(self):
        payload = """<eventUnsubscribe
                     cookie="%s"></eventUnsubscribe>""" % self.cookie
        self.send_request(payload)

    def submit_event(self, name, msg):
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

    def get_configFindDnsByClassId(self, class_id):
        payload = """<configFindDnsByClassId
                    classId="%s"
                    cookie="%s" />""" % (class_id, self.cookie)
        return self.send_request(payload)

    def get_Dns(self):
        for class_id in self.class_ids:
            res = self.get_configFindDnsByClassId(class_id)
            tree = XML(res.text)

            for dn in tree.iterfind('outDns/dn'):
                self.dn_list.add(dn.get('value'))

    def get_configResolveDn(self, dn, inHierarchical='false'):
        payload = """<configResolveDn dn="%s" cookie="%s"
                  inHierarchical="%s"/>""" % (dn, self.cookie, inHierarchical)
        return self.send_request(payload)

    def get_dn_config(self):
        self.get_Dns()
        for dn in self.dn_list:
            res = self.get_configResolveDn(dn)
            self.submit_event('dnconfig', msg=res.text)

    def get_configResolveClass(self, class_id, inHierarchical='false'):
        payload = """<configResolveClass cookie="%s"
                     inHierarchical="%s"
                     classId="%s"/>""" % \
                  (self.cookie, inHierarchical, class_id)
        res = self.send_request(payload)

        self.add_log('info', class_id, msg=res.text)

    def get_configResolveClasses(self, class_ids, inHierarchical='false'):
        class_id_xml = ''
        for id in class_ids:
            class_id_xml += """<Id value="%s"/>""" % id

        payload = """<configResolveClasses cookie = "%s"
                      inHierarchical = "%s">
                      <inIds> %s</inIds></configResolveClasses>""" % \
                  (self.cookie, inHierarchical, class_id_xml)

        res = self.send_request(payload)
        self.add_log('info', "classes", msg=res.text)


if __name__ == "__main__":
    ucs_plugin = UCSPlugin()
    ucs_plugin.set_up()

    ucs_plugin.close()
