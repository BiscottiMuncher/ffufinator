#!/usr/bin/env python3
import os
import sys
import subprocess

def setup_cron(task_path):
    subprocess.run('touch mycron', shell=True, check=True)
    subprocess.run(f'echo "@reboot {task_path}" >> mycron', shell=True, check=True)
    subprocess.run('crontab mycron', shell=True, check=True)
    subprocess.run('rm mycron', shell=True, check=True)
    subprocess.run('sudo reboot', shell=True, check=True)

def install_ffuf():
    if(os.path.exists('/usr/bin/ffuf')): 
        print("fuff already installed")
        return
    else:
        print("Installing ffuf")
        subprocess.run('sudo apt-get install ffuf -y', shell=True, check=True)
     
def setup_env():
    subprocess.run('sudo apt-get install python3.11-venv -y ', shell=True, check=True)
    subprocess.run('python3 -m venv worker', shell=True, check=True)
    pip_path = os.path.join("worker", "bin", "pip")
    subprocess.run(f"{pip_path} install --upgrade pip", shell=True, check=True)
    subprocess.run(f"{pip_path} install dask[distributed]", shell=True, check=True)

def generate_script(master_addr):
    file_path = 'worker.sh'
    with open(file_path, 'w') as file:
        file.write('#!/bin/bash\n')
        file.write('source worker/bin/activate \n')
        file.write(f'dask-worker tcp://{master_addr}:8786')
    os.chmod(file_path, 0o755)
    print('File created successfully')
    return os.path.abspath('worker.sh')

def main():
    if len(sys.argv) < 2:
        print("Usage: setup.py <master_addr>")
        sys.exit(1)

    install_ffuf()
    setup_env()
    master_addr = sys.argv[1]
    generate_script(master_addr)
    setup_cron(generate_script(master_addr))
    
if __name__ == "__main__":
    main() 