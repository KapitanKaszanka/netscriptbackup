
### Linux setup. How I do it.
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
sudo mkdir -p /script/backup_app/backup_configuration/
```

5. You need to change permissions for users.
```bash
sudo chown root:script_runners /script/
sudo chmod 750 /script/
sudo chown -R script_run:script_runners /script/backup_app/
sudo chmod -R 750 /script/backup_app
```

6. Creating a file for logs.
```bash
sudo mkdir -p /var/log/backup_app/
touch /var/log/backup_app/backup_app.log
sudo chown -R root:script_run /var/log/backup_app/
sudo chmod 610 /script/backup_app/
sudo chmod 620 /script/backup_app/backup_app.log
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
git clone https://github.com/krupczynskimateusz/backup_app.git
````

10. Changing script setting.
- Config
 ```bash
  cd backup_app/
  nano config.ini
  ```
  ```ini
  [Applications_Setup]
  Configs_Path = /script/backup_app/backup_configuration/
  [Logging]
  File_Path = /var/log/backup_app/backup_app.log
  ```

- Adding devices to the JSON database.
```bash
nano files/devices.json
```
  
Well, do it yourself ;)

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
git config --global user.name "Backup App"  
git config --global user.email backupapp@superexample.com 
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
ls /script/backup_app/backup_configuration/
cd /script/backup_app/backup_configuration/r1.network/
cat r1.network_conf.txt
git status
git log
```

15. If everything works correctly, you can automate it and put it into production. Remember, single tests do not guarantee that everything will work. Don't forget to uncomment what you commented. This will really increase the security of your network. 

16. What else?
- linux hardering,
- nftables.

### Good luck.



