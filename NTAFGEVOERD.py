from psdi.util.logging import MXLoggerFactory

try:
    commTemplateSet = mbo.getMboSet("$commtemp","COMMTEMPLATE","TEMPLATEID ='NTAFGEVOERD'")
    commTemplate = commTemplateSet.getMbo(0)
    if commTemplate==None:
        print("Automationscript NTAFGEVOERD kon communicatietemplate NTAFGEVOERD niet vinden")
    else:
        commTemplate.sendMessage(mbo)
except:
    myLogger = MXLoggerFactory.getLogger("maximo.script.autoscript")
    myLogger.error("Fout opgetreden bij uitvoeren automationscript NTAFGEVOERD")