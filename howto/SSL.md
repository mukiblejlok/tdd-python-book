# How to add a SSL certificate using Certbot and Nginx
>Based on [DigitalOcena tutorial](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-18-04) 

>It uses [Let's Encrypt](https://letsencrypt.org/) services to obtain free but signed SSL Certificate.

## Prerequisities
1. Ubuntu 18.04
2. Registered domain. ie. name.domain.com, www.name.domain.com
3. DNS records set up based on above domains.
 

## Install Certbot
First add the repository
```bash
$ sudo add-apt-repository ppa:certbot/certbot
```
Then install the certbot nginx package
```bash
$ sudo apt install python-certbot-nginx
```

## Configure Nginx file
```bash
$ sudo nano /etc/nginx/sites-available/name.domain.com
```
Only one line is required to make certbot working
```
server_name name.domain.com www.name.domain.com
```
If you need to validate the config file you can run
```bash
$ sudo nginx -t
```
Then nginx needs to be reloaded.
```bash
$ sudo systemctl reload nginx
```

## Add rule to Ubuntu Firewall
To verify if required apps are available type:
```bash
$ sudo ufw app list
```
You should see find following entries
```
  Nginx Full
  Nginx HTTP
  Nginx HTTPS
  OpenSSH
```
Then two rules have to be added:
```bash
$ sudo ufw allow 'OpenSSH'
$ sudo ufw allow 'Nginx Full'
```
If 'Nginx HTTP' or 'Nginx HTTPS' rules exists, they can be removed by 
```bash
$ sudo ufw delete allow 'Nginx HTTP'
```

## Obtain SSL Certificate

Run certbot nginx plugin:
```bash
$ sudo certbot --nginx -d name.domain.com -d www.name.domain.com
```

If you run it for the first time you will be asked for email and terms of service acceptance.
Then certbot will ask if you want to redirect HTTP to HTTPS (option **2**) or do nothing (option **1**). 

Thats all.
but...

## Verify certbot auto-renewal
To test if auto-renewal done by certbot works well run following command:
```bash
$ sudo certbot renew --dry-run
```
If no errors displayed, then everything is done. 
(Certbot automatically adds cron.d script that runs twice a day and renews all certificates that are within 30 day of expiration)



