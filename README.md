
# BackupApp
### Working in progress. 
**A multi-vendor script for automating backups of network device configurations using Git version control.**


### Currently supports devices:
- Cisco IOS, IOS-XE.
- Mikrotik RouterOSv6, RouterOSv7.
- Juniper.
### Basic operation of the application:
#### Short version:
- [1] Configuration parsing.
- [2] Creating device objects.
- [3] Connecting to device.
- [4] Downloading configuration.
- [5] Filtering downloaded configuration.
- [6] Creating/overwriting configuration folders/files.
- [7] Creating git repozytory.
- [8] Commiting chagnes to repozytory.

#### Long version:
- [1] App start parsing information from config.ini. This is place where first validation occur. If something is wrong with config.ini file error will occur application stop working.
  For more information about config.ini check [here](./docs/doc_config.md).
- Using the netmiko module and an SSH connection, their configuration is downloaded from the devices and then filtered from unnecessary things, e.g. comments, "!".

### Documentation:
| | Name |
| ---- | ---- |
| 1 | [First run step by step](./docs/1.first_run.md) |
| 2 | [Supported devices](./docs/supported_vendors.md) |
| 3 | [Config file](./docs/doc_config.md) |
| 4 | [Device parametrs](./docs/doc_devices_file.md) |

##### *Super sneaky information*
###### *Theoretically, the script will support any vendor with very little work. How and can be used to download telemetry from devices.*








































