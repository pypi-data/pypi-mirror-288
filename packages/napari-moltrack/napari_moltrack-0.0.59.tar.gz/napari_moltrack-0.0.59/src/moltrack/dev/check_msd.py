import trackpy as tp
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import numpy as np
from scipy.spatial.distance import squareform, pdist
import pickle
import time
from numba import njit
import trackpy



path = r"D:\1 Rho-PAmCherry FOV\24-05-02 RhoPAM-plasmid-NusGsfGFP poorM9_17.03.43_18_Channel1_moltrack_tracks.csv"
path = r"D:\1 Rho-PAmCherry FOV\24-05-02 RhoPAM-plasmid-NusGsfGFP poorM9_17.03.43_18_dataset_channel_moltrack_tracks.csv"

df = pd.read_csv(path, sep=",")

pixel_size_nm = 100
pixel_size_um = 100 *1e-3
exposure_time_ms = 10
exposure_time_s = exposure_time_ms * 1e-3
fps = 1 / exposure_time_s

mpp = pixel_size_um


def calculate_msd_numba(x, y, max_lag):
    
    x = np.array(x)
    y = np.array(y)
    
    n = len(x)
    msd_values = np.zeros(max_lag)

    for lag in range(1, max_lag + 1):
        displacements_x = x[lag:] - x[:-lag]
        displacements_y = y[lag:] - y[:-lag]
        squared_displacements = displacements_x ** 2 + displacements_y ** 2
        msd = np.mean(squared_displacements)
        msd_values[lag - 1] = msd

    return msd_values


def compute_msd_pandas(df, max_lag):
    
    msd_values = []

    for lag in range(1, max_lag + 1):
        displacements = (df[['x', 'y']].shift(-lag) - df[['x', 'y']]).dropna()
        squared_displacements = (displacements ** 2).sum(axis=1)
        msd = squared_displacements.mean()
        msd_values.append(msd)

    return msd_values


for particle in df.particle.unique():
    
    particle_df = df[df.particle == particle].copy()
    particle_df = particle_df[["particle", "frame", "x", "y"]]
    
    msdDD = trackpy.motion.msd(particle_df, mpp, fps, len(particle_df))
    
    # x = particle_df["x"].tolist()
    # y = particle_df["y"].tolist()
    # max_lag = len(x)
    
    msd0 = msdDD["msd"].tolist()
    # msd2 = calculate_msd_numba(x,y,max_lag)
    # msd3 = compute_msd_pandas(particle_df, len(particle_df))
        
    break