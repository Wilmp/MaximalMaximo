owner=mbo.getOwner()
if owner is not None:
    mbo.setValue("FOREIGNKEY", owner.getUniqueIDValue())
    strKeyAttr=""
    # Loopen door maxattribute voor de gecombineerde key
    KeySet=mbo.getMboSet("NTUNIQUECOLUMNS")
    KeySet.setOrderBy("PRIMARYKEYCOLSEQ asc")
    Key=KeySet.moveFirst()
    while (Key):
        if Key.getString("MAXTYPE") in ["BIGINT","INTEGER","SMALLINT"]:
            strKeyAttr += owner.getInt(Key.getString("ATTRIBUTENAME"))
        else:
            strKeyAttr += owner.getString(Key.getString("ATTRIBUTENAME"))
     
        strKeyAttr += "_"
        Key=KeySet.moveNext()

    #Otherwise it is not possible to save to a directory.
    strKeyAttr=strKeyAttr.rstrip("_")
    mbo.setValue("KEYATTRIBUTEVALUE", strKeyAttr)

    if owner.getName() in ["MAXOBJECTCFG"]:
        if owner.getBoolean("INTERNAL"):
            mbo.setValue("INTERNAL", True)
    elif owner.getName() in ["MAXDOMAIN"]:
        if owner.getInt("INTERNAL")==1:
            mbo.setValue("INTERNAL", True)