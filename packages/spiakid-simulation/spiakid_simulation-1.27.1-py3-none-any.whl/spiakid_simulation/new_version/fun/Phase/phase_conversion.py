import numpy as np
import multiprocessing as mp
import csv
from scipy.optimize import least_squares
import numpy.random as rand


def phase_conv(Photon,pix,conv_wv,conv_phase,resolution, process_nb):
    r"""Convert the wavelength in phase on each pixel

    Parameters:
    -----------

    Photon: array
        Photon's wavelength on each pixel

    pix: array
        Pixel id

    conv_wv: array
        Calibration's wavelength

    conv_phase: array
        Calibration's phase

    resolution: float
        Spectrale resolution of the detector

    Output:
    -------

    signal: array
        Phase on each pixel 
    
    
    """
    dim = np.shape(Photon)
    signal = np.zeros(dim,dtype = object)

    args = []
    for i in range(len(pix)):
        k,l = np.int64(pix[i].split(sep='_'))
        if k < dim[0] and l < dim[1]:
            args.append([Photon[k,l],conv_wv[i],conv_phase[i],resolution,(k,l)])

    with mp.Pool(processes=process_nb) as pool : 
        res = pool.map(photon2phase,args)

    for r in res:
        signal[r[0][0],r[0][1]] = r[1]
 
    return(signal)


def phase_conv_calib(data,pix,conv_wv,conv_phase,resolution, process_nb):
    signal_calib = []

  
    for wv in range(len(data)):
       
        sig = phase_conv(data[wv][1],pix,conv_wv,conv_phase,resolution, process_nb)
        signal_calib.append([data[wv],sig])

    
    return(signal_calib)

def ConversionTab(Photon, conversion):
    dim_x, dim_y = np.shape(Photon[0])
    pix, conv_wv, conv_phase = conversion
    convtab = np.zeros(shape = (dim_x, dim_y), dtype = object)
    for i in range(len(pix)):
        k, l = np.int64(pix[i].split(sep='_'))

        if k < dim_x and l < dim_y:
            convtab[k,l] = fit_parabola(conv_wv[i], conv_phase[i])

    return(convtab)

def photon2phase(Photon, curv, resolution):
    r"""Convert the wavelength in phase

    Parameters:
    -----------

    Photon: array
        Photon's wavelength on each pixel

    conv_wv: array
        Calibration's wavelength

    conv_phase: array
        Calibration's phase

    Output:
    -------

    signal: array
        Signal converted in phase 
    
    
    """

    
    dim_x, dim_y = np.shape(Photon[0])

    signal = np.copy(Photon)
    for i in range(dim_x):
        for j in range(dim_y):
       
                # for j in range(0,len(Photon[0][k,l])):

                ph = curv[i,j][0] * np.array(Photon[0][i,j]) ** 2 +  curv[i,j][1] * np.array(Photon[0][i,j]) + curv[i,j][2]
                sigma = ph / (2*resolution*np.sqrt(2*np.log10(2)))

                signal[0][i,j] = np.where(Photon[0][i,j]==0,0,np.random.normal(ph, sigma))
 
    return(signal)
    #         curv = fit_parabola(conv_wv,conv_phase)
    # ph = curv[0] * Photon[1] ** 2 +  curv[1] * Photon[1] + curv[2] #µ
    # sigma = ph / (2*resolution*np.sqrt(2*np.log10(2)))
    # signal[1] = np.where(Photon[1]==0,Photon[1],np.random.normal(ph, sigma))
    # return(inx,signal)

def PhaseNoise(photon, scale):

    dimx, dimy = np.shape(photon[0])
    sig = np.zeros(shape = 2, dtype = object)
    sig[0] = np.zeros(shape = (dimx, dimy), dtype = object)
    sig[1] = np.zeros(shape = (dimx, dimy), dtype = object)


    for i in range(dimx):
        for j in range(dimy):
            sig[0][i,j] = []
            sig[1][i,j] = []
            if len(photon[0][i,j]) >0:
                for k in range(len(photon[0][i,j])):
                    
                    sig[0][i,j].append(rand.normal(loc = 0,scale = scale, size = len(photon[0][i,j][k] )) + photon[0][i,j][k])
                    sig[1][i,j].append(np.copy(photon[1][i,j][k]))

    return(sig)

