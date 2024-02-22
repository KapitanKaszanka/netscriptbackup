### Devices file

> [!NOTE]
> #### Security note
> The script will download and store the configuration of network devices and requires some authentication method to work. Leakage of such information may have tragic consequences. As a responsible administrator, you should appropriately secure access to these files and devices by limiting the possibility of logging in to a specific pool of addresses and creating 'service' accounts that will limit the list of possible commands to be entered on the devices. I also encourage you to log in using your public key instead of your password.

#### Brief information:
All device information is stored in JSON format. When starting the program, it only undergoes basic validation of this format. This means that errors in entered devices are not validated at this stage, and therefore, devices that have insufficient or incorrect information will be rejected at a later stage. After adding it, it is worth checking the script logs to verify whether everything is working properly.

#### Description of database keys:
The database uses the device's IP address as the master key for the entry, this means that it isn't possible to add two devices with the same IP.
> The information in bold is required to be completed. The rest can be set to 'null'.
- **IP** - the master key identifying the device.
- name - device name. It is not necessary for the script to function properly. It is used to create files and folders for more convenient searching.
- **vendor** - name of the device and possible software version. A necessary condition for proper operation. The name should match the name in [this file](supported_vendors.md)
- **port** - the port on which the script will try to establish an SSH connection.
- connection - entry for later use. It is worth setting it to 'ssh', currently it can be set to null.
- **username** - the username with which the script will connect via SSH.
- ***password*** - optional or required parameter. If you log in with a password, enter it here. When logging into devices using public keys, it may be set to null; read key_file. 
- change_mode - Data needed to switch to privileged mode. When you use a permission level other than the standard one, enter the command in the first field, e.g. 'enable 5'. If you don't use it, the field may remain empty. Enter the password in the second field. If you don't use any of the above, the option can be set to null.
- ***key_file*** - the absolute path to the private key that will be used to connect to the device. This option clearly determines whether we will connect using a password or a public key. Setting it to a value other than 'null' causes the script to try to connect using the public key and only in this way.
- passphrase - the password that is used to encrypt the public key.

#### Examples:
- Cisco - login with password, privileged level 5:
```json
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
```
- Mikrotik - login with public key:
```json
"2001:db8::13": {
    "name": "MT-13",
    "vendor": "mikrotik",
    "port": 22,
    "connection": "ssh",
    "username": "mikrotik",
    "password": null,
    "change_mode": null,
    "key_file": "/home/netscript/.ssh/mikrotik_id_rsa",
    "passphrase": "strongpassword"
    },
```
- Juniper - login with password:
```json
"r6.juniper.network": {
    "name": "R6",
    "vendor": "juniper",
    "port": 22,
    "connection": "ssh",
    "username": "juniper",
    "password": "juniper",
    "change_mode": null,
    "key_file": null,
    "passphrase": null
    }
```
