if mbo.getInt('NTWORKORDERID'):
    woSet=mbo.getMboSet('NTTOPWO')
    if not woSet.isEmpty():
        wo=woSet.moveFirst()
        mbo.setValue('NTWONTLOCTYPE',wo.getString('NTLOCTYPE'))