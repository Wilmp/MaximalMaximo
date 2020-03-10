from psdi.mbo import MboConstants

if len(mbo.getString("NTVALUEALPHA") )>0:
    mbo.setValue("CHECKED",True, MboConstants.NOACCESSCHECK )
    mbo.setValue("NTVALUE",0, MboConstants.NOACCESSCHECK )
else:
    mbo.setValue("CHECKED",False , MboConstants.NOACCESSCHECK )