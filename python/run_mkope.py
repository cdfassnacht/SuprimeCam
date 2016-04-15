import make_ope_2014a as mkope

srcinfo = mkope.init_src()

# HE0435
mkope.obs_wl(srcinfo,0,filtchange=False,reverse=False)
print ''
print '#----------------------------------------------------------------------'
print '#'
print '# Changing filter to g'
print ''
mkope.obs_phot(srcinfo,0,'g',filtchange=True,reverse=True)
print ''
print '#----------------------------------------------------------------------'
print '#'
print '# Changing filter to i'
print ''
mkope.obs_phot(srcinfo,0,'i',filtchange=True,reverse=False)

print '######################################################################'
print '######################################################################'

# STD_0924
mkope.obs_phot(srcinfo,4,'i',filtchange=False,reverse=True)
mkope.obs_phot(srcinfo,4,'r',filtchange=True,reverse=False)
mkope.obs_phot(srcinfo,4,'g',filtchange=True,reverse=True)

print '######################################################################'
print '######################################################################'

# HE1104 and RXJ1131
mkope.obs_phot(srcinfo,1,'i',filtchange=False,reverse=True)
print ''
print '#----------------------------------------------------------------------'
print '#'
print '# Changing sources to %s' % srcinfo.fullname[2]
print ''
mkope.obs_phot(srcinfo,2,'i',filtchange=False,reverse=False)
print ''
print '#----------------------------------------------------------------------'
print '#'
print '# Changing filter to r'
print ''
mkope.obs_wl(srcinfo,2,filtchange=True,reverse=True)
print ''
print '#----------------------------------------------------------------------'
print '#'
print '# Changing sources to %s' % srcinfo.fullname[1]
print ''
mkope.obs_wl(srcinfo,1,filtchange=False,reverse=False)
print ''
print '#----------------------------------------------------------------------'
print '#'
print '# Changing filter to g'
print ''
mkope.obs_phot(srcinfo,1,'g',filtchange=True,reverse=True)
print ''
print '#----------------------------------------------------------------------'
print '#'
print '# Changing sources to %s' % srcinfo.fullname[2]
print ''
mkope.obs_phot(srcinfo,2,'g',filtchange=False,reverse=False)

print '######################################################################'
print '######################################################################'

# B1608
mkope.obs_wl(srcinfo,3,filtchange=True,reverse=True)
print ''
print '#----------------------------------------------------------------------'
print ''
mkope.obs_phot(srcinfo,3,'g',filtchange=True,reverse=False)
print ''
print '#----------------------------------------------------------------------'
print ''
mkope.obs_phot(srcinfo,3,'i',filtchange=True,reverse=True)
