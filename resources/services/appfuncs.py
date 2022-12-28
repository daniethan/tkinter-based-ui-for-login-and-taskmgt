import os, subprocess
import glob
from typing import Union

def search_with_glob(filename: Union[str,None]=None, root_dirs: list[str]=['C:\\Program Files', 'C:\\Program Files']):
    if filename is not None:
        globs = [glob.iglob(pathname=f'**/*{filename}*.exe', root_dir=root_dirs[i], recursive=True) for i in range(len(root_dirs))]
    else:
        globs = [glob.iglob(pathname=f'**/*.exe', root_dir=root_dirs[i], recursive=True) for i in range(len(root_dirs))]
    
    for path_generator in globs:
        for filepath in path_generator:
            yield os.path.basename(filepath),filepath


def search(filename: str, search_path: str = "C:\\Program Files"):
    for root, _, files in os.walk(search_path):
        for fname in files:
            if filename.lower() in fname.lower() and fname.endswith('.exe'):
                yield fname, os.path.join(root, fname)

def get_running_tasks():
    task = subprocess.run("tasklist /fo list", capture_output=True, text=True)
    if task.returncode == 0:
        tasks_on = task.stdout.splitlines()
        for byt in tasks_on:
            if 'Image Name' in byt and byt.endswith('.exe'):
                yield byt.split(':')[-1].strip()

def get_sys_info():
    resp = subprocess.run("systeminfo /fo list", capture_output=True, text=True)
    if resp.returncode == 0:
        info = resp.stdout.splitlines()
        for byt in info:
            if ':' in byt:
                yield byt.strip()

if __name__=='__main__':
    result = {file:path for file,path in search_with_glob()}
    for i, f in enumerate(sorted(set(result.items())), start=1):
        print(i, f[0], sep=': ')