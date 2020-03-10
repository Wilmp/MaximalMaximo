if mbo.getString('CLNUM')=='QC' and mbo.getInt('SEQUENCE') < 150:
    if mbo.getBoolean('DEFECT')==True:
        mbo.setValue('CHECKED',False)
        mbo.setValue('NTNVTTEXT',None)