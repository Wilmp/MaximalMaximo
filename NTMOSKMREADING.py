from psdi.server import MXServer
from psdi.mbo import MboRemote
from psdi.mbo import MboSetRemote
from java.util import Date


mosreadingSet=mbo.getMboSet('NTMOSREADINGSUPDATE')
if not mosreadingSet.isEmpty():
    mosread = mosreadingSet.moveFirst()
    while mosread:
        assetSet=mosread.getMboSet('NTASSET')
        if not assetSet.isEmpty():
            asset=assetSet.getMbo(0)
            notoperating=asset.getBoolean('NTNOTOPERATING')
            if mosread.getBoolean('VALID'):
                maximo=MXServer.getMXServer()
                curruser=maximo.getUserInfo(user)
                assetmeterSet=mosread.getMboSet('NTKMSTAND')
                personid=curruser.getUserName()
                mosread.setValue('DESCRIPTION',personid)
                if not assetmeterSet.isEmpty():
                    km=str(mosread.getInt('KMSINCEYESTERDAY'))
                    assetmeter=assetmeterSet.getMbo(0)
                    if not mosread.getBoolean('PROCESSED') and mosread.getDate('READINGDATE') < Date() and mosread.getDate('READINGDATE')>assetmeter.getDate('LASTREADINGDATE'):
                        assetmeter.setValue('NEWREADING',km)
                        assetmeter.setValue('NEWREADINGDATE',mosread.getDate('READINGDATE'))
                        assetmeter.setValue('INSPECTOR',personid)
                        mosread.setValue('PROCESSED',1)
                        bdagmeterSet=mosread.getMboSet('NTDAGENSTAND')
                        if not bdagmeterSet.isEmpty(): 
                            bdagmeter=bdagmeterSet.getMbo(0)
                            if mosread.getInt('KMSINCEYESTERDAY')==0 and asset.getString('NTSERIE') in ['DDZ','SGM','ICM'] and notoperating:
                                bdagmeter.setValue('NEWREADING','0')
                                bdagmeter.setValue('NEWREADINGDATE',mosread.getDate('READINGDATE'))
                                bdagmeter.setValue('INSPECTOR',personid)
                            else:
                                asset.setValue('NTNOTOPERATING',0)
                                bdagmeter.setValue('NEWREADING','1')
                                bdagmeter.setValue('NEWREADINGDATE',mosread.getDate('READINGDATE'))
                                bdagmeter.setValue('INSPECTOR',personid)
            mosread=mosreadingSet.moveNext()