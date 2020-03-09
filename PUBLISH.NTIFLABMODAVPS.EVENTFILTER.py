from psdi.server import MXServer
from psdi.mbo import MboConstants
from psdi.util.logging import MXLoggerFactory
from java.util import Date, Calendar

logger = MXLoggerFactory.getLogger("maximo.script.autoscript")

# Retrieve the workdate from the incoming modavail mbo.
workdateOfRecord = mbo.getDate("WORKDATE")
workDateCalendar = Calendar.getInstance()
workDateCalendar.setTime(workdateOfRecord)

year = workDateCalendar.get(Calendar.YEAR)
month = workDateCalendar.get(Calendar.MONTH)
dayOfMonth = workDateCalendar.get(Calendar.DAY_OF_MONTH)

# Function created for jira story MAXIMO-1080
# The interface NTIFLABMODAVPS sent incorrect time values for the fields 'Start time' and 'End time'. 
# This was due to the incorrect calculation of daylight savings time caused by the fields being saved as a date-time fields with 1970-01-01 as the date-part. 
# Daylight savings time did not exist in 1970 in the Netherlands, causing the incorrect calculation.
# We will add the work date to the date-time fields 'Start time' and 'End time' to fix this problem.
def adjustTimesForDaylightSavings():

	logger.info("Automation script PUBLISH.NTIFLABMODAVPS.EVENTFILTER: Updating the date-part of start and end time to the date of attribute 'workdate' to adjust for problems in daylight savings time determination.")
	updateDateTimeToWorkDate("STARTTIME")
	updateDateTimeToWorkDate("ENDTIME")

def updateDateTimeToWorkDate(dateTimeString):
	dateTime = mbo.getDate(dateTimeString)
	calendar = Calendar.getInstance()
	calendar.setTime(dateTime)
	calendar.set(Calendar.YEAR, year)
	calendar.set(Calendar.MONTH, month)
	calendar.set(Calendar.DAY_OF_MONTH, dayOfMonth)
	
	mbo.setValue(dateTimeString, calendar.getTime(), MboConstants.NOACCESSCHECK)

adjustTimesForDaylightSavings()