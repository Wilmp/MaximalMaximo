strDay=mbo.getString('NTWEEKDAY')
intDay=0
if strDay=='MAANDAG':
    intDay=1
elif strDay=='DINSDAG':
    intDay=2
elif strDay=='WOENSDAG':
    intday=3
elif strDay=='DONDERDAG':
    intday=4
elif strDay=='VRIJDAG':
    intday=5
elif strDay=='ZATERDAG':
    intday=6
else:
    intDay=7
mbo.setValue('NTDAGNUMMER', intDay)