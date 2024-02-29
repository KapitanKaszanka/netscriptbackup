
# NetScriptBackUP
**Script to automate configuration backups and more.**

The script is created to automate backup creation and collect telemetry from network devices. It is still in development and will likely be in development for a very long time. The plan is to create a tool that will collect data from devices that can be used to make life easier for administrators.

#### [First run - step by step](./docs/first_run.md) 

### Currently supports devices:
- Cisco IOS, IOS-XE.
- Mikrotik RouterOSv6, RouterOSv7.
- Juniper.

### How it works:
#### Short version:
- [1] Loading configuration.
- [2] Creating device objects.
- [3] Connecting to device, downloading configuration.
- [4] Filtering downloaded configuration.
- [5] Creating/overwriting configuration folders/files.
- [6] Git managment.
- [7] End.

#### Long version:
- [1] Script start parsing information from config.ini. This is place where first validation occur. If something is wrong with config.ini file error will occur script stop working.
  For more information about config.ini check [here](./docs/doc_config.md).
- [2] Information is downloaded from the file indicated in the config, based on which device objects are created. The device object contains variables needed to connect to the device as well as modules responsible for providing appropriate commands or filtering the received data.
- [3] A connection is made to the device using the netmiko module. The script will try to connect via ssh only one of two methods: password, public key. The 'key_file' field decides what type of connection attempt will be made with. If its value is 'null', the login attempt will be made using the password. After connection is established, the appropriate commands are sent.
- [4] Basic filtering. For example, comments are removed from the file.
- [5] Let's move on to file management. The script will check the paths to the  files and if they do not exist, it will create them. File permissions will also be checked. If they are not allocated to the user, an error will be returned and the backup will be interrupted. Once the files are created, they are overwritten/updated with the newly output from device.
- [6] After creating the files, the script will move on to tasks related to the Git repository. These are very basic actions without advanced git features. First, it will be checked whether the repository exists, if it doesn't exist, it will be created and a configuration file added to it. The script checks whether the configuration file is added to the repository. If everything is OK, a 'commit' occurs with the date of any modification.
  > - A separate repository will be created for each device.
  > - The module doesn't yet have the ability to push changes to a remote repository.

- [7] End. The script will wait for a restart.
  
> [!TIP]
> The script can be launched every, say, 5 minutes, which means that we can track any changes in the configuration on an ongoing basis, and because we use Git version control, we will not fill the disk with 'empty runs'.

### Documentation:
| | Name |
| ---- | ---- |
| 1 | [First run - step by step](./docs/first_run.md) |
| 2 | [Supported devices](./docs/supported_vendors.md) |
| 3 | [Config file - docs](./docs/doc_config.md) |
| 4 | [Device parametrs - docs](./docs/doc_devices_file.md) |

### One day:
- encryption,
- better logging,
- restconf module,
- telemetry.
  
> [!WARNING]
> The script and advice on how to use it should be tested first before implementing them into production. I take no responsibility for any damage resulting from the use of the content contained in the publication.

##### *Super sneaky information*
##### *Theoretically, the script will support any vendor with very little work. How and can be used to get telemetry from devices.*








































