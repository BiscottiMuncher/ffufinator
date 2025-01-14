#!/usr/bin/env python3
import os
import sys
import subprocess

def run_command(command):
    subprocess.run(command, shell=True, check=True)

def setup_cron(task_path):
    run_command('touch mycron')
    run_command(f'echo "@reboot {task_path}" >> mycron')
    run_command('crontab mycron')
    run_command('rm mycron')
    run_command('sudo reboot')

def install_ffuf():
    if(os.path.exists('/usr/bin/ffuf')): 
        print("fuff already installed")
        return
    else:
        print("Installing ffuf")
        run_command('sudo apt-get install ffuf -y')
         
def setup_env():
    run_command('sudo apt-get install python3.11-venv -y ')
    run_command('python3 -m venv worker')
    pip_path = os.path.join("worker", "bin", "pip")
    run_command(f'{pip_path} install --upgrade pip')
    run_command(f"{pip_path} install dask[distributed]")
    
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
