# Linux Server Config
This is the final project that builds a Linux server and run the Item Catalog website on it.

* [Deployed web site](http://ec2-52-200-118-181.compute-1.amazonaws.com/) (IP address: 52.200.118.181)
* [Amazon Lightsail](https://lightsail.aws.amazon.com) is used to launch and manage a virtual private server with AWS.
* Ubuntu is used as a Linux server in Lightsail

# Software install and configurations
## Linux server setup
First, go to [Amazon Lightsail](https://lightsail.aws.amazon.com) to make a new instance with Ubuntu.
Once the new instance has started up, we can SSH in as the ubuntu user. Now, we have a virtual server!

## Security setup
Create a new user 'grader' and grant a proper access for the user. Also only allow incoming connections for SSH (port 2200), http and ntp.

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
   
   Now, you can SSH with port 2200 using `ssh grader@52.200.118.181 -i ~/.ssh/your-ssh-public-key-filename -p 2200`.
   
9. Configure the Uncomplicated Firewall (UFW)
   Set UFW to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123) using below command.
   
   ```
   sudo ufw allow http
   sudo ufw allow ntp
   sudo ufw allow 2200
   sudo ufw default deny incoming
   sudo ufw default allow outgoing
   sudo ufw enable
   ```
   
## Deploy the category project
1. Update all installed packages by below command
   ```
   sudo apt-get update
   sudo apt-get upgrade
   ```
2. Configure the local timezone to UTC
   Execute `sudo dpkg-reconfigure tzdata` and select UTC on a screen which brings up

3. Install Apache, Postgres, and Python tools
   ```
   sudo apt-get install apache2
   sudo apt-get install -y postgresql
   sudo apt-get install python-setuptools libapache2-mod-wsgi
   sudo apt-get install python-pip
   sudo apt-get install -y python-dev
   sudo apt-get install -y python-psycopg2
   sudo apt-get install libpq-dev
   ```
   
4. Configure Postgres
   Login as user postgres by `sudo su - postgres`
   
   Get into postgreSQL shell `psql`
   
   On the shell, create a database and a new user. Then set password and grant a permission for the user.
   ```
   CREATE DATABASE catalog;
   CREATE USER catalog;
   ALTER ROLE catalog WITH PASSWORD 'catalog';
   GRANT ALL PRIVILEGES ON DATABASE catalog TO catalog;
   ```
   
   Type `\q` to exit from postgreSQL then `exit` to exit from the user postgres

5. Install git and clone the catalog project
   Next, install git using `sudo apt-get install git` and clone the project under /var/www.
   Once the project is cloned, edit .git directory to access by only owner.
   
   ```
   cd /var/www
   sudo git clone https://github.com/sallychan55/fullstack-nanodegree.git
   cd fullstack-nanodegree/
   sudo chmod 400 .git
   ```
   
   Rename project.py to __init__.py using `sudo mv project.py __init__.py`.
   
   Edit database_setup.py, sample_data_sets.py and __init__.py to change `engine = create_engine('sqlite:///shopitemswithusers.db')` to `engine = create_engine('postgresql://catalog:catalog@localhost/catalog')`.

   Finally run `sudo python database_setup.py` to create a database schema. Run `sudo python python sample_data_sets.py` to set sample data if you want :)
   
 6. Configure Apache
    Create a config file to configure Apache to serve the project as a virtual host using `sudo vi /etc/apache2/sites-available/catalog.conf`.
    
    Paste following lines for configuration:
    ```
    <VirtualHost *:80>
            ServerName 52.200.118.181
            ServerAdmin wmix04@gmail.com
            WSGIScriptAlias / /var/www/fullstack-nanodegree/flaskapp.wsgi
            <Directory /var/www/fullstack-nanodegree/catalog/>
                    Order allow,deny
                    Allow from all
            </Directory>
            Alias /static /var/www/fullstack-nanodegree/catalog/static
            <Directory /var/www/fullstack-nanodegree/catalog/static/>
                    Order allow,deny
                    Allow from all
            </Directory>
            ErrorLog ${APACHE_LOG_DIR}/error.log
            LogLevel warn
            CustomLog ${APACHE_LOG_DIR}/access.log combined
    </VirtualHost>
    ```
    
    Enable the virtual host using `sudo a2ensite catalog`.
    
7. Create the .wsgi File
   Create .wsgi file that points to the project to start running.
   Run `sudo vi /var/www/fullstack-nanodegree/flaskapp.wsgi` and paste following lines.
   
   ```
   import sys
   import logging
   logging.basicConfig(stream=sys.stderr)
   sys.path.insert(0,"/var/www/fullstack-nanodegree/")

   from catalog import app as application
   ```
    
   Restart apache server using `sudo service apache2 restart`
    
# References
* [How To Add and Delete Users on an Ubuntu 14.04 VPS
](https://www.digitalocean.com/community/tutorials/how-to-add-and-delete-users-on-an-ubuntu-14-04-vps)
* [How To Secure PostgreSQL on an Ubuntu VPS
](https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps)
* [How To Deploy a Flask Application on an Ubuntu VPS](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)
