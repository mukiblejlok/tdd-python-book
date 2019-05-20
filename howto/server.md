Short Guide on how to startup and manage Ubuntu based server for django development.


A. Initial settings and users

1. Generate private ssh key on your local machnie. Authentiacation with password should not be an alternative no a first choice.
```bash
ssh-keygen
```
By default on windows the key is stored in
```
c:\Users\{UserName}\.ssh\id_rsa.pub
```
2. Login to your server as a root
```bash
ssh root@111.111.222.111
```
---
**Intermezzo 1**
There is an article [My First 5 Minutes On A Server; Or, Essential Security for Linux Servers]( https://plusbryan.com/my-first-5-minutes-on-a-server-or-essential-security-for-linux-servers) that describes in few short steps what to do when you startup you server for the first time. In this and following intermezzos I will add some points from it.

```bash
apt-get update
apt-get upgrade
apt-get install fail2ban
```
---

3. Create a user that will run our applications (with *sudo* access and '*deploy*' as a name)
```bash
useradd -m -s /bin/bash deploy   
# -m creates a home folder
# -s sets user to use bash by default

usermod -a -G sudo delpoy 
# add user to the sudoers group

passwd deploy 
# set password for user
# make it hard and long, because we will use ssh in most of the times, password will be used only when sudoing


su - deploy
# switch-user to being 'deploy'!
``` 

4. Check (in another console) if you can log in
```
ssh deploy@111.111.222.111
...
sudo echo sudo_works!
```
---
**Intermezzo 2**
How to copy your ssh private key to the server.
On linux is as easy as:
```bash
ssh-copy-id deploy@111.111.222.111
```
Unfortunately windows has no 'ssh-copy-id' application you it has to be done a different way. When using *cmder* or *GitBASH* it can be done by piping cat and ssh
```bash
cat c:\Users\{UserName}\.ssh\id_rsa.pub | ssh deploy@111.111.222.111 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys".
```
In both cases you will be prompted for a password to confirm. If everything goes ok then next login will be possible without password.
---

---
**Intermezzo 3**
Set up your firewall. Ubuntu has a default firewall called 'ufw'.
To set it up for a ssh and web server only do following (as a sudo):
```bash
ufw allow from {your-ip} to any port 22
# if you have dynamic ip or more clients you can make it more open with 
# ufw allow 22
ufw allow 80  # HTTP
ufw allow 443  # HTTPS
ufw enable
```
To check the status use ```ufw status```

