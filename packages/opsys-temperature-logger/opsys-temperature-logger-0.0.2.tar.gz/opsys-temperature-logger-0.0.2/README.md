# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* This repository is a part of opsys automation infrastructure
* This repository is temperature logger implementation for temperature sensors device

### How do I get set up? ###

* pip install opsys-temperature-logger

### Unit Testing

* python -m unittest -v

### Reference Links

* Installation Software: 'R:\Lidar\Dima\Software\picolog-setup-6.2.7.exe'

### Pyinstaller

* Directories containing DLLs should be imported by pyinstaller during executable generation.
* The following functionality should be added inside pyinstaller spec file:
```
def get_dirs(root_folder, hint):
    target_dirs = []
    for root, dirs, files in os.walk(root_folder):
        for dir in dirs:
            if '.env' in os.path.join(root, dir) and hint in dir:
                target_dirs.append(os.path.join(root, dir))
    return target_dirs

root_folder_path = os.getcwd()
dirs = get_dirs(root_folder_path, 'opsys_temperature_logger')
datas_dirs = [(f'{_dir}\*', './opsys_temperature_logger/') for _dir in dirs]
```
* ```datas_dirs``` should be added at ```datas``` variable:
```
pathex=[],
binaries=binaries_file,
datas=datas_dirs,
```

### Usage Example
```
### PicoLog data logger

from opsys_temperature_logger.temperature_logger import TemperatureLogger

temperature_logger = TemperatureLogger()

temperature_logger.connect()
temperature_logger.set_channel(channel_number=1)
print(temperature_logger.read_temperature(channel=1))
temperature_logger.close_connection()
```