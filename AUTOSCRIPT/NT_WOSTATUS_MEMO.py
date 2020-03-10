#Bij status wijziging met memo, wordt gekeken naar de reinigingsrelatie NTREINWO
if mbo.getString("STATUS") in ["WGK","GEREED"]:
    woSet=mbo.getMboSet("NTREINWO")
    wo=woSet.getMbo(0)
    if not woSet.isEmpty():
        if (wo.getString("STATUS") =="GEREED" or wo.getString("STATUS") =="WGK") and mbo.getString("MEMO"):
            ntreinwostatusSet = mbo.getMboSet("NTREINWOSTATUSINIT")
            ntreinwostatus = ntreinwostatusSet.addAtEnd()
            ntreinwostatus.setValue("STATUS",mbo.getString("STATUS"))
            ntreinwostatus.setValue("CHANGEBY",mbo.getString("CHANGEBY"))
            ntreinwostatus.setValue("CHANGEDATE",mbo.getDate("CHANGEDATE"))
            ntreinwostatus.setValue("WOSTATUSID",mbo.getInt("WOSTATUSID"))
            ntreinwostatus.setValue("WONUM",mbo.getString("WONUM"))
            if wo.getString("STATUS")=="GEREED" and mbo.getString("MEMO"):
                wo.setValue("NTREINONVOLLEDIG", mbo.getString("MEMO"))
                ntreinwostatus.setValue("NTREINONVOLLEDIG", mbo.getString("MEMO"))
            elif wo.getString("STATUS")=="WGK" and mbo.getString("MEMO"):
                wo.setValue("NTREINTERUGGAVE", mbo.getString("MEMO"))
                ntreinwostatus.setValue("NTREINTERUGGAVE", mbo.getString("MEMO"))