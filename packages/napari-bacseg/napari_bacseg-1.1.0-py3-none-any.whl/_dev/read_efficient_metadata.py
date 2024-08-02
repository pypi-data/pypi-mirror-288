
from glob2 import glob
import numpy as np
import pandas as pd
import tifffile
import shutil
import matplotlib.pyplot as plt
import pickle
import tifffile
import shutil
from skimage import exposure, img_as_ubyte
import os
from skimage import data
from skimage.registration import phase_cross_correlation
from skimage.registration._phase_cross_correlation import _upsampled_dft
from scipy.ndimage import fourier_shift
import scipy.ndimage
import cv2
import hashlib
import datetime
import json
from multiprocessing import Pool
import tqdm
import pickle
from functools import partial
import pathlib
import traceback
from ast import literal_eval


def generate_bacseg_paths(dat, database_dir=r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG"):
    
    try:
        
        user_initial = dat.user_initial
        folder = dat.folder
        file_name = dat.file_name
        segmentation_file = dat.segmentation_file
        
        image_dir = os.path.join(database_dir,"Images", user_initial,"images",folder)
        mask_dir = os.path.join(database_dir,"Images", user_initial,"masks",folder)
        label_dir = os.path.join(database_dir,"Images", user_initial,"labels",folder)
        json_dir = os.path.join(database_dir,"Images", user_initial,"json",folder)
        
        segmentation_file_json = str(pathlib.Path(segmentation_file).with_suffix('.txt'))
        
        image_save_path = os.path.join(image_dir, file_name)
        mask_save_path = os.path.join(mask_dir, segmentation_file)
        label_save_path = os.path.join(label_dir, segmentation_file)
        json_save_path = os.path.join(json_dir, segmentation_file_json)
        
        dat["image_save_path"] = image_save_path
        dat["mask_save_path"] = mask_save_path
        dat["label_save_path"] = label_save_path
        dat["json_save_path"] = json_save_path
        
    except:
        dat["image_save_path"] = None
        dat["mask_save_path"] = None
        dat["label_save_path"] = None
        dat["json_save_path"] = None
          
    return dat



path = "efficient_metadata.txt"


meta = pd.read_csv(path, sep=",", low_memory=False)

meta = meta.drop_duplicates(subset="segmentation_file")

meta['file_list'] = meta['file_list'].apply(literal_eval)
meta['channel_list'] = meta['channel_list'].apply(literal_eval)

meta["file_name"] = meta["file_list"]
meta["channel"] = meta["channel_list"]

meta = meta.explode(['file_name','channel'])

# meta = meta.apply(lambda row: generate_bacseg_paths(row),axis=1)