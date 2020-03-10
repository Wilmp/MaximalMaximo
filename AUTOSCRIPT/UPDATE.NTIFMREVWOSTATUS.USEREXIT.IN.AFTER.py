from java.lang import System
from java.util import HashMap
from psdi.server import MXServer

#erData.breakData()
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
    if "masterPmTemplateNumber" in strErData:
        strPOH=erData.getXPathData("//*[local-name()='masterPmTemplateNumber']")
        strDesc = "Workorder closed for: "
        strDesc += strPOH
    elif "workorderNumber" in strErData:
        strWO = erData.getXPathData("//*[local-name()='workorderNumber']")
        strDesc = "Workorder closed for: "
        strDesc += strWO
    else:
        strDesc = "Workorder created for: "
        strDesc += strAsset
    
    ctx=HashMap()
    ctx.put("strIntobjectname", "NTIFMREVWOSTATUS")
    ctx.put("strInterface", "NTIFMREVWOSTATUS")
    ctx.put("strTablename", "WORKORDER")
    ctx.put("strKey", strAsset)
    ctx.put("strApp", strApp)
    ctx.put("strDesc", strDesc)
    ctx.put("strContents", strErData)

    #System.out.println(str(ctx))

    service.invokeScript("LIB_NTINTERFACELOG",ctx)