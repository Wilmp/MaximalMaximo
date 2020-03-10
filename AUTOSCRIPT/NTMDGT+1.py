from psdi.server import MXServer
from psdi.mbo import MboRemote
from psdi.mbo import MboSetRemote
from java.util import Date

mdgtSet=mbo.getMboSet('NTMDGT')
if not mdgtSet.isEmpty():
    mdgt= mdgtSet.moveFirst()
    mdgt.setValue('NEWREADING','1')
    mdgt.setValue('INSPECTOR','MAXADMIN')