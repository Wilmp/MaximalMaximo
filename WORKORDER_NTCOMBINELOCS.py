if mbo.getString('STATUS') in ('WGK','WOM'):
    combi = ""
    if mbo.getString('WORKLOCATION'):
        combi = "=" + mbo.getString('WORKLOCATION')
        if mbo.getString('REPAIRFACILITY'):
           combi = combi + ",=" + mbo.getString('REPAIRFACILITY')
    mbo.setValue('NTCOMBINELOCS',combi)