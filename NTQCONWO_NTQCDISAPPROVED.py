if mbo.getBoolean('NTQCDISAPPROVED')==True:
    mbo.setValue('NTQCAPPROVED',False)
    mbo.setValue('NTNVT',False)