"""
Python code to create in a semi-automated way the text for the required
OPE file, which is used to control the telescope and camera for Subaru.
"""

import numpy as n

def init_src():
    """
    Initializes the structure containing the source info.
    """
    srcinfo = n.array([
            ('HE0435-1223','HE0435',043814.9,-121715.0,False),
            ('HE1104-1805','HE1104',110633.5,-182124.2,False),
            ('RXJ1131-1231','RXJ1131',113151.4,-123158.2,False),
            ('B1608+656','B1608',160914.0,+653228.0,False),
            ('Std_SDSS0924','Std0924',092455.9,+021924.9,True)
            ],
                      dtype=[('fullname','S12'), ('root','S7'), ('ra',float), 
                             ('dec',float), ('is_std',bool)]
                      )

    srcinfo = srcinfo.view(n.recarray)

    return srcinfo

#--------------------------------------------------------------------------

def write_src(srcinfo, index):
    """
    Given the index in the source array, creates the OPE source definition
    block.
    """

    """ Set the PA range"""
    if srcinfo.is_std[index]:
        pa = n.array([90,])
    else:
        pa = n.arange(30,165,15)

    """ Loop over the PA list, writing out a different 'source' for each PA """
    for i in pa:
        if i<0:
            pastr = 'm%2d' % (-1 * i)
        else:
            pastr = '%03d' % i
            
        if srcinfo.is_std[index]:
            sobj = '%s=OBJECT="%s"' % \
                (srcinfo.root[index],srcinfo.fullname[index])
        else:
            sobj = '%s_%s=OBJECT="%s"' % \
                (srcinfo.root[index],pastr,srcinfo.fullname[index])
        ra = 'RA=%08.1f' % srcinfo.ra[index]
        dec = 'DEC=%+08.1f' % srcinfo.dec[index]
        eqstr = 'EQUINOX=2000.0'
        instpa = 'INSROT_PA=%d' % i
        print '%s %s %s %s %s' % (sobj,ra,dec,eqstr,instpa)

#--------------------------------------------------------------------------

def obs_phot(srcinfo, index, band, filtchange=False, texp=120, reverse=False,
             dx=17, dy=23, autoguider=False):
    """
    Sets up and prints out the OPE commands for doing the observations in one
    of the photometric band setups (g or i).  This block of commands contains 
    three subblocks:
     1. Go to field and focus
     2. Take short exposures for astrometry and photometry
     3. Take longer exposures to build up a relatively deep image
    """

    """ Set up PA range """
    if reverse:
        pa = n.arange(150,0,-30)
        pa0str = '150'
    else:
        pa = n.arange(30,180,30)
        pa0str = '030'

    """ String setup """
    objstr_ng = '$DEF_IMAGE $%s_%s' % (srcinfo.root[index],pa0str)
    if autoguider:
        objstr = '$DEF_IMAGE_VGW $%s_%s' % (srcinfo.root[index],pa0str)
    else:
        objstr = '$DEF_IMAGE $%s_%s' % (srcinfo.root[index],pa0str)
    filtstr = 'Filter="W-S-%s+"' % band.upper()

    """ Generate focus sub-block """
    print ''
    if filtchange:
        print '# Change filter to %s and focus (%s)' % \
            (band,srcinfo.root[index])
        print 'FilterChange $DEF_SPCAM %s' % filtstr
    else:
        print '# Move to new object and focus (%s)' % srcinfo.root[index]
    print 'SetupField %s OFFSET_RA=0 OFFSET_DEC=0 %s' \
        % (objstr,filtstr)
    print 'FOCUSOBE %s EXPTIME=10 Z=7.10 DELTA_Z=0.05 DELTA_DEC=5 %s' \
        % (objstr_ng,filtstr)

    """ Generate short-exposure block """
    print ''
    print '# Take short exposures in %s so we can do astrometry and photometry'\
        % band
    print 'GetObject %s EXPTIME=3 OFFSET_RA=0 OFFSET_DEC=0 %s' \
        % (objstr,filtstr)
    print 'GetObject %s EXPTIME=30 OFFSET_RA=0 OFFSET_DEC=0 %s' \
        % (objstr,filtstr)

    """ Take deeper exposures for photo-z's"""
    expstr = 'EXPTIME=%d' % texp
    raoff = n.array([0,1,2,-1,-2])
    decoff = n.array([0,-2,1,2,-1])
    raoff *= dx
    decoff *= dy
    print ''
    print '# Take deeper exposures in %s to use for photo-z determination (%s)'\
        % (band,srcinfo.root[index])
    for i in range(pa.size):
        if pa[i]<0:
            pastr = 'm%2d' % (-1 * pa[i])
        else:
            pastr = '%03d' % pa[i]
        if autoguider:
            objstr = '$DEF_IMAGE_VGW $%s_%s' % (srcinfo.root[index],pastr)
        else:
            objstr = '$DEF_IMAGE $%s_%s' % (srcinfo.root[index],pastr)
        drastr  = 'OFFSET_RA=%d' % raoff[i]
        ddecstr = 'OFFSET_DEC=%d' % decoff[i]
        print 'SetupField %s %s %s %s' % (objstr,drastr,ddecstr,filtstr)
        print 'GetObject %s %s %s %s %s' % (objstr,expstr,drastr,ddecstr,filtstr)

