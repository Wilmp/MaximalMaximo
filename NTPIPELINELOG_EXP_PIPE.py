from java.io import *
from java.lang import System

from psdi.mbo import Mbo, MboRemote, MboSet, MboSetRemote
from psdi.server import MXServer

properties = MXServer.getMXServer().getConfig()

clientid = "maxadmin"
clientsecurity = "maxadmin"
# get authentication header
authHeader =  'bWF4YWRtaW46bWF4YWRtaW4='

ntpipelineSet=mbo.getMboSet("NTPIPELINEPACKLINE")
ntpipelineSet.setOrderBy("SEQUENCE")
if ntpipelineSet.isEmpty():
    service.error('ntpipeline','pipelineMap', None) #Break


strFile = properties.getProperty("ntpipeline.folder")

strFile += "AA_RUN\\"
strFile += mbo.getString("PACKAGENAME")
strFile += ".txt"

filExport=File(None, strFile)

if filExport.createNewFile():
    System.out.println( "Created File: " + strFile)
writerExport=FileWriter(filExport,True)

ntpipeline=ntpipelineSet.moveFirst()
while ntpipeline:
    writerExport.write('curl -H "Accept-Encoding: gzip,deflate" -H "Content-Type: application/json" -H "MAXAUTH: ')
    writerExport.write(authHeader)
    writerExport.write('" -H "x-method-override: PATCH" -X POST --data @')
    writerExport.write(ntpipeline.getString("OBJECTNAME")) 
    writerExport.write('/')
    
    ntpipelinelogSet=ntpipeline.getMboSet("NTPIPELINELOG")
    ntpipelinelog=ntpipelinelogSet.moveFirst()
    strKeyAttr=ntpipelinelog.getString("KEYATTRIBUTEVALUE")
    writerExport.write(strKeyAttr)
    writerExport.write('.json ')
    writerExport.write('${BUILD_URL}')
    writerExport.write('/maxrest/oslc/os/')
    
    apiNameSet=ntpipelinelog.getMboSet("NTPIPELINEAPI")
    
    if apiNameSet.isEmpty():
        service.error('ntpipeline','pipelineMap', None) #Break
    pipelineapi=apiNameSet.moveFirst()
    
    writerExport.write(pipelineapi.getString("INTOBJECTNAME"))
    writerExport.write('/_')
    writerExport.write(ntpipelinelog.getString("KEYATTRIBUTEVALUEBASE64"))
    writerExport.write('?lean=1 -i')

    writerExport.write('\r\n')
    ntpipeline=ntpipelineSet.moveNext()

writerExport.close()