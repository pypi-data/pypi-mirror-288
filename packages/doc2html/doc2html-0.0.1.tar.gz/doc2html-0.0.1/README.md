# unoserver-fastapi

## Introduction
This server creates API access to Unoserver (LibreOffice) using FastApi.

[Further unoserver documentation](https://github.com/unoconv/unoserver)

### Installation
We recommend that you use the provided Dockerfile, as the server requires LibreOffice, Unoserver, etc. 
And the integration of Unoserver with the python libraries is not straightforward. 
Install Docker and familiarise yourself with it.
  ```
  docker build -t unoserver-fastapi:v0 .
  docker run unoserver-fastapi:v0
  ```

Or using docker-compose
  ```
  docker-compose build --no-cache
  docker-compose up
  ```

### Local execution
1. Install the local environment using the Pipfile provided. Be aware that it is using python 3.11:
  ```
  pipenv install --dev
  ```
2. Run the script for the unoserver required library (tested in linux [Ubuntu]):
  ```
  # Make the script executable
  chmod +x allocate_local_unoserver.sh
  
  # Run the script
  ./allocate_local_unoserver.sh
  
  # After that, you should be able to run the unoserver locally and you can test it with this command:
  ./environments/virtenv/bin/python3 -m unoserver.server --interface localhost --port 2024
  ```
3. Local run
  ```
  pipenv shell
  
  gunicorn main:app --workers 2 -b :5000 -k uvicorn.workers.UvicornWorker --timeout 60
  ```

### Fonts
You may encounter a font issue with certain documents (ex: pdf).
One option is to bring fonts from Windows into your system.
- Copy the fonts under C:\Windows\Fonts  (removing the .fon files)
- Paste them in /usr/share/fonts/win     (create the folder yourself)
- Update the font cache running on the previous folder
    
  ```
  # These commands require xfonts-utils:  sudo apt-get install xfonts-utils
  mkfontscale
  mkfontdir
  fc-cache
  ```

### System Service
To create a system service for unoserver:
  ```
  nano /etc/systemd/system/unoserver.service
  ```

Copy inside the following:
```
[Unit]
Description=unoserver
After=network.target
 
[Install]
WantedBy=multi-user.target
 
[Service]
Type=simple
User=root
Group=root
ExecStart=/usr/local/bin/unoserver
Environment=PYTHONUNBUFFERED=true
Restart=on-failure
RestartSec=3
```

To take effect:   `systemctl daemon-reload`

To make the service on startup: `systemctl enable daemon-reload`


### Notes:
- If executed on a multi-core machine, run several unoservers with different ports.
here is however no support for any form of load balancing in unoserver, 
you would have to implement that yourself in your usage of unoconverter. 
For performant multi-core scaling, it is necessary to specify unique values 
for each unoserver's --port and --uno-port options.
- A next step may include managing multiple unoservers for the requests.
- Only LibreOffice is officially supported. Other variations are untested.
- Some samples have been downloaded from [sample-videos.com](https://sample-videos.com/download-sample-doc-file.php)
