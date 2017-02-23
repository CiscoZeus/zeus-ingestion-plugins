class_ids = ["faultInst", "123", "-34", "cv wr"]

dn_str = """ Managed Object			:	FaultInst
                --------------
                ack                             :no
                cause                           :activation-failed
                change_set                      :
                child_action                    :None
                code                            :F0856
                created                         :2017-02-16T20:17:28.343
                descr                           :Activation failed and Activate Status set to failed.
                dn                              :sys/chassis-2/cartridge-2/server-2/mgmt/fw-boot-def/bootunit-combined/fault-F0856
                highest_severity                :major
                id                              :52258
                last_transition                 :2017-02-16T20:17:28.343
                lc                              :
                occur                           :1
                orig_severity                   :major
                prev_severity                   :major
                rn                              :fault-F0856
                rule                            :firmware-boot-unit-activate-status-failed
                sacl                            :None
                severity                        :major
                status                          :None
                tags                            :network,server
                type                            :management"""

event_str_list = []

event_str_1 = """441
 <methodVessel cookie=""> <inStimuli>  <configMoChangeEvent cookie="" inEid="871484"> <inConfig> <trigMeta dn="sys/meta-trig-infra-fw" status="modified" trigTime="2017-02-19T03:02:59.236"/> </inConfig> </configMoChangeEvent>  <configMoChangeEvent cookie="" inEid="871485"> <inConfig> <trigMeta dn="sys/meta-trig-fi-reboot" status="modified" trigTime="2017-02-19T03:02:59.236"/> </inConfig> </configMoChangeEvent> </inStimuli> </methodVessel>"""
event_str_2 = """441
 <methodVessel cookie=""> <inStimuli>  <configMoChangeEvent cookie="" """
event_str_3 = """inEid="853812"> <inConfig> <trigMeta dn="sys/meta-trig-infra"""
event_str_4 = """-fw" status="modified" trigTime="2017-02-19T01:35:59.236"/>"""
event_str_5 = """ </inConfig> </configMoChangeEvent>  <configMoChangeEvent """
event_str_6 = """cookie="" inEid="853813"> <inConfig> <trigMeta dn="sys/meta"""
event_str_7 = """-trig-fi-reboot" status="modified" trigTime="2017-02-19T01:"""
event_str_8 = """35:59.236"/> </inConfig> </configMoChangeEvent> </inStimuli> </methodVessel>"""

event_str_list.append(event_str_1)
event_str_list.append(event_str_2)
event_str_list.append(event_str_3)
event_str_list.append(event_str_4)
event_str_list.append(event_str_5)
event_str_list.append(event_str_6)
event_str_list.append(event_str_7)
event_str_list.append(event_str_8)
