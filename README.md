
# Ffufinator

ffuf distributed across multiple machines using Dask

## Installation

Install all packages with pip, ffuf is a requirement across all machines 

```bash
pip install -r requirements.txt
```

## Usage/Examples

Running this script on the main/naster machines will send tasks to all the workers
```bash
./ffufinator <host_IP> <url> <wordlist> <output_file> [ffuf_arguments]

```

All worker machines should have dask running on start up

```bash
./setup <dask_scheduler_IP>
```

## Lessons Learned

This re-sparked my interest in python(for the millionth time) and distributed computing as a whole, I have been doing lots of API and endpoint fuzzing for my current certification I am working on. Speeding up the process with a VM server or cloud host was really the next logical step in my eyes. 

## License

[MIT](https://choosealicense.com/licenses/mit/)