#--------------------------------------------------------------------------

def obs_wl(srcinfo, index, band='r', filtchange=False, texp=300, reverse=False,
           dx=17, dy=23, autoguider=False):
    """
    Sets up and prints out the OPE commands for doing the observations in the
    weak lensing setup (r band).  This block of commands contains 
    three subblocks:
     1. Go to field and focus
     2. Take short exposures for astrometry and photometry
     3. Take longer exposures to build up a relatively deep image
    """

    """ Set up PA range """
    if reverse:
        pa = n.arange(135,15,-15)
        pa0str = '135'
    else:
        pa = n.arange(30,150,15)
        pa0str = '030'

    """ String setup """
    objstr_ng = '$DEF_IMAGE $%s_%s' % (srcinfo.root[index],pa0str)
    if autoguider:
        objstr = '$DEF_IMAGE_VGW $%s_%s' % (srcinfo.root[index],pa0str)
    else:
        objstr = '$DEF_IMAGE $%s_%s' % (srcinfo.root[index],pa0str)
    filtstr = 'Filter="W-S-%s+"' % band.upper()

    """ Generate focus sub-block """
    print ''
    if filtchange:
        print '# Change filter to %s and focus (%s)' % \
            (band,srcinfo.root[index])
        print 'FilterChange $DEF_SPCAM %s' % filtstr
    else:
        print '# Move to new object and focus (%s)' % srcinfo.root[index]
    print 'SetupField %s OFFSET_RA=0 OFFSET_DEC=0 %s' \
        % (objstr,filtstr)
    print 'FOCUSOBE %s EXPTIME=10 Z=7.10 DELTA_Z=0.05 DELTA_DEC=5 %s' \
        % (objstr_ng,filtstr)

    """ Generate short-exposure block """
    print ''
    print '# Take short exposures in %s so we can do astrometry and photometry'\
        % band
    print 'GetObject %s EXPTIME=3 OFFSET_RA=0 OFFSET_DEC=0 %s' \
        % (objstr,filtstr)
    print 'GetObject %s EXPTIME=30 OFFSET_RA=0 OFFSET_DEC=0 %s' \
        % (objstr,filtstr)

    """ Take deeper exposures for photo-z's"""
    expstr = 'EXPTIME=%d' % texp
    raoff = n.array([0,1,2,-1,-2,3,-3,-3])
    decoff = n.array([0,-2,1,2,-1,1,-2,2])
    raoff *= dx
    decoff *= dy
    print ''
    print '# Take deeper exposures in %s to use for weak lensing (%s)'\
        % (band,srcinfo.root[index])
    for i in range(pa.size):
        if pa[i]<0:
            pastr = 'm%2d' % (-1 * pa[i])
        else:
            pastr = '%03d' % pa[i]
        if autoguider:
            objstr = '$DEF_IMAGE_VGW $%s_%s' % (srcinfo.root[index],pastr)
        else:
            objstr = '$DEF_IMAGE $%s_%s' % (srcinfo.root[index],pastr)
        drastr  = 'OFFSET_RA=%d' % raoff[i]
        ddecstr = 'OFFSET_DEC=%d' % decoff[i]
        print 'SetupField %s %s %s %s' % (objstr,drastr,ddecstr,filtstr)
        print 'GetObject %s %s %s %s %s' % (objstr,expstr,drastr,ddecstr,filtstr)
        drastr  = 'OFFSET_RA=%d' % (raoff[i] + dx)
        ddecstr = 'OFFSET_DEC=%d' % (decoff[i] - dy)
        print 'SetupField %s %s %s %s' % (objstr,drastr,ddecstr,filtstr)
        print 'GetObject %s %s %s %s %s' % (objstr,expstr,drastr,ddecstr,filtstr)
