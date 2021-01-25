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
<li>For Debian Based Linux Distributions</li>
<ol>
    <li>Extract the SysAdmin.zip file</li>
    <li>Open the terminal where the files have been extracted.</li>
    <li>Run <code>chmod +x run.sh</code> to make run.sh executable. NOTE: run.sh and SysAdmin have to be in the same directory.</li>
    <li>Run <code>./run.sh</code> to start the server</li>
    <li>Enter an email when prompted.</li>
    <li>"The tunneled url have been sent to <i>email</i>" should show up on your screen.</li>
    <li>Now you can keep the terminal on in the background and make API calls.</li>
    <li>In the Postman collection, replace the value of {{fast_api}} variable with the tunneled url value.</li>
</ol>

