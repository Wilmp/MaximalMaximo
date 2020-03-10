from sys import *
from java.io import *
from java.lang import System

strFile = "C:\\Temp\\"

strMbo = mbo.getName()
strFile +=strMbo
strFile +="\\"

if strMbo == "AUTOSCRIPT":
    strFile += mbo.getString("AUTOSCRIPT") 
    strFile += ".py"
elif strMbo == "REPORTDESIGN":
    strFile += mbo.getString("REPORTNAME")
elif strMbo == "MAXPRESENTATION":
    strFile += mbo.getString("APP") 
    strFile += ".xml"

filExport=File(None, strFile)

if filExport.createNewFile():
    System.out.println( "Created File: " + strFile)
writerExport=FileWriter(filExport)

if strMbo == "AUTOSCRIPT":
    writerExport.write(mbo.getString("SOURCE"))
elif strMbo == "REPORTDESIGN":
    writerExport.write(mbo.getString("DESIGN"))
elif strMbo == "MAXPRESENTATION":
    writerExport.write(mbo.getString("PRESENTATTION"))
    
writerExport.close()