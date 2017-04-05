# Linux Server Config
This is the final project that builds a Linux server and run the Item Catalog website on it.

* [Deployed web site](http://ec2-52-200-118-181.compute-1.amazonaws.com/) IP address: 52.200.118.181
* [Amazon Lightsail](https://lightsail.aws.amazon.com) is used to launch and manage a virtual private server with AWS.
* Ubuntu is used as a Linux server in Lightsail

# Software install and configurations
## Linux server setup
First, go to [Amazon Lightsail](https://lightsail.aws.amazon.com) to make a new instance with Ubuntu.
Once the new instance has started up, we can SSH in as the ubuntu user. Now, we have a virtual server!

## Security setup
Create a new user 'grader' and grant a proper access for the user. Also only allow connections for SSH (port 2200).

1. Download a default private key for the default Lightsail user ubuntu from [here](https://lightsail.aws.amazon.com/ls/webapp/account)
2. Change the permissions on the key file for the user ubuntu

  `chmod 600 LightsailDefaultPrivateKey.pem `
  
3. SSH to the server using the key

  `ssh ubuntu@52.200.118.181 -i ~/.ssh/LightsailDefaultPrivateKey.pem`
  
4. Add a new user once logged onto the server as the user ubuntu

  `sudo adduser grader`

   Type `sudo cat /etc/passwd` and confirm that the new user grader should be listed in the output.

5. Give the new user access to sudo

   Type `sudo visudo` to open the appropriate configuration file in your editor.
   
   Add one line to grant access for grader like below.
     ```
     # User privilege specification
     root    ALL=(ALL:ALL) ALL
     grader  ALL=(ALL:ALL) ALL
     ```
     
    Make sure that you can execute `sudo login grader` now to login as grader. 

6. Generate SSH keys
   On your local computer, execute `ssh-keygen` to generate SSH keys.
   
   Then, run `cat your-ssh-public-key-filename.pub` to copy the key. This is for next step. 

7. Add the public key to the server
   Back to a terminal which ssh in the server as grader, create .ssh directory and paste the public key using below command.

   ```
   mkdir .ssh
   touch .ssh/authorized_keys
   ```
   
   Modify permission to allow editing 
   ```
   chmod 700 .ssh
   chmod 664 .ssh/authorized_keys
   ```
   
   Now you can SSH as grader using `ssh grader@52.200.118.181 -i ~/.ssh/your-ssh-public-key-filename` 

8. SSH port update
   Modify Post 20 to 2200 on the config by `sudo nano /etc/ssh/sshd_config`
   
   Then restart the server using `sudo service ssh restart` to reflect the update.
   
   On Amazon Lightsail page, go to Network tab and add the new port in Firewall section. 
   `Application=Custom, Protocol=TCP, Port=2200`
   
   Test you can SSH with port 2200 using `ssh grader@52.200.118.181 -i ~/.ssh/your-ssh-public-key-filename -p 2200`.
   

IP address, URL, summary of software installed, summary of configurations made, 
a list of third-party resources used to completed this project.
