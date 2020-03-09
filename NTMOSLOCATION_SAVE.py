from java.util import Calendar
from java.util import Date
from psdi.mbo import MboRemote
from psdi.mbo import MboSetRemote
from psdi.mbo import SqlFormat
from java.util import GregorianCalendar

WEEKDAYS =  ["ZONDAG","MAANDAG", "DINSDAG", "WOENSDAG", "DONDERDAG", "VRIJDAG", "ZATERDAG"]
cal=Calendar.getInstance()
cal.setTime(mbo.getDate('STARTDATE'))
destMboSet = mbo.getMboSet("NTPLANARRIVAL")
if not destMboSet.isEmpty():
    destMboSet.deleteAll()
for x in range(7):
    if x>0:
        cal.add(Calendar.DATE,1)
    weekday=WEEKDAYS[ cal.get( Calendar.DAY_OF_WEEK )-1]
    headerMboSet = mbo.getMboSet("NTPLANHEADER")
    sqf = SqlFormat("ntday = :1 and ntvalidfrom <= :2 and :2 <= ntvalidto")
    sqf.setObject(1, "NTPLANHEADER", "NTDAY", weekday)
    sqf.setDate(2, cal.getTime())
    headerMboSet.setWhere(sqf.format())
    headerMboSet.reset()
    if not headerMboSet.isEmpty():
        headerMbo = headerMboSet.moveFirst()
        sourceMboSet = headerMbo.getMboSet("NTPLANSCHEDULE");
        if not sourceMboSet.isEmpty():
            sourceMbo=sourceMboSet.moveFirst()
            while sourceMbo:
                destMbo = destMboSet.add()
                destMbo.setValue("LOCATION", sourceMbo.getString("LOCATION"))
                destMbo.setValue("NTARRTRACK", sourceMbo.getString("NTARRTRACK"))

                destMbo.setValue("NTDEPTRACK", sourceMbo.getString("NTDEPTRACK"))
                destMbo.setValue("NTNSRSERIE", sourceMbo.getString("NTNSRSERIE"))
                destMbo.setValue("NTSERIE", sourceMbo.getString("NTSERIE"))                
                destMbo.setValue("NTPARTSERIE", sourceMbo.getString("NTPARTSERIE")) 
                destMbo.setValue("NTNSRMODEL", sourceMbo.getString("NTNSRMODEL"))
                
                destMbo.setValue("NTSTATION", sourceMbo.getString("NTSTATION"))

                destMbo.setValue("NTTRAINNR", sourceMbo.getString("NTTRAINNR"))
                destMbo.setValue("NTPOSITION", sourceMbo.getString("NTPOSITION"))
                
                maintarrdate=Calendar.getInstance()
                maintarrdate.setTime(cal.getTime())
                if sourceMbo.getInt("NTARROFFSET")>0:
                    maintarrdate.add(Calendar.DATE,sourceMbo.getInt("NTARROFFSET"))
                destMbo.setValue("NTMAINTARRDATE", maintarrdate.getTime())
                destMbo.setValue("NTMAINTARRTIME", sourceMbo.getString("NTMAINTARRTIME"))
                
                destMbo.setValue("NTTRAINDEP", sourceMbo.getString("NTTRAINDEP"))
                destMbo.setValue("NTPOSITIONDEP", sourceMbo.getString("NTPOSITIONDEP"))
                
                maintdepdate=Calendar.getInstance()
                maintdepdate.setTime(cal.getTime())
                if sourceMbo.getInt("NTDEPOFFSET")>0:
                    maintdepdate.add(Calendar.DATE,sourceMbo.getInt("NTDEPOFFSET"))
                destMbo.setValue("NTMAINTDEPDATE", maintdepdate.getTime())
                destMbo.setValue("NTMAINTDEPTIME", sourceMbo.getString("NTMAINTDEPTIME"))
    
                destMbo.setValue("NTWEEKDAY", weekday)
                destMbo.setValue("ORGID", sourceMbo.getString("ORGID"))
                destMbo.setValue("SITEID", sourceMbo.getString("SITEID"))

                sourceMbo=sourceMboSet.moveNext()