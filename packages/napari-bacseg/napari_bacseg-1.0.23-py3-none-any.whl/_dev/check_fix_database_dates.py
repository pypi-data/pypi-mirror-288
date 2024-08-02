import pandas as pd
import numpy as np
from ast import literal_eval
import datetime
import datefinder
import tqdm
from tqdm import tqdm
from multiprocessing import Pool
from functools import partial

metadata_columns = ["date_uploaded", "date_created", "date_modified", "file_name", "channel", "file_list", "channel_list", "segmentation_file", "segmentation_channel", "akseg_hash",
    "user_initial", "content", "microscope", "modality", "source", "strain", "phenotype", "stain", "stain_target", "antibiotic", "treatment time (mins)", "antibiotic concentration",
    "mounting method", "protocol", "folder", "parent_folder", "num_segmentations", "image_laplacian", "image_focus", "image_debris", "segmented", "labelled", "segmentation_curated",
    "label_curated", "posX", "posY", "posZ", "image_load_path", "image_save_path", "mask_load_path", "mask_save_path", "label_load_path", "label_save_path", ]


def check_metadata_format(metadata, expected_columns):
    missing_columns = list(set(expected_columns) - set(metadata.columns.tolist()))
    extra_columns = list(set(metadata.columns.tolist()) - set(expected_columns))

    all_columns = list(set(expected_columns + extra_columns))

    metadata[missing_columns] = pd.DataFrame([[None] * len(missing_columns)], index=metadata.index)

    date = datetime.datetime.now()

    metadata.loc[metadata["date_uploaded"].isin(["None", None, np.nan, 0]), ["date_uploaded", "date_created", "date_modified"],] = str(date)

    metadata = metadata[all_columns]

    metadata = metadata.astype({"segmented": bool, "labelled": bool, "segmentation_curated": bool, "label_curated": bool, })

    return metadata, all_columns

def read_metadata(path):

    user_metadata = pd.read_csv(path, sep=",", low_memory=False)
    user_metadata = user_metadata.astype("str")
    
    user_metadata = user_metadata.drop_duplicates(subset="segmentation_file")
    
    user_metadata["segmented"] = user_metadata["segmented"].apply(literal_eval)
    user_metadata["labelled"] = user_metadata["labelled"].apply(literal_eval)
    user_metadata["segmentation_curated"] = user_metadata["segmentation_curated"].apply(literal_eval)
    user_metadata["label_curated"] = user_metadata["label_curated"].apply(literal_eval)
    
    user_metadata[["treatment time (mins)"]] = user_metadata[["treatment time (mins)"]].apply(pd.to_numeric, downcast="float", errors="coerce")
    
    # user_metadata, expected_columns = check_metadata_format(user_metadata, metadata_columns)
    
    user_metadata["segmentation_channel"] = user_metadata["segmentation_channel"].astype(str)
    
    user_metadata['file_list'] = user_metadata['file_list'].apply(literal_eval)
    user_metadata['channel_list'] = user_metadata['channel_list'].apply(literal_eval)
    
    user_metadata["file_name"] = user_metadata["file_list"]
    user_metadata["channel"] = user_metadata["channel_list"]
    
    user_metadata = user_metadata.explode(['file_name', 'channel'])
    
    user_metadata.drop_duplicates(subset=["segmentation_file"], keep="first", inplace=True)
    
    return user_metadata



def fix_dates(dat):
    
    for date_col in ["date_uploaded", "date_created", "date_modified"]:
        
        try:
    
            date = dat[date_col]
            
            matches = datefinder.find_dates(date)
            
            for date_match in matches:
                date = date_match.strftime('%Y-%m-%d %H:%M:%S')
                dat[date_col] = date
            
        except:
            dat[date_col] = ""
    
    return dat


user_initial = "PT"
path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Images\{}\{}_file_metadata.txt".format(user_initial,user_initial)

meta = read_metadata(path)


meta = [row for index, row in meta.iterrows()]

if __name__ == '__main__':
    
    with Pool() as p:
        
        results = list(tqdm(p.imap(fix_dates, meta), total=len(meta)))
        
        p.close()
        p.join()
        
        results = pd.DataFrame(results).reset_index(drop=True)
        # meta = meta[metadata_columns]
        
        results.drop_duplicates(subset=["segmentation_file"], keep="first", inplace=True)
        
        results.to_csv(path, sep=",", index = False) 
        
    
        

# # meta = meta[meta["user_meta1"] == "SpeciesIDv2"]

# # meta = meta[["date_uploaded", "date_created", "date_modified"]].iloc[:1000]


# for index, row in tqdm(meta.iterrows(), total=len(meta), desc='Processing Rows'):
#     # Update the row
#     updated_row = fix_dates(row)
    
#     # Update the DataFrame with the updated row
#     meta.iloc[index] = updated_row
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    