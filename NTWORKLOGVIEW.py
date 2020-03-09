from psdi.server import MXServer

mbo.setValue("MODIFYBY", "MAXADMIN")
mbo.setValue("MODIFYDATE", MXServer.getMXServer().getDate())