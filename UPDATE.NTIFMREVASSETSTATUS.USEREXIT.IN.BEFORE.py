from java.lang import System
from java.util import HashMap 
from psdi.server import MXServer

#erData.breakData()
strErData = str(erData.getDataAsString())
strErData = str(erData.getDataAsString())
if "assetNumber" in strErData:
    strAsset = str(erData.getXPathData("//*[local-name()='assetNumber']"))
else:
    strAsset=""
if len(strAsset)<2 and "serialNumber" in strErData:
    strAsset = str(erData.getXPathData("//*[local-name()='serialNumber']"))
    
if len(strAsset)>1:
    if "applicationName" in strErData:
        strApp = erData.getXPathData("//*[local-name()='applicationName']")
    else:
        strApp="None"
    
    strDesc = "Maintenance Status: "
    if "maintenanceStatus" in strErData:
        strDesc += str(erData.getXPathData("//*[local-name()='maintenanceStatus']"))

    ctx=HashMap()
    ctx.put("strIntobjectname", "NTIFMREVASSETSTATUS")
    ctx.put("strInterface", "NTIFMREVASSETSTATUS")
    ctx.put("strTablename", "ASSET")
    ctx.put("strKey", strAsset)
    ctx.put("strApp", strApp)
    ctx.put("strDesc", strDesc)
    ctx.put("strContents", strErData)

    #System.out.println(str(ctx))
    
    service.invokeScript("LIB_NTINTERFACELOG",ctx)