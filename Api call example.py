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
def recursiveJSON(jsObject):
    jsObjectTemp = JSONObject()
    for strName in jsObject.keySet():
        
        if strName is not None:
            jsElement = jsObject.get(strName)
            #System.out.println(type(jsElement).__name__)
            if type(jsElement).__name__== "JSONArray":
                System.out.println(strName)
                System.out.println(jsElement.size())
                jsArrayTemp=JSONArray()
                for i in range(jsElement.size()):
                    
                    if type(jsElement[i]).__name__== "JSONObject":
                        jsElementTemp=jsElement[i]
                        System.out.println(type(jsElement[i]).__name__)
                        jsElementTemp=recursiveJSON(jsElementTemp)
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
host = "http://localhost"

# get Pipeline data for the address (href)
ntpipelineapiSet=mbo.getMboSet("NTPIPELINEAPI")
if ntpipelineapiSet.isEmpty():
    service.error('workorder','qcwoalreadygenerated', None) #placeholder error message
pipelineapi=ntpipelineapiSet.moveFirst()
uri = host + '/maxrest/oslc/os/'                   #MXAPIDOMAIN'
uri = uri + pipelineapi.getString("INTOBJECTNAME")
uri = uri + '?lean=1&oslc.where='                   #MAXDOMAINID='
uri = uri + pipelineapi.getString("UNIQUECOLUMN") +'='
uri=uri+str(mbo.getInt("FOREIGNKEY"))
uri=uri+'&oslc.select=*'
System.out.println(uri)
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
#request.setEntity(entity)

# get client response
response = client.execute(request)

# return JSON response and access token
mbo.setValue("STATUS", str(response.getStatusLine().getStatusCode()))

obj = JSONObject()
obj = JSONObject.parse(response.getEntity().getContent())
#System.out.println( str(obj))

objToSend = obj.get("member")

obj = objToSend.get(0)

strHREF=str(obj.get("href"))   
#responseString = obj.toString()
#########################
obj=recursiveJSON(obj)
#System.out.println( str(obj))
#########################
responseString = obj.serialize(True)

intPos = strHREF.find("/_",1)+2
strKeyAttrB64=strHREF[intPos:]
strKeyAttr=""
## Loopen door maxattribute
KeySet=mbo.getMboSet("NTUNIQUECOLUMNS")
KeySet.setOrderBy("PRIMARYKEYCOLSEQ asc")
Key=KeySet.moveFirst()
while (Key):
    strKey=Key.getString("ATTRIBUTENAME").lower()
    System.out.println(strKey)
    strKeyAttr += str(obj.get(strKey))
    strKeyAttr += "_"
    Key=KeySet.moveNext()

strKeyAttr=strKeyAttr.rstrip("_")

#Otherwise it is not possible to save to a directory.

System.out.println(strKeyAttr)

mbo.setValue("KEYATTRIBUTEVALUEBASE64", strKeyAttrB64)
mbo.setValue("KEYATTRIBUTEVALUE", strKeyAttr)
System.out.println(mbo.getString("DESCRIPTION"))
System.out.println(mbo.getString("KEYATTRIBUTEVALUE"))
mbo.setValue("JSON", responseString)

System.out.println(strKeyAttrB64)
strFile = properties.getProperty("ntpipeline.folder")

#strFile = "\\\\toolingserver\\tools\\BitBucket\\WMU\\maximo-configuratie\\"
strFile += mbo.getString("OBJECTNAME") + "\\"
strFile += strKeyAttr + ".json"
#mbo.setValue("DESCRIPTION_LONGDESCRIPTION", strFile)

filExport=File(None, strFile)
System.out.println( filExport.getAbsolutePath())

if filExport.createNewFile():
    System.out.println( "Created File: " + strFile)
writerExport=FileWriter(filExport)
writerExport.write(responseString)
writerExport.close()