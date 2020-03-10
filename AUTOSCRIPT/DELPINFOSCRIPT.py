#
# Licensed Materials - Property of IBM
# Copyright IBM Corporation. 2018
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp
#
# Modifications to this script are not supported. Any modifications that are made to the script may be overwritten during the next product upgrade. The functionality of this script is subject to change and may be migrated to an application in a future release.
#
#

from java.lang import Math
from psdi.mbo import MboConstants
from psdi.mbo import MboValueData
from psdi.mbo import MboValueInfo
from psdi.mbo import SqlFormat
from psdi.security import UserInfo
from psdi.server import MXServer
from psdi.util import MXRequiredFieldException

singleValueTables=["EMAIL", "SMS", "PHONE"]
personId = mbo.getString('PERSONID')
unprocessedFields = "" #Required fields will not be processed, but tracked and displayed in the final dialog.

def randomString(length, type):
  INTEGERS = '0123456789'
  #ALPHA = 'abcdefghijklmnopqrstuvwxyz'
  ALPHANUM = 'aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ0123456789'
  VALUES = None
    
  if (type == "integer"):
    VALUES = INTEGERS
  else:
    VALUES = ALPHANUM

  str = ""
  for i in range(length):
   pos = (int)(Math.random() * len(VALUES));
   str += VALUES[pos]

  if (type is "upper"):
   return str.upper()

  return str
# end def randomString

def delete(): 
 mxs = MXServer.getMXServer()
 userInfo = mbo.getThisMboSet().getUserInfo()
 piFields = mxs.getMboSet("MAXPINFO", userInfo)
 piFields.setOrderBy("deltype asc")
 field = piFields.moveFirst()
 
 while(field):
  objectName = field.getString("object")
  attributeName = field.getString("attribute")
  relationship = field.getString("relationship")
  pair = objectName+":"+attributeName
  deltype = field.getString("deltype")
  #service.log("#######################################################################################################################")  
  #service.log("############## Processing objectName = "+objectName+", attributeName = "+attributeName+", deltype = "+deltype+", relationship = "+relationship) 
  #service.log("#######################################################################################################################") 
  #objectSet = mxs.getMboSet(objectName, userInfo)
  objectSet = mbo.getMboSet("$"+objectName+attributeName, objectName, relationship)
  #objectSetWhere = " personid = '" + personId + "' "
  #objectSet.setWhere(objectSetWhere)
  #where = relationship.replace("PERSONID", "\'"+personId+"\'")
  #service.log("###########################################################")  
  #service.log("######## relationship = "+where)
  #service.log("###########################################################")
  #sqf = SqlFormat(where)
  #objectSet.setWhere(sqf.format())
  ct = objectSet.count()
  #service.log("###########################################################")  
  #service.log("######## count = "+str(ct))
  #service.log("###########################################################")

  thisObject = objectSet.moveFirst()
  
  counter = 1
  while(thisObject):
   #service.log(" ######################### counter = " +str(counter))
   counter += 1
   mvi = objectSet.getMboSetInfo().getMboValueInfo(attributeName)
   mvd = thisObject.getMboValueData(attributeName)
   maxtype=mvi.getMaxType()
   length = str(mvi.getLength())   
   required = mvi.isRequired()	
   hasList = mvd.hasList()   
   value = thisObject.getString(attributeName)
   valuestr = value.encode('utf-8')
   valuelen = len(value)   
   #service.log("############## maxtype = "+maxtype+", length  = "+length+", required = "+str(required)+", hasList = "+str(hasList)+", value = <<"+valuestr.decode('utf-8')+">>, valuelen = "+str(valuelen))

   if (deltype == "DELROW"):
    if (objectName in singleValueTables):
     #service.log("######################################################################################################")  
     #service.log("######### This is a delete row operation, therefore deleting the entire set.")
     #service.log("######################################################################################################")
     # Need to do a two stage delete since there are primary records.
     objectSet.setWhere("isprimary=0")
     objectSet.deleteAll(MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
     objectSet.save()     
     objectSet = mxs.getMboSet(objectName, userInfo)
     objectSetWhere = " personid = '" + personId + "' "
     objectSet.setWhere(objectSetWhere)
     objectSet.deleteAll(MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
     objectSet.save()
     break
    else:
     #service.log("###################################################################################################################################")
     #service.log("############## WE CANNOT DELETE THIS WHOLE ROW: objectName = "+objectName+", attributeName = "+attributeName+", deltype = "+deltype) 
     #service.log("###################################################################################################################################")
     global unprocessedFields
     unprocessedFields = unprocessedFields +"\n" + pair
     break
 
   if((deltype == "NULL") and (required is False)):
    #service.log("################# Nulling the value of "+attributeName+".")
    thisObject.setValue(attributeName, None, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
   elif((deltype == "NULL") and (required is True)):
    #service.log("##############################################################################")   
    #service.log("############ " +attributeName+ " is a required field")   
    #service.log("##############################################################################")   
    pair = objectName+":"+attributeName
    global unprocessedFields
    unprocessedFields = unprocessedFields +"\n" + pair
   
   if (deltype == "SCRAMBLE" and (not valuestr)):
    print("Nothing to do.")
   elif ((deltype == "SCRAMBLE") and (valuestr)):    
    if(maxtype=="UPPER"):
     randstr = randomString(valuelen,type="upper")
    elif (maxtype=="INTEGER" or maxtype=="BIGINT"):
     randstr = randomString(valuelen,type="integer")
    else:
     randstr = randomString(valuelen, None)
    #service.log("################## Scrambling the value of "+attributeName+" to be "+randstr+".")
    thisObject.setValue(attributeName,randstr,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION)
    #break  #Without these breaks, things go infinitely loopy (something about the setValue())

   thisObject = objectSet.moveNext()
  objectSet.save()
  #service.log("######################################################################################")

  field = piFields.moveNext()
# end def delete()

#main

delete()

if not unprocessedFields:
 params=[]
 errorgroup = "maxpinfo"
 errorkey = "completeNoFindings"
else: 
 #service.log("##################################################### uprocessedFields = >>>" + unprocessedFields+"<<<")
 params = [unprocessedFields]
 errorgroup = "maxpinfo"
 errorkey = "completeWithFindings"