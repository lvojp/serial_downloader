# serial_downloader / sdl
Download the files saved with the serial number at once.

## Getting Started

### 1
Install Poetry and command ```poetry install```

(Introduction | Documentation | Poetry - Python dependency management and packaging made easy
https://python-poetry.org/docs/)

And run ```poetry run python src/sdl.py```

### 2
Use the executable file ```dist/sdl```

### 3
Install packages from requirements.txt
```pip install -r requirements.txt```


## Usage
To get help ```sdl.py -h```
```
-u URL, --url URL
    Enter the URL of the last file of the serial numbered file
    ex: -u https://example.com/storage/100.pdf

-s START_NUM, --start_num START_NUM
    First file number of serial number file 
    ex: [-s 001] or [-s 01] or [-s 1]

-o OUTPUT, --output OUTPUT
    Output destination directory
    ex: -o /tmp/dest
```

For example, if you want to download files from 001 to 100 to /tmp/download
```
sdl.py -u https://example.com/storage/100.pdf -s 001 -o /tmp/download
```

## License
This software is released under the MIT License, see ```LICENSE.txt```
