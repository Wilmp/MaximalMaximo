from java.lang import System
from psdi.server import MXServer
from psdi.iface.mic import MicService

mxServer = MXServer.getMXServer()
micService=MicService(mxServer)
micService.init()
userInfo = micService.getNewUserInfo()
ntinterfacelogSet = mxServer.getMboSet("NTINTERFACELOG",userInfo)

ntinterface = ntinterfacelogSet.add()
ntinterface.setValue("INTOBJECTNAME",strIntobjectname)
ntinterface.setValue("IFACENAME",strInterface)
ntinterface.setValue("OBJECTNAME",strTablename)
ntinterface.setValue("FOREIGNKEY",strKey)
ntinterface.setValue("APPLICATIONNAME",strApp)
ntinterface.setValue("DESCRIPTION",strDesc)
ntinterface.setValue("CONTENTS",strContents)
ntinterfacelogSet.save()