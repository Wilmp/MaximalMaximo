if mbo.getString('CLNUM')=='QC' and mbo.getInt('SEQUENCE') < 150:
    if mbo.getBoolean('CHECKED')==True:
        mbo.setValue('DEFECT',False)
        mbo.setValue('NTNVTTEXT',None)