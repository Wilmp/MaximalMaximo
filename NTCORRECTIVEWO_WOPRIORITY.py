if mbo.getInt("WOPRIORITY")==1:
    mbo.setValue("AUTOASSIGN",0)
    mbo.setValue("WORKLOCATION", None)
    mbo.setValue("NTINZETBEPERKING", None)
    mbo.setValue("NTWOVOORVERTREK", None)
    mbo.setValue("NTREDENOPENWO", None)
elif mbo.getInt("WOPRIORITY")==2:
    mbo.setValue("AUTOASSIGN",0)
    mbo.setValue("WORKLOCATION", None)
elif mbo.getInt("WOPRIORITY")==3:
    mbo.setValue("NTINZETBEPERKING", None)
    mbo.setValue("NTWOVOORVERTREK", None)
    mbo.setValue("NTREDENOPENWO", None)