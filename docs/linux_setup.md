
### Linux basic setup. How I do it.
#### Setup is done on Ubuntu 22.04

1. Log in to linux server.
```bash
ssh mateusz@backup_server.network
```

2. First, let's create a new user who will run the script. This user will be responsible only for executing the script, and this user's keys will also be used to connect to the devices. Therefore, we do not want anyone to be able to log in to it
```bash
sudo adduser --disabled-login script_run
```

3. Creating a group for users who manage scripts may also be useful.
```bash
sudo addgroup script_runners
```

4. Now create a folder where the downloaded data from devices will be stored.
```bash
sudo mkdir -p /script/netscriptbackup/backup_configuration/
```

5. You need to change permissions for users.
```bash
sudo chown root:script_runners /script/
sudo chmod 750 /script/
sudo chown -R script_run:script_runners /script/netscriptbackup/
sudo chmod -R 750 /script/netscriptbackup
```

6. Creating a file for logs.
```bash
sudo mkdir -p /var/log/netscriptbackup/
touch /var/log/netscriptbackup/netscriptbackup.log
sudo chown -R root:script_run /var/log/netscriptbackup/
sudo chmod 610 /script/netscriptbackup/
sudo chmod 620 /script/netscriptbackup/netscriptbackup.log
```
The script does not rotate logs for now. You have to take care of it yourself. Logrotate works very well.

7. Setup script_run user.
```bash
sudo usermod -aG script_runners script_run
sudo su - script_run
```

8. Generating keys for an ssh connection
```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N "strongpassword"
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N "diffrentstrongpassword"
``` 

9. Downloading the git repository
```bash
git clone https://github.com/krupczynskimateusz/netscriptbackup.git
````

10. Changing script setting.
- Config
 ```bash
  cd netscriptbackup/
  nano config.ini
  ```
  ```ini
  [Applications_Setup]
  Configs_Path = /script/netscriptbackup/backup_configuration/
  [Logging]
  File_Path = /var/log/netscriptbackup/netscriptbackup.log
  ```

- Adding devices to the JSON database.
```bash
nano files/devices.json
```
  
Well then, do it yourself. [Click](./docs/doc_devices_file.md)

11. Setup python
- I recommend using a python virtual environment.
  ```bash
  python3 -m venv .venv/
  ```
  If it doesn't work, check online how to set up a Python virtual environment for Ubuntu.
- Installing the necessary modules.
  ```bash
  source .venv/bin/activate
  pip install -r requirements.txt
  deactivate
  ```

12. Setup git for user.
```bash
git config --global user.name "Net Script Backup"  
git config --global user.email netscriptbackup@superexample.com 
git config --global init.defaultBranch main # Optional
```

13. First run
> [!IMPORTANT]
> The script does not allow connection to hosts whose keys have not been previously manually accepted.
> To disable this, go to [modules/connections.py](./modules/connections.py) and comment out the "ssh_strict=True" line. It occurs twice in code.
> After the first run, I suggest uncommenting these lines.

  ```bash
  .venv/bin/python3 main.py
  ```

14. Checking if everything works properly.
```bash
ls /script/netscriptbackup/backup_configuration/
cd /script/netscriptbackup/backup_configuration/<device name>/ 
cat r1.network_conf.txt
git status
git log
```

15. If everything works correctly, you can automate it and put it into production. Remember, single tests do not guarantee that everything will work. Don't forget to uncomment what you commented. This will really increase the security of your network. 

### Good luck.
