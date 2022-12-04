import os, subprocess

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
