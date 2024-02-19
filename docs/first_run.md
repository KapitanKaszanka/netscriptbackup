### First run

#### 1. Download the repository to your local system:

```bash
git clone http://github.com/krupczynskimateusz/backup_app.git
```
#### 2. Go to the repository folder:

```bash
cd backup_app/
```
#### 3. Configure application settings. The file is located in the config.ini folder by default.
There are paths where device data will be downloaded, where backups will be saved, and where application logs will be stored.
I highly suggest changing to the settings recommended in the config.ini documentation for practical reasons.
*[Config.ini documentation](./docs/doc_config.md)*
```bash
nano config.ini
```

#### 4. Configuration of device login parameters. Default file path files/devices.json.
```bash
nano files/devices.json
```
 - A brief description of the required pools. Marked with [x] they are required for correct operation. Marked with [o] may be set to null:
   - [x] ip -> main json key; it cannot be repeated; use to connect to device; can be dns name,
   - port -> SSH port through which you can connect to the device,
   - [x] vendor -> the value must be the same as in supported devices,
   - connection -> for future use; it is worth setting 'ssh'
   - [x] username,
   - change_mode -> settings for switching to privileged mode; default null; check docs for more information
   - [x] password or key_file/passphrase -> login method; check docs for more information
- [Docs devices.json](./docs/doc_devices_file.md)
- [Supported vedors](./docs/supported_vendors.md)
  
```json
{
    "192.168.11.11": {
        "name": "R1",
        "vendor": "cisco",
        "port": 22,
        "connection": "ssh",
        "username": "cisco",
        "password": "cisco",
        "change_mode": [
            "enable 5",
            "superstrongpassword"
        ],
        "key_file": null,
        "passphrase": null
    },
    "2001:db8:abcd::2": {
        "name": "R12",
        "vendor": "cisco",
        "port": 22,
        "connection": "ssh",
        "username": "cisco",
        "password": "cisco",
        "change_mode": [
            null,
            "superstrongpassword"
        ],
        "key_file": "/home/backup_app/.ssh/cisco_id_ed25519",
        "passphrase": "superstrongpassword"
    },
    "r6.juniper.network": {
        "name": "R6",
        "vendor": "juniper",
        "port": 22,
        "connection": "ssh",
        "username": "juniper",
        "password": null,
        "change_mode": null,
        "key_file": "/home/backup_app/.ssh/juniper_id_rsa",
        "passphrase": "superstrongpassword"
    }
}
```

#### 5. Python configuration.
- I suggest using a python virtual environment:
```bash
python3 -m venv .venv
```
- Enable the virtual environment:
```bash
source .venv/bin/activate
```
- Installing the necessary packages:
```bash
pip install -r requirements.txt
```
#### 6. Git settings.
Before running, you need to change the global git settings if they are not already set.

```bash
git config --global user.name "Backup App"  
git config --global user.email backupapp@superexample.com 
git config --global init.defaultBranch main # Optional
```

#### 7. Now you can perform the first run. The console should show any errors.

```bash
.venv/bin/python3 main.py
```
> [!IMPORTANT]
> 
>
> The script does not allow connection to hosts whose keys have not been previously manually accepted.
> To disable this, go to [modules/connections.py](./modules/connections.py) and comment out the ssh_stric line. It occurs twice in code.
> After the first run, I suggest uncommenting these lines.
> More information: [Security considerations](./docs/security_considerations.md)

```python
with ConnectHandler(
    **connection_parametrs,
    # ssh_strict=True,
    system_host_keys=True
    ) as connection:
#########################
with ConnectHandler(
    **connection_parametrs,
    use_keys=True,
    # ssh_strict=True,
    system_host_keys=True
    ) as connection:
```

#### 8. End
If everything works correctly, a configuration backup will appear in the folder of your choice. 
A local Git repository will also be created, thanks to which you can track changes in device configuration. 
The script currently does not have the ability to push changes to a remote repository, if someone needs such an option, they must add it themselves or do it manually.
Now you can have the script run automatically using cron or systemd.timers.


#### Good luck















