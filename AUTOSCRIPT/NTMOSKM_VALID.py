mosreadingSet=mbo.getMboSet('NTMOSREADINGSTOVALIDATE')
if not mosreadingSet.isEmpty():
    mosread = mosreadingSet.moveFirst()
    while mosread:
        mosread.setValue('VALID',True)
        mosread=mosreadingSet.moveNext()