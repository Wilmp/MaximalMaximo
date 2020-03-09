if mbo.getString('CLNUM')=='QC' and mbo.getInt('SEQUENCE') < 150:
    if mbo.getString('NTNVTTEXT'):
        mbo.setValue('CHECKED',False)
        mbo.setValue('DEFECT',False)