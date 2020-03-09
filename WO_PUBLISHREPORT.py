from java.util import Calendar
from java.util import Date
from psdi.app.report import ReportUtil
from psdi.server import MXServer
from psdi.mbo import MboConstants, Mbo, MboRemote, MboSet, MboSetRemote, SqlFormat
from java.lang import StringBuilder

# Required functions, do not alter
emailfiletype = 'PDF'
emailtype = 'attach'
paramdelimiter = '||'
paramstring = 'appHierarchy=NTPLUSAWO'

assetSet=mbo.getMboSet("ASSET")
if assetSet is not None:
    asset=assetSet.moveFirst()
    serialnum=asset.getString("SERIALNUM")
    if asset.getString("NTSERIE")=='TRAXX-LOC' and asset.getString("ASSETTYPE") in ["EENHEID","LOC"]:
        pmwoSet=mbo.getMboSet("NTPMWO")
        pmwo=pmwoSet.moveFirst()
        if pmwo is not None:
            # DPWS Set variables
            emailsubject = 'Onderhoud Traxx voor: ' + serialnum + ', BWO: ' + mbo.getString("WONUM") + ', ' + mbo.getString("DESCRIPTION") #Text for email subject
            reportname = 'nt_traxx_onderhoud.rptdesign' # BIRT report name to send

            #property opgezet om de url die de browser gebruikt op te halen
            cfgData=MXServer.getMXServer().getConfig()
            maximourl=cfgData.getProperty("nt.browser.url")

            #rapport moet naar nsr.vloot@ns.nl
            personSet=mbo.getMboSet("NSR_VLOOT")
            if personSet is not None:
                person=personSet.moveFirst()
                emailto=person.getString("PRIMARYEMAIL")
            else:
                emailto = "centraalsupportmaximo.ovm@ns.nl"

            emailcomments = StringBuilder() # Body of the email text
            emailcomments.append('<br><p style="font-family:Calibri">This email is automatically generatated by Maximo.<br>')
            emailcomments.append('<br>Please do not reply to this message.<br>')
            emailcomments.append('</p>')

            # set a schedule for the report
            c = Calendar.getInstance()

            # add 120 seconds to current time to allow preparing REPORTSCHED cron task instance
            c.add(Calendar.SECOND,120)
            d = c.getTime()
            thiswoset = mbo.getThisMboSet()
            if thiswoset is not None:
                    locale = thiswoset.getClientLocale()
                    userinfo = thiswoset.getUserInfo()
            schedule = ReportUtil.convertOnceToSchedule(d,locale,c.getTimeZone())

            #SChedule van een rapport gaat niet via normale acties, vandaar NOACCESSCHECK en NOVALIDATION_AND_NOACTION
            #Tabellen REPORTSCHED, Crontaskinstance en Crotaskparam moeten worden gevuld. Reportparam is input.
            if schedule is not None:
                reportschedset = MXServer.getMXServer().getMboSet("REPORTSCHED",userinfo)
                if reportschedset is not None:
                    print "Obtained REPORTSCHED set"
                    reportsched = reportschedset.add()
                    reportsched.setValue("REPORTNAME",reportname)
                    reportsched.setValue("appname",app)
                    reportsched.setValue("USERID",userinfo.getUserName(),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) # To run as current logged in user
                    reportsched.setValue("TYPE","once")
                    reportsched.setValue("EMAILTYPE",emailtype)
                    reportsched.setValue("MAXIMOURL",maximourl)#.toString())
                    reportsched.setValue("EMAILUSERS",emailto)
                    reportsched.setValue("EMAILSUBJECT",emailsubject)
                    reportsched.setValue("EMAILCOMMENTS",emailcomments.toString())
                    reportsched.setValue("EMAILFILETYPE",emailfiletype)
                    reportsched.setValue("COUNTRY",locale.getCountry())
                    reportsched.setValue("LANGUAGE",locale.getLanguage())
                    reportsched.setValue("VARIANT",locale.getVariant())
                    reportsched.setValue("TIMEZONE",thiswoset.getClientTimeZone().getID())
                    reportsched.setValue("LANGCODE",userinfo.getLangCode())
                    print "About to work with REPORTSCHEDULE cron task"
                    crontaskdef = reportsched.getMboSet("$parent","crontaskdef","crontaskname='REPORTSCHEDULE'").getMbo(0)
                    if crontaskdef is not None:
                        crontaskinstset = crontaskdef.getMboSet("CRONTASKINSTANCE")
                        if crontaskinstset is not None:
                            print "About to work with Cron task instance of REPORTSCHEDULE cron task"
                            crontaskinst = crontaskinstset.add(MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                            if crontaskinst is not None:
                                d = Date()
                                crontaskinstname = str(d.getTime())
                                crontaskinst.setValue("CRONTASKNAME","REPORTSCHEDULE",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                crontaskinst.setValue("INSTANCENAME",crontaskinstname,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                crontaskinst.setValue("SCHEDULE",schedule,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                crontaskinst.setValue("ACTIVE",1,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                crontaskinst.setValue("RUNASUSERID",userinfo.getUserName(),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                crontaskinst.setValue("HASLD",0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                crontaskinst.setValue("AUTOREMOVAL",True,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                print "have set all cron task instance values for REPORTSCHEDULE cron task"
                    reportsched.setValue("CRONTASKNAME",crontaskinst.getString("CRONTASKNAME"))
                    reportsched.setValue("INSTANCENAME",crontaskinst.getString("INSTANCENAME"))
                    print "Now going to work with Cron task PARAMETERS"
                    cronparamset = crontaskinst.getMboSet("PARAMETER")
                    if cronparamset is not None:
                        sqf = SqlFormat(cronparamset.getUserInfo(),"reportname=:1")
                        sqf.setObject(1,"REPORTPARAM","REPORTNAME",reportname)
                        reportparamset = MXServer.getMXServer().getMboSet("REPORTPARAM",cronparamset.getUserInfo())
                        if reportparamset is not None:
                            print "working with REPORTPARAM mbo set"
                            reportparamset.setWhere(sqf.format())
                            reportparamset.reset()
                            i=reportparamset.count()
                            reportparammbo = None
                            for j in range(i):
                                reportparam = reportparamset.getMbo(j)
                                cronparam = cronparamset.add(MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                if cronparam is not None:
                                    print "going to copy values from REPORTPARAM into CRONTASKPARAM"
                                    cronparam.setValue("CRONTASKNAME","REPORTSCHEDULE",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                    cronparam.setValue("INSTANCENAME",crontaskinstname,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                    cronparam.setValue("CRONTASKNAME","REPORTSCHEDULE",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                    paramname = reportparam.getString("PARAMNAME")
                                    cronparam.setValue("PARAMETER",paramname,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                    if paramname=="where":
                                        cronparam.setValue("VALUE","1=1",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                    elif paramname=="paramstring":
                                        print 'If condition for paramstring'
                                        cronparam.setValue("VALUE",paramstring,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                    elif paramname=="paramdelimiter":
                                        print 'If condition for paramdelimiter'
                                        cronparam.setValue("VALUE",paramdelimiter,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                    elif paramname=="appname":
                                        cronparam.setValue("VALUE",app,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                    elif paramname=="ancestor":
                                        cronparam.setValue("VALUE",mbo.getString("WONUM"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                    else:
                                        continue
                    reportschedset.save()