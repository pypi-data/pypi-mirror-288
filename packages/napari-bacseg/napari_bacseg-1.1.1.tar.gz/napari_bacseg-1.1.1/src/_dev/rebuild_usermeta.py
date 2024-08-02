# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 18:44:12 2022

@author: turnerp
"""

from glob2 import glob
import numpy as np
import pandas as pd
import tifffile
import shutil
import matplotlib.pyplot as plt
import pickle
# import psycopg2
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
import traceback


def read_tif(path):
    
    try:

        with tifffile.TiffFile(path) as tif:
            metadata = tif.pages[0].tags["ImageDescription"].value
            metadata = json.loads(metadata)
    except Exception:
        metadata = {}
        pass
            
    return metadata




def get_filemeta(path):
    
    try:
    
        meta = read_tif(path)
        
        if "posX" in meta.keys():
            
            posX = meta['posX']
            posY = meta['posX']
            posZ = meta['posX']
            
        elif "StagePos_um" in meta.keys():
            posX,posY,posZ = meta["StagePos_um"]
        else:
            posX = 0
            posY = 0
            posZ = 0

        
        if "date_modified" in meta.keys():
            date_modified = meta["date_modfied"]
        else:
            date_modified = datetime.datetime.now()
            
        if "date_created" in meta.keys():
            date_created = meta["date_created"]
        else:
            date_created = datetime.datetime.now() 

        file_name = path.split("\\")[-1]
        file_metadata = pd.DataFrame([[
            datetime.datetime.now(),
            date_created,
            date_modified,
            file_name,
            meta["channel"],
            meta["file_list"],
            meta["channel_list"],
            meta["segmentation_file"],
            str(meta["segmentation_channel"]),
            meta["akseg_hash"],
            meta["user_initial"],
            meta["image_content"],
            meta["microscope"],
            meta["modality"],
            meta["light_source"],
            meta["stain"],
            meta["antibiotic"],
            meta["treatmenttime"],
            meta["abxconcentration"],
            meta["mount"],
            meta["protocol"],
            meta["usermeta1"],
            meta["usermeta2"],
            meta["usermeta3"],
            meta["folder"],
            meta["parent_folder"],
            meta["segmented"],
            meta["labelled"],
            meta["segmentations_curated"],
            meta["labels_curated"],
            posX,
            posY,
            posZ,
            meta["image_path"],
            path,
            None,
            path.replace("\\images\\","\\masks\\"),
            None,
            path.replace("\\images\\","\\masks\\")]]
            ,
            columns=["date_uploaded",
            "date_created",
            "date_modified",
            "file_name",
            "channel",
            "file_list",
            "channel_list",
            "segmentation_file",
            "segmentation_channel",
            "akseg_hash",
            "user_initial",
            "content",
            "microscope",
            "modality",
            "source",
            "stain",
            "antibiotic",
            "treatment time (mins)",
            "antibiotic concentration",
            "mounting method",
            "protocol",
            "user_meta1",
            "user_meta2",
            "user_meta3",
            "folder",
            "parent_folder",
            "segmented",
            "labelled",
            "segmentation_curated",
            "label_curated",
            "posX",
            "posY",
            "posZ",
            "image_load_path",
            "image_save_path",
            "mask_load_path",
            "mask_save_path",
            "label_load_path",
            "label_save_path"]
            )
        
    except Exception:
        
        print(traceback.format_exc())
        
        file_metadata = pd.DataFrame(columns=["date_uploaded",
                                              "date_created",
                                              "date_modified",
            "file_name",
            "channel",
            "file_list",
            "channel_list",
            "segmentation_file",
            "segmentation_channel",
            "akseg_hash",
            "user_initial",
            "content",
            "microscope",
            "modality",
            "source",
            "stain",
            "antibiotic",
            "treatment time (mins)",
            "antibiotic concentration",
            "mounting method",
            "protocol",
            "user_meta1",
            "user_meta2",
            "user_meta3",
            "folder",
            "parent_folder",
            "segmented",
            "labelled",
            "segmentation_curated",
            "label_curated",
            "posX",
            "posY",
            "posZ",
            "image_load_path",
            "image_save_path",
            "mask_load_path",
            "mask_save_path",
            "label_load_path",
            "label_save_path"])
        
        pass
    
    return file_metadata
                                 
    
paths = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images\PT\images"
paths = glob(paths + "*\**\*.tif")
paths = [path for path in paths if "_flows.tif" not in path]



file_metadata = get_filemeta(paths[0])


if __name__=='__main__':

    with Pool() as p:
        
        d = list(tqdm.tqdm(p.imap(get_filemeta, paths), total=len(paths)))
        p.close()
        p.join()
        
        user_metadata = pd.concat(d)
        
        user_metadata.drop_duplicates(subset=['akseg_hash'], keep="first", inplace=True)
        
        user_initials = user_metadata["user_initial"].unique().tolist()
        
        for user_initial in user_initials:
            
            akgroup_dir = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images"
            user_metadata_path = akgroup_dir + "\\" + user_initial + "\\" + user_initial + "_file_metadata.txt"   
            
            data = user_metadata[user_metadata["user_initial"]==user_initial]
            
            data.to_csv(user_metadata_path, sep=",", index = False)            



# for path in paths:
#     try:
#         file_metadata = get_filemeta(path)
#     except Exception:
#         print(path)
#         break
    





# akgroup_dir = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images"
# user_initial = "PT"
# user_metadata_path = akgroup_dir + "\\" + user_initial + "\\" + user_initial + "_file_metadata.txt"
# user_metadata = pd.read_csv(user_metadata_path, sep=",")


# antibiotics = user_metadata["antibiotic"].unique()


# print(user_metadata.columns)


# xx = user_metadata[user_metadata["user_meta3"]is"Repeat 1"]


# user_metadata["segmentation_channel"] = user_metadata["segmentation_channel"].astype(str)
# user_metadata = user_metadata[user_metadata["segmentation_channel"]is"53d2"]

# for i in range(len(user_metadata)):
    
#     file_name = user_metadata["file_name"][i]
#     file_name_path = os.path.basename(user_metadata["image_save_path"][i])
    
#     if file_name!=file_name_path:
#         print(i)



