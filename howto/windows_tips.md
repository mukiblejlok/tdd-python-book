List of tips on how to handle Windows as a development system

1. How to run a command line with a temporary set of enviromental variable
On linux it is
```
STAGING_SERVER=superlists-staging.ottg.eu python manage.py test functional_tests
```
However on Windows you have to do
```
env STAGING_SERVER=superlists-staging.ottg.eu python manage.py test functional_tests
```


2. Deploy a fabfile
```
cd deploy_tools
fab deploy:host=django@lists.fmularczyk.pl
```