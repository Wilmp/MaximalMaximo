ntwpset=mbo.getMboSet('NTWPOUTSIDESERVICE')
if not ntwpset.isEmpty():
    wpout= ntwpset.moveFirst()
    if wpout.getDouble('ITEMQTY')>mbo.getDouble('QUANTITY'):
        wpout.setValue('NTCOPYRESERVED',0)