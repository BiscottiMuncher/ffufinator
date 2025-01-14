
# Ffufinator

A distributed computing fuzzer

## Installation

Install requirements on main/master machine
```bash
pip install -r requirements.txt
```

Setup will install all needed scripts, packages, generate the python environment, and setup a cron task that starts dask-worker on boot
```bash
python3 setup <dask_scheduler_IP>
```

## Usage/Examples

Running this script on the main/naster machines will send tasks to all the workers
```bash
./ffufinator.py <url + FUZZ> <wordlist> <output_file> [ffuf_arguments...]
```

An example of ffufinator, fuzzing ffuf.me
```bash
./ffufinator.py http://www.ffuf.me wordlist ffuf_me
```

A working example of ffufinator, fuzzing ffuf.me, with ffuf arguments attached 
```bash
./ffufinator.py http://www.ffuf.me wordlist ffuf_me -recursion -recursion-depth 3
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Credits
ffuf: https://github.com/ffuf/ffuf

## Lessons Learned

This re-sparked my interest in python(for the millionth time) and distributed computing as a whole, I have been doing lots of API and endpoint fuzzing for my current certification I am working on. Speeding up the process with a VM server or cloud host was really the next logical step in my eyes. 
