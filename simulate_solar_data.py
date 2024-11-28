import h5py
import numpy as np
from astropy.io import fits
from casatools import image,simulator,measures,quanta
import os
from scipy.ndimage import zoom
import matplotlib.pyplot as plt

def makeimage(ra,dec,freq,cell,flux,imagename='sim_onepoint_true.im'):  
	'''
	ra dec is center of image. Give in radians
	freq in GHz
	cell : e.g. '2arcsec'
	'''
	flux1=flux
	shape=np.shape(flux1)
	qa=quanta()
	ia=image()
	## Make the image from a shape
	ia.close()
	ia.fromshape(imagename,[shape[0],shape[1],1,1],overwrite=True)
	## Make a coordinate system
	cs=ia.coordsys()
	cs.setunits(['rad','rad','','Hz'])
	print (cell)
	cell_rad=qa.convert(qa.quantity(str(cell)+"arcsec"),"rad")['value']
	cs.setincrement([-cell_rad,cell_rad],'direction')
	print (ra,dec)
	#cs.setreferencevalue([ra,dec],type="direction")
	cs.setreferencevalue([qa.convert(ra,'rad')['value'],qa.convert(dec,'rad')['value']],type="direction")
	cs.setreferencevalue(str(freq)+'GHz','spectral')
	cs.setreferencepixel([0],'spectral')
	cs.setincrement('0.001GHz','spectral')
	## Set the coordinate system in the image
	ia.setcoordsys(cs.torecord())
	ia.setbrightnessunit("Jy/pixel")
	ia.set(0.0)
	ia.close()
	
	
	ia.open(imagename)
	data=ia.getchunk()
	data[:,:,0,0]=flux1.T
	#plt.imshow(flux1);plt.colorbar();plt.show()
	ia.putchunk(data)
	ia.close()
	


def generate_ms(config_file,solar_model,source_ra,source_dec,reftime,integration_time=60,msname='MeerKAT.ms',duration=None):
	'''
	config_file: Antenna configuration file in standard format. 
		     First column: x
		     Second COlumn:y
		     Third Column: z
		     Fourth column: dish diameter
		     Fifth column: Antenna name
	spws:  Frequencies of the spws
	source_ra, source_dec: ra, dec of phasecenter in radians
	reftime: Reference time of observation in CASA format. in UTC 
	integration_time: in seconds
	duration: in seconds
	'''
	sm=simulator()
	me=measures()
	sm.open(msname)
	ia=image()
	antenna_params=np.genfromtxt(config_file,usecols=(0,1,2))
	#ant_names=np.genfromtxt(config_file,usecols=(4))
	x=antenna_params[:,0]
	y=antenna_params[:,1]
	z=antenna_params[:,2]
	dish_dia=13.5*np.ones(len(x))
	
	hf=h5py.File(solar_model)
	spws=np.array(hf['frequency'])
	flux=np.array(hf['flux_jy'])
	cell=hf.attrs['cdelt1']*8
	print (cell)
	cont=input('?')
	hf.close()
	
	sm.setconfig(telescopename="MeerKAT",x=x,y=y,z=z,dishdiameter=dish_dia,\
		mount='ALT-AZ',coordsystem='local',referencelocation=me.observatory('MeerKAT'))
	
	num_spw=np.size(spws)
	for i in range(0,num_spw):
		sm.setspwindow(spwname='Band'+str(i),freq=str(spws[i])+"GHz",deltafreq='1MHz',\
			freqresolution='1MHz',nchannels=1,stokes='RR LL')
		
	sm.setfeed('perfect R L')
	sm.setfield(sourcename='Sun',sourcedirection=['J2000',str(source_ra)+"rad",str(source_dec)+"rad"])
	sm.setauto(autocorrwt=0.0)
	sm.settimes(integrationtime=str(integration_time)+"s",referencetime=me.epoch('UTC',reftime),usehourangle=False)
	
	if duration==None:
		duration=integration_time
	
	starttime=str(-duration/2)+"s"
	endtime=str(duration/2)+"s"
	for i in range(0,num_spw):
		sm.observe("Sun","Band"+str(i),starttime=starttime,stoptime=endtime)
		
	for i in range(0,num_spw):
		sm.setdata(spwid=i)
		os.system("rm -rf solar_image.model")
		makeimage(source_ra,source_dec,spws[i],cell,flux[:,:,i],imagename='solar_image.model')
		#make_empty_sky_model_image(msname,imagename_prefix='solar_image',calculate_imsize=True,FWHM=True,use_wsclean=False,full_stokes=False)
		flux1=flux[:,:,i].T
		shape=np.shape(flux1)
		ia.open('solar_image.model')
		data=ia.getchunk()
		cent_pix=int(data.shape[0]/2)
		cent_pix1=int(flux1.shape[0]/2)
		print (data.shape,flux1.shape)
		data[cent_pix-600:cent_pix+600,cent_pix-600:cent_pix+600,0,0]=flux1[cent_pix1-600:cent_pix1+600,cent_pix1-600:cent_pix1+600]
		#plt.imshow(flux1);plt.colorbar();plt.show()
		ia.putchunk(data)
		ia.close()
		sm.predict(imagename='solar_image.model')
		#os.system("rm -rf solar_image.model")
	sm.close()

### taking solar coords from meerkat data of same day. 
solar_ra=np.deg2rad(44.66)
solar_dec=np.deg2rad(+16.49)

solar_model='synthetic_free_free_data_meerkat_20240509_0825.hdf5'
config_file='meerkat.config'



reftime='2024/05/09/08:25:00'
duration=60
msname='meerkat_20240509_0825_lband.ms'

generate_ms(config_file,solar_model,solar_ra,solar_dec,reftime,msname=msname)



