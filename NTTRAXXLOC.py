#Bij uitbouw van een Traxx-loc met open SA uit een sandwichstam wordt een mail verstuurd naar het MBN

from psdi.util.logging import MXLoggerFactory

try:
    commTemplateSet = mbo.getMboSet("$commtemp","COMMTEMPLATE","TEMPLATEID ='NTTRAXXLOC'")
    commTemplate = commTemplateSet.getMbo(0)
    if commTemplate==None:
        print("Automationscript NTTRAXXLOC kon communicatietemplate NTTRAXXLOC niet vinden")
    else:
        commTemplate.sendMessage(mbo)
except:
    myLogger = MXLoggerFactory.getLogger("maximo.script.autoscript")
    myLogger.error("Fout opgetreden bij uitvoeren automationscript NTTRAXXLOC")