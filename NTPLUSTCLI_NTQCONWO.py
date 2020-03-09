from java.lang import System
from java.util import HashMap
from psdi.server import MXServer
from psdi.common.xpath import XPathEvaluator
from org.jdom import Element, Document

#erData.breakData()
strAsset = str(erData.getXPathData("//*[local-name()='assetNumber']"))
if len(strAsset)<2:
    strAsset = str(erData.getXPathData("//*[local-name()='serialNumber']"))
System.out.println(strAsset)
if len(strAsset)>1:
    strApp = erData.getXPathData("//*[local-name()='applicationName']")
    #path = XPathEvaluator("//*[local-name()='masterPmTemplateNumber']", erData.getNamespaces())
    #strPOH=pathData(0).getText()
    try:
        strPOH=erData.getXPathData("//*[local-name()='masterPmTemplateNumber']")
        strDesc = "Workorder closed for: "
        strDesc += strPOH
    except:
        try:
            strWO = erData.getXPathData("//*[local-name()='workorderNumber']")
            strDesc = "Workorder closed for: "
            strDesc += strWO
        except:
            strDesc = "Workorder created for: "
            strDesc += strAsset
    service.error('workorder','nowoonassettrans', None)
    ctx=HashMap()
    ctx.put("strIntobjectname", "NTIFMREVASSETSTATUS")
    ctx.put("strInterface", "NTIFMREVASSETSTATUS")
    ctx.put("strTablename", "ASSET")
    ctx.put("strKey", strAsset)
    ctx.put("strApp", strApp)
    ctx.put("strDesc", strDesc)
    ctx.put("strContents", str(erData.getDataAsString()))

    #System.out.println(str(ctx))

    service.invokeScript("LIB_NTINTERFACELOG",ctx)