# UCS(Unified Computing Server) Plugin


UCS plugin supports to collect data from Cisco Unified Computing Server.

## Dependencies

* [ucsmsdk](https://github.com/CiscoUcs/ucsmsdk)
    
        pip install ucsmsdk
    
* [zeus python client](https://github.com/CiscoZeus/python-zeusclient)
    
        pip install cisco-zeus


## Installation
 
 No need to install. Run it directly.

## Configuration
#### Configuration can be done by CLI.

    usage: ucs_plugin.py [-h] [-c [UCS]] [-u [USER]] [-p [PASSWORD]] [-s [SECURE]]
                         [-P [PORT]] [-l [LOG_LEVEL]] [-t [TOKEN]] [-z [ZEUS]]
    
    optional arguments:
      -h, --help            show this help message and exit
      -c [UCS], --ucs [UCS]
                            IP or host name of unified computing server. (default:
                            0.0.0.0)
      -u [USER], --user [USER]
                            User name of UCS. (default: ucspe)
      -p [PASSWORD], --password [PASSWORD]
                            Password of UCS (default: ucspe)
      -s [SECURE], --secure [SECURE]
                            Secure of connection. (default: False)
      -P [PORT], --port [PORT]
                            Port of TCP socket. (default: 80)
      -l [LOG_LEVEL], --log_level [LOG_LEVEL]
                            Level of log. (default: info)
      -t [TOKEN], --token [TOKEN]
                            Token of ZEUS API.
      -z [ZEUS], --zeus [ZEUS]
                            IP or host name of ZEUS server. (default: 127.0.0.1)


## Collected Data
UCS plugin collects many kinds of data, including:

* fault
    * faultInst

* performance
    * swSystemStats,
    * etherTxStats,
    * etherPauseStats,
    * etherRxStats,
    * etherErrStats,
    * adaptorVnicStats,
    * equipmentPsuStats,
    * processorEnvStats,
    * computeMbTempStats,
    * computeMbPowerStats,
    * equipmentChassisStats

* inventory
    * firmwareRunning,
    * storageLocalDisk,
    * vnicEtherIf,
    * lsServer,
    * fabricVsan,
    * fabricVlan,
    * fabricEthLanPcEp,
    * fabricEthLanPc,
    * etherPIo,
    * fabricDceSwSrvEp,
    * computeBlade,
    * equipmentPsu,
    * equipmentChassis,
    * equipmentSwitchCard,
    * equipmentIOCard,
    * topSystem,
    * computeRackUnit

##Event listening

UCS plugin also supports to listen to UCS's events, and submit them to Zeus server.

## Copyright
####Copyright
Copyright(C) 2017 - @Cisco Systems, Inc.

####License
Apache License, Version 2.0
