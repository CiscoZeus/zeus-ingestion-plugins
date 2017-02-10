# UCS(Unified Computing Server) Plugin

## Component

#### Plugin for sending UCS data

UCS plugin supports to collect data from Cisco Unified Computing Server.

## Installation
 
 No need to install.

## Configuration
#### Configuration can be done by CLI.

    usage: ucs_plugin.py [-h] [-c [UCS]] [-u [USER]] [-p [PASSWORD]]
                         [-l [LOG_LEVEL]] [-t [TOKEN]] [-z [ZEUS]]
    
    optional arguments:
      -h, --help            show this help message and exit
      -c [UCS], --ucs [UCS]
                            IP or host name of unified computing server. (default:
                            0.0.0.0)
      -u [USER], --user [USER]
                            User name of UCS. (default: ucspe)
      -p [PASSWORD], --password [PASSWORD]
                            Password of UCS (default: ucspe)
      -l [LOG_LEVEL], --log_level [LOG_LEVEL]
                            Level of log. (default: info)
      -t [TOKEN], --token [TOKEN]
                            Token of ZEUS API.
      -z [ZEUS], --zeus [ZEUS]
                            IP or host name of ZEUS server. (default: 127.0.0.1)


#### Collected Data
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


## Copyright
####Copyright
Copyright(C) 2017- @muzixing

####License
Apache License, Version 2.0
  
Currently, UCS plugin supports to fetch all kinds of data listed above. Events handler will be implemented very soon.
