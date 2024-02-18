
# BackupApp

**A multi-vendor script for automating backups of network device configurations using Git version control.**


### Currently supports devices:
- Cisco IOS, IOS-XE.
- Mikrotik RouterOSv6, RouterOSv7.
- Juniper.
- 
### Basic operation of the application:
#### Short version:
- Configuration parsing.
- Creating device objects.
- Connecting to device.
- Downloading configuration.
- Filtering downloaded configuration.
- Creating/overwriting configuration folders/files.
- Creating git repozytory.
- Commiting chagnes to repozytory.

#### Long version:
The app starts by parsing all the information it needs about its settings and device logins. 
If there is an error in the settings, an error occurs and the startup is canceled. 
In case of an error in the device parameters, it will be skipped.
Using the netmiko module and an SSH connection, their configuration is downloaded from the devices and then filtered from unnecessary things, e.g. comments, "!".

### Documentation:
| | Name |
| ---- | ---- |
| 1 | [First run step by step](./docs/1.first_run.md) |
| 2 | [Supported devices](./docs/supported_vendors.md) |
| 3 | [Config file](./docs/doc_config.md) |
| 4 | [Device parametrs](./docs/doc_devices_file.md) |

##### *Super sneaky information*
###### *Theoretically, the script will support any vendor with very little work. How and can be used to download telemetry from devices.*








































