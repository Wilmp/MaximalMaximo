from java.util import Date

if mbo.getString('STATUS')=='INACTIEF' and not mbo.getDate('PLUSASTOPDATE'):
    mbo.setValue('PLUSASTOPDATE', Date())