def PhaseNoiseCalib(photon, scale):

    dimx, dimy = np.shape(photon[0])
    sig = np.zeros(shape = (dimx, dimy), dtype = object)
    
    for i in range(dimx):
        for j in range(dimy):
            sig[i,j] = [photon[1][i,j], photon[0][i,j] + rand.normal(loc = 0,scale = scale, size = len(photon[0][i,j] ))]
    
    return(sig)

def exp_adding(photon,decay, exptime):
    r""" Add the exponential decay after the photon arrival

    Parameters:
    -----------

    sig: array
        Signal with the photon arrival

    decay: float
        The decay of the decreasing exponential
    
    Output:
    -------
    
    signal: array
        The signal with the exponential decrease
    
    """

    listph = np.zeros(np.shape(photon[0]), dtype = object)
    listtime = np.zeros(np.shape(photon[0]), dtype = object)
    dimx, dimy = np.shape(photon[0])
    
    for i in range(dimx):
        for j in range(dimy):
            listph[i,j] = []
            listtime[i,j] = []
            if len(photon[0][i,j])>0:
                for k in range(len(photon[0][i,j])):
                    if int(photon[1][i,j][k]) + 500 < exptime * 1e6:
                        listtime[i,j].append(np.array(range(0,500))+int(photon[1][i,j][k]))
                        listph[i,j].append(photon[0][i,j][k] * np.exp(decay * np.array(range(0,500))/1e6) )
                    else:
                        t = exptime*1e6 - (int(photon[1][i,j][k]) + 500)
                        print(photon[0][i,j][k])
                        print(np.exp(decay * np.array(range(0,t))/1e6))
                        listph[i,j].append(photon[0][i,j][k] * np.exp(decay * np.array(range(0,t))/1e6))
                        listtime[i,j].append(np.array(range(0, t))+int(photon[1][i,j][k]))
    return([listph, listtime])

def extractDigits(lst, decay):
    return list(map(lambda el:np.array(np.exp(decay * np.linspace(el,el+498,499) * 1e-6)).astype(np.float64), lst))


def AddingExp(ph, photonlist, time):
    ph = ph.astype(np.float64)
    addmatrix = np.zeros(shape = (len(ph)),dtype=np.float64)
    for (t, photon) in zip(time, photonlist):
     
        addmatrix[t:t+len(photon)] = photon
    ph = ph + addmatrix
    return(ph)

def exp_adding_calib(photon,decay, exptime):

    phasecalib = np.copy(photon)
    
    dimx, dimy = np.shape(photon[0])
    for i in range(dimx):
        for j in range(dimy):
            # print(time)
 
            photonlist = extractDigits(photon[0][i,j], decay)

            if phasecalib[1][i,j][-1] + 500 > exptime:
                ph = np.zeros(shape= (phasecalib[1][i,j][-1] + 500))
                extphoton = AddingExp(ph, photonlist, phasecalib[1][i,j])
                phasecalib[0][i,j] = extphoton[:exptime]
                phasecalib[1][i,j] = np.linspace(0,exptime-1,exptime, dtype = int)
            
            else:
                ph = np.linspace(0,exptime-1,exptime, dtype = int)
                phasecalib[0][i,j] = AddingExp(ph, photonlist, phasecalib[1][i,j])
                phasecalib[1][i,j] = np.linspace(0,exptime-1,exptime, dtype = int)


    return(phasecalib)



def read_csv(Path,sep='/'):
    r"""Read the calibration file

    Parameters:
    -----------

    Path: string
        Path to the calibration file
    
    sep: string
        The delimiter

    Output:
    -------

    pix: array
        The pixel id

    wv: array
        Calibration wavelength

    phase: array
        Calibration phase          
    
    
    """
    pix = []
    wv = []
    phase = []
    with open(Path,'r') as file:
        data = csv.reader(file,delimiter = sep)
        for i in data:
            pix.append(i[0])
            wv.append(eval(i[2]))
            phase.append(eval(i[1]))
    return(pix,wv,phase)


def fit_parabola(wavelength, phase):
        def model(x,u):
            return(x[0]*u**2 + x[1]*u + x[2])     
        def fun(x,u,y):
            return(model(x,u) - y)
        def Jac(x,u,y):
            J = np.empty((u.size,x.size))
            J[:,0] = u**2
            J[:,1] = u
            J[:,2] = 1
            return(J)
        t = np.array(wavelength)
        dat = np.array(phase)
        x0 = [1,1,1]
        res = least_squares(fun, x0, jac=Jac, args=(t,dat)) 
        return res.x[0],res.x[1],res.x[2]