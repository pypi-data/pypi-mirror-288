import numpy as np
import numpy.random as rand
from astropy.io import fits
from pathlib import Path
from scipy import interpolate
import matplotlib.pyplot as plt
import h5py
from scipy.signal import find_peaks

from spiakid_simulation.new_version.fun.PSF.turbulence import PSF_creation, PSF_creation_mult
from spiakid_simulation.new_version.fun.DataReading import data_check
from spiakid_simulation.new_version.fun.Photon.sim_image_photon import photon, photon_pos_on_PSF, photon_proj, detector_scale, photon_calib
from spiakid_simulation.new_version.fun.Rot.rot import EarthRotation

from spiakid_simulation.new_version.fun.Phase.phase_conversion import read_csv, photon2phase, exp_adding, PhaseNoise,  ConversionTab
from spiakid_simulation.new_version.fun.Calibration.Calib import exp_adding_calib , PhaseNoiseCalib, ConversionTabCalib, Photon2PhaseCalib
from spiakid_simulation.new_version.fun.Filter.filter import PSD, Template, FilterCreation

from spiakid_simulation.new_version.fun.output.HDF5_creation import recursively_save_dict_contents_to_group

class Simulation():


    def __init__(self,file ):
        
        global DATA
        DATA = data_check(file)

        global path
        path = DATA['sim_file']

        global phgen
        phgen = DATA['Photon_Generation']

        global telescope
        telescope = phgen['telescope']
        global exptime 
        exptime = telescope['exposition_time']
        global diameter 
        diameter = telescope['diameter']
        global obscuration
        obscuration = telescope['obscuration']
        global latitude
        latitude = telescope['latitude'] * np.pi / 180 
        global transmittance
        transmittance = telescope['transmittance']
        global pxnbr
        pxnbr = telescope['detector']['pix_nbr']
        global pxsize 
        pxsize = telescope['detector']['pix_size']
        global baseline
        baseline =  telescope['detector']['baseline']

        st = phgen['star']
        global stnbr 
        stnbr = st['number']
        global stdistmin
        stdistmin = st['distance']['min']
        global stdistmax
        stdistmax = st['distance']['max']
        global wv
        wv = np.linspace(st['wavelength_array']['min'],
                        st['wavelength_array']['max'],
                        st['wavelength_array']['nbr'])
        global spectrum 
        spectrum = st['spectrum_folder']

        sky = phgen['sky']
        global skymethod 
        skymethod = sky['method']
        global contamination
        contamination = sky['contamination']
        global rotation
        rotation = sky['rotation']
        global fovmethod 
        fovmethod = sky['fov_method']
        global altguide 
        altguide = sky['guide']['alt'] * np.pi / 180 
        global azguide 
        azguide = sky['guide']['az'] * np.pi / 180 
        
        global timelinestep 
        timelinestep = DATA['Timeline']['point_nb']

  
        global spectrumlist 
        spectrumlist = []
        files = Path(spectrum).glob('*')
        for i in files:
            spectrumlist.append(i)

        
        

        try: DATA['Phase']
        except: pass
        else:
            global calibfile
            calibfile = DATA['Phase']['Calib_File']
            global conversion
            conversion = read_csv(calibfile)
            global nphase
            nphase = DATA['Phase']['Phase_Noise']
            global decay
            decay = - DATA['Phase']['Decay']
            global nreadoutscale
            nreadoutscale = DATA['Phase']['Readout_Noise']['scale']
            global nreadouttype
            nreadouttype = DATA['Phase']['Readout_Noise']['noise_type']

            

            global nperseg
            nperseg = DATA['Electronic']['nperseg']

            global templatetime
            templatetime = DATA['Electronic']['template_time']
            
            global trigerinx
            trigerinx = DATA['Electronic']['trigerinx']

            global pointnb
            pointnb = DATA['Electronic']['point_nb']




            self.detect = self.Detector()

        self.psf = self.PSF()

        self.stars = {}

        for i in range(0, stnbr):
            print('star %i'%i)
            self.stars['star_'+str(i)] = self.Star(self.psf)

        try: DATA['Phase']
        except: pass
        else:
            self.stars['Detector'] = self.PhotonDetection(self.stars)

        self.Output(DATA['Output']['save'])
   
    class PSF():

            def __init__(self):

        
                try: phgen['PSF']
                except:
                        self.gaussian_psf(pxnbr=pxnbr, pxsize=pxsize, wv=wv)
                else:
                        psf = phgen['PSF']
                        psfmeth = psf['method']
                        psffile = psf['file']
                        try: psfmeth == 'Download'
                        except:
                            self.defined_psf(psf=psf,psffile=psffile, wv=wv, diameter=diameter,
                                            obscuration=obscuration,exptime=exptime)
                        else:
                            file = fits.open(psffile)[0]
                            self.psf = file.data
                            list_axis = [file.header['NAXIS1'],file.header['NAXIS2'],file.header['NAXIS3']]
                            if (list_axis.count(file.header['NAXIS1']) == 2)  and (file.header['CUNIT1'] == 'arcsec'):
                                self.psfpxnbr = file.header['NAXIS1']
                                self.psfsize = self.psfpxnbr * file.header['CDELT1']
                            else:
                                if file.header['CUNIT2'] == 'arcsec':
                                    self.psfpxnbr =file.header['NAXIS2']
                                    self.psfsize = self.psfpxnbr * file.header['CDELT2']


                # Create a minimum of intensity on the psf to place a photon
                self.psfenergy = np.zeros(shape = np.shape(wv), dtype = object)
                self.psfpos = np.zeros(shape = np.shape(wv), dtype = object)
                self.maxpsf = []
         
                for wvl in range(len(wv)):
                    self.maxpsf.append(1.1 * np.max(self.psf[wvl]))
                    self.psfpos[wvl]  = []
                    self.psfenergy[wvl] = []
                    lim = np.max(self.psf[wvl])/100
                    data  = self.psf[wvl]
                    for i in range(self.psfpxnbr):
                        for j in range(self.psfpxnbr):
                            if self.psf[wvl][i,j]> lim: 
                                self.psfpos[wvl].append([i,j])
                                self.psfenergy[wvl].append(data[i,j])

                    

            def gaussian_psf(self, pxnbr, pxsize, wv):
                self.psfpxnbr = pxnbr
                psf_grid = np.zeros(shape = (pxnbr,pxnbr,len(wv)))
                psf_grid[int(pxnbr/2),int(pxnbr/2),:] = 1
                    # point = np.linspace(0,1,pix_nbr)
                    # psf = interpolate.RegularGridInterpolator((point,point,wavelength_array),psf_grid)
                    # psf_pix_nbr = pix_nbr
                self.psfsize = pxsize * pxnbr
                self.psf = psf_grid
             

            def defined_psf(self, psf, psffile, wv, diameter, obscuration, exptime):
                self.psfpxnbr = psf['pix_nbr']
                self.psfsize = psf['size']
                seeing = psf['seeing']
                wind = psf['wind']
                L0 = psf['L0']

                if type[wind] == list:
                    coeff = psf['coeff']
                    self.psf = PSF_creation_mult(fov_tot=self.psfsize, nb_pixels_img=self.psfpxnbr,
                                                wavelength_array=wv, seeing=seeing, wind=wind,
                                                D=diameter, obscuration=obscuration, L0=L0,
                                                obs_time=exptime, coeff=coeff,save_link=psffile)
                else:
                    self.psf = PSF_creation(fov_tot=self.psfsize, nb_pixels_img=self.psfpxnbr,
                                            wavelength_array=wv, seeing=seeing, wind=wind,
                                            D=diameter, obscuration=obscuration, L0=L0,
                                            obs_time=exptime, save_link=psffile)

    class Star():

            def __init__(self, psf):
                
                self.posx  = rand.uniform(low =int(0), high= int(pxnbr))
                self.posy  = rand.uniform(low =int(0), high= int(pxnbr))
                print(self.posx,self.posy)
                self.spectrumchoice = np.loadtxt(spectrumlist[rand.randint(len(spectrumlist))])
                self.spectrumchoice = interpolate.interp1d(self.spectrumchoice[:,0],self.spectrumchoice[:,1])
                self.stardist = rand.uniform(stdistmin, stdistmax)
                self.starintensity = 1 * (10 / self.stardist**2)
                self.spectrum = (10 /self.stardist**2) * self.spectrumchoice(wv*10**3)

                rot, evalt = self.Rotation()
                self.PhotonCreation()
                self.PSFDistribution(psf)
                self.PhotonProj(psf, rot,evalt)
                photondetect = self.DetectorProj()
                

                try: DATA['Phase']
                except: pass
                else:
                    # self.Calib()
                    phaseconv = self.PhaseConversion(photondetect)
                    expphase = self.PhaseExp(phaseconv)
                    nexpphase = self.PhaseExpNoise(expphase)
                    self.phase = np.zeros(shape = (pxnbr, pxnbr), dtype = object)
                    for i in range(0, pxnbr):
                        for j in range(0, pxnbr):
                            self.phase[i,j] = []
                            for ph in range(0, len(nexpphase[0][i,j])):
                                self.phase[i,j].append([nexpphase[1][i,j][ph],nexpphase[0][i,j][ph]])


            def Rotation(self):
                print('Rot')
                if rotation == True:
                
                    # print('Earth rotation effect')
                    guide = [altguide,azguide]

                    rot,evalt,self.alt_az_t,self.ra_dec_t,self.ang = EarthRotation(lat_tel=latitude,coo_guide=guide,coo_star=[self.posx, self.posy],time = exptime,size=pxnbr)

                else:
                    t = np.linspace(0,exptime,exptime+1 )
                    rot = [interpolate.interp1d([0,exptime],[self.posx,self.posy]),
                                interpolate.interp1d([0,exptime],[t,t])]
                    evalt = interpolate.interp1d([0,exptime],[np.pi/2,np.pi/2])
                    self.alt_az_t =[altguide,azguide,0]
                    self.ra_dec_t = [0,0,0]
                    self.ang = 0
                return(rot, evalt)
            
            def PhotonCreation(self,):
                print('photon creation')
                # dict with [wavelength (µm), time (µs)]
                self.photon = photon(wavelength=wv, spectre=self.spectrum, time=exptime,
                                    diam=diameter, point_nb=timelinestep, transmission=transmittance)
                print(len(self.photon))

            def PSFDistribution(self,psf):
                print('PSFed')
                self.photonPSF = photon_pos_on_PSF(self.photon, psf, wv)

            def PhotonProj(self,psf, rot, evalt):
                print('photon pos on detector frame + rot')
                lam0 = (max(wv)+min(wv))/2
                self.detectpos = photon_proj(self.photonPSF, psf, rot,evalt, pxnbr, pxsize, lam0, timelinestep)

            def DetectorProj(self,):
                print('Detector projection')
                # [Wavelength[pix,pix], Time[pix,pix]]
                photondetect = detector_scale(pxnbr, self.detectpos)
                return(photondetect)

            def PhaseConversion(self,photondetect):
                print('Phase conversion')
                convtab = ConversionTab(photondetect,conversion)
                phaseconv = photon2phase(photondetect,convtab, nphase)
                return(phaseconv)
                
            def PhaseExp(self,phaseconv):
                print('Phase exp')
                expphase = exp_adding(phaseconv, decay, exptime)
                return(expphase)
        
            def PhaseExpNoise(self, expphase):
                #   [Wavelength[pix,pix][list],Time[pix,pix]]
                print('Phase Exp Noise')
   
                nexpphase = PhaseNoise(expphase, nreadoutscale)
                return(nexpphase)
                
    class Detector():
        
        def __init__(self,):

            test = 0
            print('Detector part')
            self.pixfilter = np.zeros(shape = (pxnbr,pxnbr), dtype = object)
           
            self.psd = np.zeros(shape = (pxnbr,pxnbr), dtype = object)
            self.template = np.zeros(shape = (pxnbr,pxnbr), dtype = object)
            self.noisetimeline = np.zeros(shape = (pxnbr,pxnbr), dtype = object)
            self.Calib()
            print('Filter creation')
            for i in range(pxnbr):
                for j in range(pxnbr):
                    self.noisetimeline[i,j] = [np.linspace(0,int(1e6),int(1e6)),np.random.normal(scale=nreadoutscale, loc = 0, size = int(1e6))]

                    self.Filter(self.noisetimeline[i,j], i, j)
      

        def Filter(self, noise, i, j):
            #  Filter creation
            self.psd[i,j] = PSD(noise, nperseg)

            self.template[i,j] = Template(decay, templatetime, trigerinx, pointnb)

            self.pixfilter[i,j] = FilterCreation(self.template[i,j], self.psd[i,j][1])

        def Calib(self,):
                print('Calibration', flush = True)
                # 3 list, each contain 1 detector with calibration on all pix
                wvcalib = np.linspace(wv[0],wv[-1],3)
                self.photondetectcalib = photon_calib(pxnbr, wvcalib)
                print('Tab creation', flush = True)
                tab = ConversionTabCalib(self.photondetectcalib[0], conversion)
                print('wv 0',flush = True) 
                phaseconvcalib0 = Photon2PhaseCalib(self.photondetectcalib[0], tab, nphase)
                print('phase calib 0',flush = True)
                expphasecalib0 = exp_adding_calib(phaseconvcalib0, decay, int(1e6))
                print('exp phase calib 0',flush = True)
                self.nexpphasecalib0 = PhaseNoiseCalib(expphasecalib0, nreadoutscale)
                print('wv 1', flush = True)
                phaseconvcalib1 = Photon2PhaseCalib(self.photondetectcalib[1], tab, nphase)
                print('phase calib 1', flush = True)
                expphasecalib1 = exp_adding_calib(phaseconvcalib1, decay, int(1e6))
                print('exp phase 1', flush = True)
                self.nexpphasecalib1 = PhaseNoiseCalib(expphasecalib1, nreadoutscale)
                print('wv 2', flush = True)
                phaseconvcalib2 = Photon2PhaseCalib(self.photondetectcalib[2], tab, nphase)
                print('phase calib 2', flush = True)
                expphasecalib2 = exp_adding_calib(phaseconvcalib2, decay, int(1e6))
                print('exp phase 2', flush = True)
                self.nexpphasecalib2 = PhaseNoiseCalib(expphasecalib2, nreadoutscale)
                print('calib done')
   
    class PhotonDetection():
        
        def __init__(self, stars):
            print('Detector')
            self.detector = np.zeros(shape = (pxnbr, pxnbr), dtype = object)

            
            for k in range(pxnbr):
                for l in range(pxnbr):
                        self.detector[k,l] = np.random.normal(loc = 0, scale = nreadoutscale, size = (exptime,int(timelinestep)))
                        for i in range(len(stars)):
                            if len(stars['star_'+str(i)].phase[k,l])>0:
                                self.phasedistrib(stars['star_'+str(i)].phase,k,l)
            # self.phase = phase

            # for i in range(pxnbr):
            #    for j in range(pxnbr):
            #         self.phasedistrib(self.phase, i, j)
            

        def phasedistrib(self, phase, i, j):
            
            
            
            if len(phase[i,j]) > 0:
                for ph in range(len(phase[i,j])): 
            
                    if int(phase[i,j][ph][0][0]/1e6) == int(phase[i,j][ph][0][-1]/1e6):
                        inx = list(map(int,phase[i,j][ph][0] - int(phase[i,j][ph][0][-1]/1e6)*1e6))
                        self.detector[i,j][int(phase[i,j][ph][0][-1]/1e6)][inx] += phase[i,j][ph][1]
                      
                    #else:
                        #inx = abs(phase[1][i,j][ph] - int(phase[1][i,j][ph][-1]/1e6)*1e6).argmin()
                        #inxb = list(map(int,phase[1][i,j][ph][:inx] - int(phase[1][i,j][ph][0]/1e6)*1e6))
                        #inxa = np.linspace(0,len(phase[1][i,j][ph] ) - len(inxb) -1, len(phase[1][i,j][ph] ) - len(inxb)).astype(int)
              
                        #self.detector[i,j][int(phase[1][i,j][ph][0]/1e6)][inxb] += phase[0][i,j][ph][:inx]
                        #self.detector[i,j][int(phase[1][i,j][ph][-1]/1e6)][inxa] += phase[0][i,j][ph][inx:]
                        #print('confirm')
                    else: 
                        inx = abs(phase[i,j][ph][0] - int(phase[i,j][ph][0][-1]/1e6)*1e6).argmin()
                        inxb = list(map(int,phase[i,j][ph][0][:inx] - int(phase[i,j][ph][0][0]/1e6)*1e6))
                        inxa = np.linspace(0, len(phase[i,j][ph][0][inx:]) - 1, len(phase[i,j][ph][0][inx:])).astype(int)

                        self.detector[i,j][int(phase[i,j][ph][0][0]/1e6)][inxb] += phase[i,j][ph][1][:inx]
                        self.detector[i,j][int(phase[i,j][ph][0][-1]/1e6)][inxa] += phase[i,j][ph][1][inx:]
                        print(i,j,ph,  int(phase[i,j][ph][0][0]/1e6))
                        print('confirm')


            

    def Output(self, savetype):

        print('output part', flush = True)
        if savetype == 'Simulation':
                    # print('Saving in HDF5 at: ' + str(path))
                    # save_dict_to_hdf5(self.config, path,self,pix_nbr)
            h5file = h5py.File(path, 'w') 
            recursively_save_dict_contents_to_group(h5file, '/', DATA)
            h5file['PSF'] = self.psf.psf
            # h5file['stars'] = {}
            for i in range(0, stnbr):
                # h5file['stars']['star_'+str(i)] = {}
                h5file['stars/star_'+str(i)+'/posx'] = self.stars['star_'+str(i)].posx
                h5file['stars/star_'+str(i)+'/posy'] = self.stars['star_'+str(i)].posy
          
                h5file['stars/star_'+str(i)+'/stardist'] = self.stars['star_'+str(i)].stardist
                h5file['stars/star_'+str(i)+'/spectrum'] = self.stars['star_'+str(i)].spectrum
                

            for k in range(pxnbr):
                for l in range(pxnbr):
                    for s in range(exptime):
                        # h5file['stars/star_'+str(i)+'/'+str(s)+'/'+str(k)+'_'+str(l)] = self.stars['detect_'+str(i)].detector[k,l][s]
                        h5file['Detector/' + str(s) + '/' + str(k)+'_'+str(l)] = self.stars['Detector'].detector[k,l][s]

            try: DATA['Phase']
            except: pass
            else:
                for k in range(pxnbr):
                    for l in range(pxnbr):
                        h5file['Filter/'+str(k)+'_'+str(l)] = self.detect.pixfilter[k,l]
                        
                        h5file['Calibration/'+str(0)+'/'+str(k)+'_'+str(l)] = self.detect.phaseconvcalib0[k,l]
                        h5file['Calibration/'+str(1)+'/'+str(k)+'_'+str(l)] = self.detect.phaseconvcalib1[k,l]
                        h5file['Calibration/'+str(2)+'/'+str(k)+'_'+str(l)] = self.detect.phaseconvcalib2[k,l]

        elif savetype == 'photon_list':

            h5file = h5py.File(path, 'w') 
            recursively_save_dict_contents_to_group(h5file, '/', DATA)
          
            for k in range(pxnbr):
                for l in range(pxnbr):
                    m_noise = max(self.detect.noisetimeline[k,l][1])
                    for s in range(exptime):
                        peaks, _ = find_peaks(self.stars['Detector'].detector[k,l][s],prominence = 10, height=m_noise)
                        h5file['Photons/'+str(s)+'/'+str(k)+'_'+str(l)] = [peaks, self.stars['Detector'].detector[k,l][s][peaks]]



# test = Simulation('/home/sfaes/sim_script_dev/new_version/Template_phase.yaml')
# print(test.star_1.nexpphase[0])
# plt.plot(test.star_1.nexpphase[1][0,0][1],test.star_1.nexpphase[0][0,0][1])
# plt.show()
# print(test.star_1.nexpphasecalib[0][0][0,0][0][500:1000])