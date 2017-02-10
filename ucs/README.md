# UCS(Unified Computing Server) Plugin

UCS plugin supports to collect data from Cisco Unified Computing Server, including:

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
    
Currently, UCS plugin supports to fetch all kinds of data listed above. Events handler will be implemented very soon.
