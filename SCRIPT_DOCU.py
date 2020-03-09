from sys import *
from java.io import *
from java.lang import System

strFile = "C:\\Temp\\"

strFile += mbo.getString("AUTOSCRIPT") 

strFile += ".py"

filExport=File(None, strFile)

if filExport.createNewFile():
    System.out.println( "Created File: " + strFile)
writerExport=FileWriter(filExport)
writerExport.write(mbo.getString("SOURCE"))
writerExport.close()