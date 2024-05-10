from glob import glob
import os

def removeFiles(filepath: str) -> bool:
    status = False
    try:
        files = glob(f"{filepath}/*")
        for file in files:
            os.remove(file)
        status = True
    except Exception as e:
        status = False
        print("ERROR == ", e)
        
    return status
    