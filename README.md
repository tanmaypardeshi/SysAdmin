# SysAdmin
SysAdmin is a platform through which a user can manage processes or create new tasks which will run on their machine using APIs.
By using SysAdmin a user can:<br>
    <li>Get list of services and processes running on their machine</li>
    <li>Stop any running processes.</li>
    <li>Store shell scripts anywhere on their machine.</li>
    <li>Schedule tasks by sending the time at which he wants it to run and get the output of the executed script on their email.</li>
    <li>Run any saved script by sending the file name and directory (if specified).</li>
<br>
Benefits:
<br>
<li>Conveniently add or run scripts.</li>
<li>User can remotely manage their machine by using ngrok url.</li>
<li>Don't need any other software to manage services and access everything using REST APIs.</li>
<br>
Supported Operating Systems:
<li>Debian Based Linux Distributions</li>
<li>Windows</li>

##Installation Instructions:

<li>For Windows:</li>
<ol>
    <li>Extract the SAC.rar file.</li>
    <li>Run the executable installer file.</li>
    <li>Enter an email when prompted.</li>
    <li>"START: The operation completed successfully." should show up on your screen. You can exit the installer now.</li>
    <li>You will receive the tunneled url at the entered email in a few minutes.</li>
    <li>In the Postman collection, replace the value of {{fast_api}} variable with this value.</li>
</ol>

####Failure cases:

1. Did not receive "The operation completed successfully" during installation.
2. Received a successful response but did not receive email.

####Reasons:
<li>Invalid Email address</li>
<li>NGROK could not download its resources and tunnel a connection.</li>
<br>
Fix for above steps: Make sure you entered a correct email address, and try uninstalling and installing again. NGROK won't download it's resources again for the subsequent launch.<br>
<br>
<li>Received an email with the url, but the url did not work</li>
<br>
Fix: Check if "SAC" is running in the Windows Services. If it shows up as stopped, try the above fix again.<br>
<br>
<li>The url worked, but did not receive expected output with a successful response code of 200.</li>
<br>
Fix: WMI and Win32 APIs have been observed to produce inconsistent outputs across different systems. Please go through the documentation to implement the required changes to your system, which may include editing Registry keys, DLL files, etc.<br>
<br>
If none of the above steps work, or you wish to set up the application yourself:<br>
<ol>
<li>Install python
<li>Run pip install pyinstaller and pyinstaller[encryption] (also virtualenv, if not installed)
<li>Clone the source code from our repo, and navigate to the Windows directory in the repo.
<li>Create a virtual environment using virtualenv venv
<li>Run venv\scripts\activate to start the virtual environment
<li>Run pip install -r requirements.txt to install all dependencies.
<li>Run python main.py <your email here>. If everything has been setup properly, you should receive a url.
<li>If you wish to generate an ".exe", run pyinstaller SAC.spec
<li>Copy install.bat, install.py, uninstall.py and nssm.exe into the dist folder.
<li>Try running the SAC.exe file.
<li>If it runs just like main.py, run install.bat to create the installer and uninstaller.
<li>These files install and uninstall SAC.exe as a service
</ol>
<li>For Debian Based Linux Distributions</li>
<ol>
    <li>Extract the SysAdmin.zip file</li>
    <li>Open the terminal where the files have been extracted.</li>
    <li>Run <code>chmod +x install.sh</code> to make install.sh executable. NOTE: install.sh and SysAdmin have to be in the same directory.</li>
    <li>Run <code>./install.sh</code> to start the server</li>
    <li>Enter an email when prompted.</li>
    <li>Now SysAdmin has been installed as a service.</li>
    <li>"Client ready and running as a service" should show up on your screen.</li>
    <li>In the Postman collection, replace the value of {{fast_api}} variable with the tunneled url value.</li>
    <li>To uninstall the service you need to run <code>chmod +x uninstall.sh</code> and <code>./uninstall.sh</code></li>
</ol>

####Failure cases:

1. Did not receive "Client ready and running as a service" during installation.
2. Received a successful response but did not receive email.

####Reasons:
<li>Invalid Email address</li>
<li>NGROK could not download its resources and tunnel a connection.</li>
<br>
Fix for above steps: Make sure you entered a correct email address, and try uninstalling and installing again. NGROK won't download it's resources again for the subsequent launch.<br>
<br>
<li>Received an email with the url, but the url did not work</li>
<br>
Fix: Check if "SystemAdmin" is running in the Services. If it shows up as stopped, try the above fix again.<br>
<br>
If none of the above steps work, or you wish to set up the application yourself:<br>
<ol>
<li>Install python
<li>Run pip install pyinstaller and pyinstaller[encryption] (also virtualenv, if not installed)
<li>Clone the source code from our repo, and navigate to the Ubuntu directory in the repo.
<li>Create a virtual environment using virtualenv venv
<li>Run source venv/bin/activate to start the virtual environment
<li>Run pip install -r requirements.txt to install all dependencies.
<li>Run python main.py <your email here>. If everything has been setup properly, you should receive a url.
<li>If you wish to generate an executable, run <code>./makedist.sh</code></li>
<li>Now run <code>pyinstaller SysAdmin.spec</code>
<li>Run <code>chmod +x install.sh</code> to make install.sh executable. NOTE: install.sh and SysAdmin have to be in the same directory.</li>
<li>Run <code>./install.sh</code> to start the server</li>
<li>Enter an email when prompted.</li>
<li>Now SysAdmin has been installed as a service.</li>
</ol>
