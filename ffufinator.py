#!/usr/bin/env python3

import os
import sys
import subprocess
from dask.distributed import Client, as_completed


def check_and_start_scheduler():
    try:
        result = subprocess.run(
            ["pgrep", "dask-scheduler"], 
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print("Dask scheduler not running. Starting scheduler...")
            subprocess.Popen(["dask-scheduler"])  
            print("Dask scheduler started.")
        else:
            print("Dask scheduler is already running.")
    except Exception as e:
        print(f"Error checking or starting Dask scheduler: {str(e)}")



def run_ffuf(directory_chunk, base_url, wordlist_file, ffuf_flags):
    temp_file = "tmpwl.txt"
    with open(temp_file, 'w') as f:
        for directory in directory_chunk:
            f.write(directory + "\n")

    cmd = ["ffuf", "-u", f"{base_url}", "-w", temp_file]

    if ffuf_flags:
        cmd.extend(ffuf_flags)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        dirty_input = result.stdout.splitlines()
        filtered_lines = [line for line in dirty_input if line.startswith("\x1b[2K")]
        formatted_lines = [line.replace("\x1b[2K", "").strip() for line in filtered_lines]
        cleaned_output = "\n".join(formatted_lines)  

    except Exception as e:
        dirty_input = f"Error: {str(e)}"

    os.remove(temp_file)
    
    return cleaned_output

def distribute_work(master_addr, base_url, wordlist, wordlist_file, ffuf_flags):
    client = Client(f'tcp://{master_addr}:8786') 

    num_workers = len(client.scheduler_info()['workers'])
    chunk_size = len(wordlist) // num_workers
    wordlist_chunks = [wordlist[i:i + chunk_size] for i in range(0, len(wordlist), chunk_size)]
    
    futures = client.map(run_ffuf, wordlist_chunks, [base_url] * len(wordlist_chunks), [wordlist_file] * len(wordlist_chunks), [ffuf_flags] * len(wordlist_chunks))

    results = []
    for future in as_completed(futures):
        results.append(future.result())
    
    return results


def main():
    check_and_start_scheduler()

    fancy_text = """
    '||''''|  .|';           .|';                         ||
     ||  .    ||             ||    ''                     ||
     ||''|   '||'  '||  ||` '||'   ||  `||''|,   '''|.  ''||''  .|''|, '||''|
     ||       ||    ||  ||   ||    ||   ||  ||  .|''||    ||    ||  ||  ||
    .||.     .||.   `|..'|. .||.  .||. .||  ||. `|..||.   `|..' `|..|' .||.

    Usage: ffufinator <master_address> <url + FUZZ> <worslist> <output> [ffuf_flags...]
    """
    if len(sys.argv) < 4:
        print(fancy_text)
        sys.exit(1)

    master_addr =sys.argv[1]
    base_url = sys.argv[2]  
    wordlist_file = sys.argv[3]  
    output_file = sys.argv[4]  
    ffuf_flags = sys.argv[4:]  

    with open(wordlist_file, 'r') as file:
        wordlist = [line.strip() for line in file.readlines()]
    
    results = distribute_work(master_addr, base_url, wordlist, wordlist_file, ffuf_flags)

    with open(output_file, 'w') as f:
        for result in results:
            f.write(result)

    print(f"Output saved to {output_file}")

if __name__ == "__main__":
    main()