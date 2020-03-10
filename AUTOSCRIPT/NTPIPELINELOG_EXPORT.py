from sys import *

from java.io import *
from java.lang import System, Class, String, StringBuffer
from java.nio.charset import Charset
from java.util import Date, Properties, List, ArrayList, AbstractList

from org.apache.commons.codec.binary import Base64
from org.apache.http import HttpEntity, HttpHeaders, HttpResponse, HttpVersion
from org.apache.http.client import ClientProtocolException, HttpClient
from org.apache.http.client.entity import UrlEncodedFormEntity
from org.apache.http.client.methods import HttpPost, HttpGet
from org.apache.http.entity import StringEntity
from org.apache.http.impl.client import DefaultHttpClient
from org.apache.http.message import BasicNameValuePair
from org.apache.http.params import BasicHttpParams, HttpParams, HttpProtocolParamBean

from com.ibm.json.java import JSONObject, JSONArray
from psdi.mbo import Mbo, MboRemote, MboSet, MboSetRemote
from psdi.security import UserInfo
from psdi.server import MXServer

#Recursively go through the json file. Maximo always creates JSON in API responses in the following order
#Array-Object-Array-Object etc. The first array was already skipped by starting from "member"
#certain maximo fields shouldnt be in the json as they could lead to errors and/or are unnecessary
def recursiveJSON(jsObject, addProps):
    jsObjectTemp = JSONObject()
    if addProps:
		jsObjectTemp.put("timestamp", mbo.getString("TIMESTAMP"))
		jsObjectTemp.put("apiaction", mbo.getString("ACTION"))
    for strName in jsObject.keySet():
        
        if strName is not None:
            jsElement = jsObject.get(strName)
            if type(jsElement).__name__== "JSONArray":
                #System.out.println(strName)
                #System.out.println(jsElement.size())
                jsArrayTemp=JSONArray()
                for i in range(jsElement.size()):
                    
                    if type(jsElement[i]).__name__== "JSONObject":
                        jsElementTemp=jsElement[i]

                        jsElementTemp=recursiveJSON(jsElementTemp, False)
                        jsArrayTemp.add(i, jsElementTemp)
                        
                jsObjectTemp.put(strName,jsArrayTemp)
            elif strName in ["href","_rowstamp"]:
                continue
            elif "collectionref" in strName:
                continue
            elif "localref" in strName:
                continue
            elif "_description" in strName:
                continue
            else:
                jsObjectTemp.put(strName, jsObject.get(strName))
            
    return jsObjectTemp

    
#jsonstr = createJSONstring()
client = None

# get connection properties from System Properties
properties = MXServer.getMXServer().getConfig()
host = properties.getProperty("mxe.oslc.restwebappurl")

# get Pipeline data for the address (href)
ntpipelineapiSet=mbo.getMboSet("NTPIPELINEAPI")
if ntpipelineapiSet.isEmpty():
    service.error('ntpipeline','pipelineMap', None) #Break
pipelineapi=ntpipelineapiSet.moveFirst()
uri = host + '/os/'
uri = uri + pipelineapi.getString("INTOBJECTNAME")
uri = uri + '?lean=1&oslc.where='                   #MAXDOMAINID='
uri = uri + pipelineapi.getString("UNIQUECOLUMN") +'='
uri=uri+str(mbo.getInt("FOREIGNKEY"))
uri=uri+'&oslc.select=*'
clientid = "maxadmin"
clientsecurity = "maxadmin"


# get authentication header
auth = clientid + ":" + clientsecurity
encodedAuth = String(Base64.encodeBase64(String.getBytes(auth, 'ISO-8859-1')),"UTF-8")
authHeader =  str(encodedAuth)

# get http parameters
params = BasicHttpParams()
paramsBean = HttpProtocolParamBean(params)
paramsBean.setVersion(HttpVersion.HTTP_1_1)
paramsBean.setContentCharset("UTF-8")
paramsBean.setUseExpectContinue(True)

# get http body entities
formparams = ArrayList()
#formparams.add(BasicNameValuePair("username", username))
entity = UrlEncodedFormEntity(formparams, "UTF-8")

# get client, http headers and request
client = DefaultHttpClient()
request = HttpGet(uri)
request.setParams(params)
request.addHeader(HttpHeaders.CONTENT_TYPE, "application/json")
request.addHeader(HttpHeaders.ACCEPT, "application/x-www-form-urlencoded")
request.addHeader("MAXAUTH", authHeader)

# get client response
response = client.execute(request)
if response.getStatusLine().getStatusCode()>300:
    service.error('ntpipeline','apiErrror', None) #Break

obj = JSONObject()
obj = JSONObject.parse(response.getEntity().getContent())

objToSend = obj.get("member")

if objToSend:
    obj = objToSend.get(0)

    strHREF=str(obj.get("href"))   

    obj=recursiveJSON(obj, True)
    responseString = obj.serialize(True)
    
    intPos = strHREF.find("/_",1)+2
    strKeyAttrB64=strHREF[intPos:]

    mbo.setValue("KEYATTRIBUTEVALUEBASE64", strKeyAttrB64)

    mbo.setValue("JSON", responseString)

    strFile = properties.getProperty("ntpipeline.folder")

    strFile += mbo.getString("OBJECTNAME") + "\\"
    strFile += mbo.getString("KEYATTRIBUTEVALUE") + ".json"

    filExport=File(None, strFile)

    #if filExport.createNewFile():
        #System.out.println( "Created File: " + strFile)
    writerExport=FileWriter(filExport)
    writerExport.write(responseString)
    writerExport.close()

    mbo.setValue("LINK", filExport.getAbsolutePath())
    
    #Export the ntpipelinelog record
    uri = host + '/os/'
    uri = uri + "PA_NTPIPELINE_NTPIPE"
    uri = uri + '?lean=1&oslc.where=NTPIPELINELOGID='
    uri=uri+str(mbo.getInt("NTPIPELINELOGID"))
    uri=uri+'&oslc.select=*'
    client = DefaultHttpClient()
    request2 = HttpGet(uri)
    request2.setParams(params)
    request2.addHeader(HttpHeaders.CONTENT_TYPE, "application/json")
    request2.addHeader(HttpHeaders.ACCEPT, "application/x-www-form-urlencoded")
    request2.addHeader("MAXAUTH", authHeader)
    #request.setEntity(entity)
    
    # get client response
    response2 = client.execute(request2)
    if response2.getStatusLine().getStatusCode()>300:
        service.error('ntpipeline','apiErrror', None) #Break

    obj = JSONObject()
    obj = JSONObject.parse(response2.getEntity().getContent())

    objToSend = obj.get("member")

    if objToSend:
        obj = objToSend.get(0)
        obj=recursiveJSON(obj, False)
        
        responseString = obj.serialize(True)
        strFile = properties.getProperty("ntpipeline.folder")

        strFile += "NTPIPELINELOG\\"
        
        strFile += mbo.getString("OBJECTNAME") + "_"
        strFile += mbo.getString("KEYATTRIBUTEVALUE")
        
        strFile += ".json"

        filExport=File(None, strFile)

        #if filExport.createNewFile():
            #System.out.println( "Created File: " + strFile)
        writerExport=FileWriter(filExport)
        writerExport.write(responseString)
        writerExport.close()

else:
    mbo.setValue("INTERNAL",True)
    mbo.setValue("DESCRIPTION", "Couldnt get JSON Object. " + mbo.getString("DESCRIPTION"))