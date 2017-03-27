# UCS(Unified Computing System) Agent


UCS agent supports to collect data from Cisco Unified Computing System manager server.

## Dependencies


* [pycurl](http://pycurl.io/)

        pip install pycurl
        

* [xmltodict](https://pypi.python.org/pypi/xmltodict)

        pip install xmltodict
        
* [ucsmsdk](https://github.com/CiscoUcs/ucsmsdk)
    
        pip install ucsmsdk

    
* [zeus python client](https://github.com/CiscoZeus/python-zeusclient)
    
        pip install cisco-zeus


## Installation
 
 We don't need to install ucs_agent, and just run it directly with CLI.

## Configuration
#### Configuration can be done by CLI.
    
    usage: ucs_agent.py [-h] [-c [UCS]] [-u [USER]] [-p [PASSWORD]] [-s [SECURE]]
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
                            Level of log: CRITICAL, ERROR, WARN, WARNING, INFO,
                            DEBUG, NOTSET (default: INFO)
      -t [TOKEN], --token [TOKEN]
                            Token of ZEUS API.
      -z [ZEUS], --zeus [ZEUS]
                            IP or host name of ZEUS server. (default: 127.0.0.1)


## Collected Data
UCS agent collects many kinds of data, including:

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

## Event listening

UCS agent also supports to listen to UCS's asynchronous events, and submit them to Zeus server.

## Copyright
#### Copyright
Copyright(C) 2017 - @Cisco Systems, Inc.

#### License
Apache License, Version 2.0
