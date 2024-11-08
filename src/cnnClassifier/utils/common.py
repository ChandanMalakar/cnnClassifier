import os # provide os functions such as file and dir manipulation.
from box.exceptions import BoxValueError # Exception handling for issues with ConfigBox.
import yaml # to read and write yaml files
from cnnClassifier import logger
import json
import joblib
from ensure import ensure_annotations # it is used to throw error if data type of input doesn't matches as of the parameter.
from box import ConfigBox # used to access the yaml output i.e. dict values as objects eg:(dict1.key) instead of eg:(dict1[key]).
from pathlib import Path # used for creating and managing file paths.
from typing import Any # A generic type used for flexibility in function inputs and outputs.
import base64


@ensure_annotations # decorator used
def read_yaml(path_to_yaml: Path) -> ConfigBox: # returns in the form of ConfigBox
    '''reads yaml file and returns
    
    Args:
        path_to_yaml (str): path like input
        
    Raises:
        ValueError: if yaml file is empty
        e: empty file
        
    Returns:
        ConfigBox: ConfigBox type
    '''

    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    

@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    '''create a list of directories
    
    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to 
    '''
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")

 
@ensure_annotations
def save_json(path: Path, data: dict):
    '''save json data
    
    Args:
        path (Path): path to the json file
        data (dict): data to be saved in the json file
    '''
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    '''load json files data
    
    Args:
        path (Path): path to json file
    
    Returns:
        ConfigBox: data as class attributes instead of dict
    '''

    with open(path) as f:
        content = json.load(f)
        
    logger.info(f"json file loaded successfully from: {path}")
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path):
    '''save binary file
    
    Args:
        data (Any): data to be saved as binary
        path (Path): path to binary file
    '''
    joblib.dump(value=data,filename=path)
    logger.info(f"binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    '''load binary data
    
    Args:
        path (Path): path to binary file
        
    Returns:
        Any: object stored in the file
    '''
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data


@ensure_annotations
def get_size(path: Path) -> str:
    '''get size in KB
    
    Args:
        path (Path): path of the file
        
    Returns:
        str: size in KB
    '''
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"


def decodeImage(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)
        f.close()


def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())