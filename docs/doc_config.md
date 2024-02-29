### Config files
> [!NOTE]
> #### Security note
> The script will download and store the configuration of network devices and requires some authentication method to work. Leakage of such information may have tragic consequences. As a responsible administrator, you should appropriately secure access to these files and devices by limiting the possibility of logging in to a specific pool of addresses and creating 'service' accounts that will limit the list of possible commands to be entered on the devices. I also encourage you to log in using your public key instead of your password.

#### Script setup
###### Information about where script can find the files, and where it should save it:
- **Devices path** - The path to the file where the script can find information about how to log in to the device, IP addresses, etc. In the future, the ability to encrypt this file will be added. Best stored together with the script files or in a created folder in /etc/. The file will contain passwords and other things needed to connect to the device, so it's worth keeping it secure.
- **Configs path** - The path to the file where the script will save configurations or update some data. The file will contain device configuration, so it is worth limiting access to it.

#### Script setup
###### Login level settings. The staging area will be rebuilt in the future:
- **Level** - Login level. Possible choices: debug, info, warning, error, critical. The 'debug' level returns a lot of information and should be used as its name suggests, i.e. for debugging. I recommend setting it to 'info' or 'warring'.
- **File path** - File path where logs will be saved
