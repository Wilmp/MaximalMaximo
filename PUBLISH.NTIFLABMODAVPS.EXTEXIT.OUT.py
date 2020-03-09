from psdi.server import MXServer
from java.util import Date, Calendar

# Script created for jira story MAXIMO-1280
	
# Determine the current date and set the hour, minutes, seconds and miliseconds to zero.
calendar = Calendar.getInstance()
calendar.set(Calendar.HOUR_OF_DAY, 0)
calendar.set(Calendar.MINUTE, 0)
calendar.set(Calendar.SECOND, 0)
calendar.set(Calendar.MILLISECOND, 0)
currentdate = calendar.getTime()

# Retrieve the workdate from the incoming modavail mbo.
workdateOfRecord = irData.getCurrentMbo().getDate("WORKDATE")

# If the workdate is before today, we skip this transaction.
if workdateOfRecord.before(currentdate):
	errorgroup = "iface"
	errorkey = "SKIP_TRANSACTION"