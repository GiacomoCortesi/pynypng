### pynypng
pynypng is a python CLI program for easily compressing and resizing images, especially
for web apps usage.


It uses the tinypng REST API: https://tinypng.com/developers/reference

### Sample usage
Install requirements.txt first:
```
pip3 install -r requirements.txt
```

Recursively compress the image files under the original-images folder
```
python3 pynypng --command compress --output-dir ./compressed-images  ./original-images
```

Recursively resize all the image files under the original-images folder.
It supports all resize methods as specified by tinypng REST API documentation.
```
python3 pynypng --command resize --width 150 --output-dir ./resized-images  ./ccac-website-images
```


### Command help
```
usage: pynypng.py [-h] [--key KEY] [--output-dir OUTPUT_DIR]
                  [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                  [--command {compress,resize}] [--width WIDTH]
                  [--height HEIGHT] [--method {scale,fit,cover,thumb}]
                  input_files [input_files ...]

Compress images for web apps using tinyPNG API

positional arguments:
  input_files           image files to convert

optional arguments:
  -h, --help            show this help message and exit
  --key KEY, -k KEY     tiny PNG API key
  --output-dir OUTPUT_DIR, -o OUTPUT_DIR
                        output directory to store converted images
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set the logging level (default: INFO)
  --command {compress,resize}, -c {compress,resize}
                        Command to perform: compress or resize. Default is
                        compress.
  --width WIDTH, -w WIDTH
                        Width for resizing. Required for resize command.
  --height HEIGHT, -a HEIGHT
                        Height for resizing. Required for resize command.
  --method {scale,fit,cover,thumb}, -m {scale,fit,cover,thumb}
                        Resize method to use. Required for resize command.
```

The tinypng API key can be specified through the CLI flag, 
or alternatively through the TINYPNG_API_KEY env variable.
