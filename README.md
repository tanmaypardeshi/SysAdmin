# SysAdmin
SysAdmin is a program that allows users to control their machines remotely via REST APIs.
Features provided by SysAdmin:
- Access to WMI API through CIM Win32 Classes or WQL
- Access to PyWin32 API
- Access to PySystemd API for Debian Systems
- Psutil API (Supported for both Windows and Debian systems)
- Scheduled/Immediate script creation and execution

Benefits:

- Conveniently add or run scripts
- Remotely control machine through tunneled ngrok url
- No additional software required
- Full access through REST APIs

Supported Operating Systems:

- Debian Based Linux Distributions
- Windows

[Postman APIs and documentation](https://www.postman.com/eldians/workspace/eldians/collection/9835426-049d2c20-123d-4ba0-abfc-2a539ada176e)

## Installation Instructions:
- ### Windows
    1. Extract the `SAC.rar` file
    2. Run the executable installer file
    3. Enter your email id when prompted
    4. `START: The operation completed successfully.` should show up on your screen. You can exit the installer now
    5. You will receive the tunneled url at the entered email in a few minutes
    6. In the Postman collection, replace the value of `{{fast_api}}` variable with this value
    - Failure Cases
        1. Did not receive `"START: The operation completed successfully."` during installation
        2. Received a successful response but did not receive email
    - How to fix
        - Problem 1: Unknown errors. Reasons:
            - Invalid Email address
            - NGROK could not download its resources and tunnel a connection
                - Make sure you entered a correct email address, and try uninstalling and installing again. NGROK won't download it's resources again for the subsequent launch
        - Problem 2: Received an email with the url, but the url did not work
            - Check if "SAC" is running in the Windows Services. If it shows up as stopped, try the above fix again
        - Problem 3: The url worked, but did not receive expected output with a successful response code of 200
            - WMI and Win32 APIs have been observed to produce inconsistent outputs across different systems. Please go through the documentation to implement the required changes to your system, which may include editing Registry keys, DLL files, etc
    - If none of the above steps work, or you wish to set up the application yourself:
        1. Install python
        2. Run `pip install pyinstaller` and `pyinstaller[encryption]` (also `virtualenv`, if not installed)
        3. Clone the source code from our repo, and navigate to the Windows directory in the repo.
        4. Create a virtual environment using `virtualenv venv`
        5. Run `venv\scripts\activate` to start the virtual environment
        6. Run `pip install -r requirements.txt` to install all dependencies.
        7. Run `python main.py <your email here>`. If everything has been setup properly, you should receive a url.
        8. If you wish to generate an executable, run `pyinstaller SAC.spec`
        9. Copy `install.bat, install.py, uninstall.py` and `nssm.exe` into the dist folder.
        10. Try running the `SAC.exe` file.
        11. If it runs just like `main.py`, run `install.bat` to create the installer and uninstaller.
        12. These files install and uninstall `SAC.exe` as a service
- ### Debian based Linux Distributions
    1. Extract the SysAdmin.zip file
    2. Open the terminal where the files have been extracted
    3. Run `chmod +x install.sh` to make `install.sh` executable. NOTE: `install.sh` and `SysAdmin` have to be in the same directory
    4. Run `./install.sh` to start the server
    5. Enter an email when prompted
    6. At this point, SysAdmin will have been installed as a service
    7. You will receive the tunneled url at the entered email in a few minutes
    8. In the Postman collection, replace the value of `{{fast_api}}` variable with this value
    9. To uninstall the service, run `chmod +x uninstall.sh` and `./uninstall.sh`
    - Failure Cases
        1. Did not receive `"Client ready and running as a service"` during installation.
        2. Received a successful response but did not receive email.
    - How to fix
        - Problem 1: Unknown errors. Reasons:
            - Invalid Email address
            - NGROK could not download its resources and tunnel a connection
                - Make sure you entered a correct email address, and try uninstalling and installing again. NGROK won't download it's resources again for the subsequent launch
        - Problem 2: Received an email with the url, but the url did not work
            - Check if "SystemAdmin" is running in the Services. If it shows up as stopped, try the above fix again
    - If none of the above steps work, or you wish to set up the application yourself:
        1. Install python
        2. Run `pip install pyinstaller` and `pyinstaller[encryption]` (also `virtualenv`, if not installed)
        3. Clone the source code from our repo, and navigate to the Ubuntu directory in the repo.
        4. Create a virtual environment using `virtualenv venv`
        5. Run `source venv/bin/activate` to start the virtual environment
        6. Run `pip install -r requirements.txt` to install all dependencies.
        7. Run `python main.py <your email here>`. If everything has been setup properly, you should receive a url.
        8. If you wish to generate an executable, run `./makedist.sh` and `pyinstaller SysAdmin.spec`
        9. Run `chmod +x install.sh` to make `install.sh` executable. NOTE: `install.sh` and `SysAdmin` have to be in the same directory.
        10. Run `./install.sh` to start the server
        11. Enter an email when prompted
        12. At this point, SysAdmin will have been installed as a service
    