from psdi.mbo import MboRemote
from psdi.mbo import MboSetRemote

bdagSet=mbo.getMboSet("NTRELATEDBDAG")
kmreadSet=mbo.getMboSet("NTLASTKMREADING")
if not kmreadSet.isEmpty():
    kmread=kmreadSet.moveFirst()
    if kmread.getDouble("DELTA")==0 and mbo.getString("NTSERIE") in ['DDZ','SGM','ICM']:
        newreading="0"
    else:
        newreading="1"
    if not bdagSet.isEmpty():
        bdag= bdagSet.moveFirst()
        bdag.setValue("NEWREADING",newreading)
        bdag.setValue("NEWREADINGDATE", kmread.getDate("READINGDATE"))
        bdag.setValue("INSPECTOR","MXINTADM")