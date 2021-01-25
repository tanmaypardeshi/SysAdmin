@ECHO OFF
ECHO Setting up distributable client
pyinstaller --onefile --name SAC-installer install.py --add-data "nssm.exe;." --add-data "SAC.exe;." --key="4Gk5vJbyN4wC7wK7"
pyinstaller --onefile --name SAC-uninstaller uninstall.py --add-data "nssm.exe;." --distpath unSAC --workpath unBuild --key="4Gk5vJbyN4wC7wK7"