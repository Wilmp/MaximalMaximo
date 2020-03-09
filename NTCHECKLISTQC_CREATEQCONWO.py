#Get the current assettrans (=laatste of huidige overstand)
assetSet=mbo.getMboSet('ASSET')
asset=assetSet.moveFirst()
assettransSet=asset.getMboSet('NTASSETTRANSOBCURRENT')
if not assettransSet.isEmpty():
    binnenkomst= assettransSet.moveFirst()
    ntqconwoSet=mbo.getMboSet('NTQCONWO')
    refwo = mbo.getString('REFWO')
    typeQC = mbo.getString('NTQCTYPE')

    #Depending on the type, add workorders to the ntqconwo table
    if typeQC in ('EBK','ONDERHOUD'):
        if ntqconwoSet.isEmpty():
            assettransid=binnenkomst.getInt('ASSETTRANSID')
            if typeQC=='ONDERHOUD':
                wolistSet=binnenkomst.getMboSet('NTWOPACKAGECURRENTSAMPLE')
            elif typeQC=='EBK':
                wolistSet=binnenkomst.getMboSet('NTWOPACKAGECURRENT') 
            if not wolistSet.isEmpty():
                wo=wolistSet.moveFirst()
                while wo:
                    ntqconwo=ntqconwoSet.addAtEnd()
                    ntqconwo.setValue('ASSETTRANSID',assettransid)
                    ntqconwo.setValue('REFWO',refwo)
                    ntqconwo.setValue('WORKORDERID',wo.getInt('WORKORDERID'))
                    wo=wolistSet.moveNext()