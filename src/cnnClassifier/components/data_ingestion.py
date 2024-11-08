import os
import urllib.request as request
from zipfile import ZipFile
from tqdm import tqdm
from pathlib import Path
from cnnClassifier import logger
from cnnClassifier.entity import (DataIngestionConfig)
from cnnClassifier.utils import get_size


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config


    def download_file(self):
        logger.info("Trying to download file...")
        if not os.path.exists(self.config.local_data_file):
            logger.info("Download started...")
            filename, headers = request.urlretrieve(
                url = self.config.source_URL,
                filename = self.config.local_data_file
            )
            logger.info(f"{filename} download! with the following info: \n{headers}")
        else:
            logger.info(f"file already exists of size: {get_size(Path(self.config.local_data_file))}")
    
    # the method name which starts with underscore(_) is called (hidden methods).
    # and can't be accessed by the user and only the author can access it

    def _get_updated_list_of_files(self, list_of_files):
        return [f for f in list_of_files if f.endswith(".jpg") and ("Cat" in f or "Dog" in f)]

    
    def _preprocess(self, zf: ZipFile, f: str, working_dir: str):
        target_filepath = os.path.join(working_dir, f)
        if not os.path.exists(target_filepath):
            zf.extract(f, working_dir)
        
        if os.path.getsize(target_filepath) == 0:
            logger.info(f"removing files:{target_filepath} of size: {get_size(Path(target_filepath))}")
            os.remove(target_filepath)



    def unzip_and_clean(self):
        logger.info(f"unzipping the file and removing the unwanted files")
        with ZipFile(file=self.config.local_data_file, mode="r") as zf:
            list_of_files = zf.namelist()
            updated_list_of_files = self._get_updated_list_of_files(list_of_files) #._get_updated_list_of_files method returns only the dog & cat folders.
            for f in tqdm(updated_list_of_files):
                self._preprocess(zf, f, self.config.unzip_dir)