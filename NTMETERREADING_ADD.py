from psdi.server import MXServer
from psdi.mbo import MboRemote
from psdi.mbo import MboSetRemote
from java.util import Date

maximo=MXServer.getMXServer()
curruser=maximo.getUserInfo(user)
personid=curruser.getUserName()

#Ophalen gerelateerd asset
notoperating=False
assetSet=mbo.getMboSet('ASSET')

if not assetSet.isEmpty():
    asset=assetSet.getMbo(0)
    notoperating=asset.getBoolean('NTNOTOPERATING')
    #Relatie naar BDAG op dezelfde dag
    bdagSet=asset.getMboSet('NTRELATEDBDAG')
    #Toevoegen BDAG meting
    if not bdagSet.isEmpty():
        bdag=bdagSet.moveFirst()
        if bdag.getDate("LASTREADINGDATE") < mbo.getDate("NEWREADINGDATE"):
            if mbo.getString("DELTAVALUE")==0 and asset.getString('NTSERIE') in ['DDZ','SGM','ICM'] and notoperating:
                bdag.setValue("NEWREADING","0")
                bdag.setValue("NEWREADINGDATE",mbo.getDate("NEWREADINGDATE"))
                bdag.setValue("INSPECTOR",personid)
            else:
                bdag.setValue("NEWREADING","1")
                bdag.setValue("NEWREADINGDATE",mbo.getDate("NEWREADINGDATE"))
                bdag.setValue("INSPECTOR",personid)