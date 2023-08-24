# his-scrapper

The his-scrapper is a tool for all Frankfurt UAS students. It automatically checks every 5 minutes on HIS if a new grade was published. If so it makes a sound and displays the grade. This script was until now only tested for my account and on a MacOS system. Feel free to open Issues if you find any bugs and I will fix them :) you can also contribute to the project to make it better, just contact me, everyone is welcome. I'm not sure how exectly HIS works, and I also do not care, but I am pretty sure that this script works only for EBIS students, beacause of the static URL that is used, if you are from another study program and want to use the script, again just open a Issue and I am sure we will find a way to make it work. 

## How to use it

1) Install requirements
You need to have Python 3 installed and all the requirements in `requirements.txt`, wich you can easily install with pip by running: 
```
pip install -r requirements.txt
```
Selenium also requires you to install a webdriver. In this script I used the chromium driver: https://sites.google.com/chromium.org/driver/ .

2) Create a `.env` file
```
his-scrapper
├── .env
└── main.py
```

In the .env file add two line
```
HIS_LOGIN=12345678
HIS_PW=MyHisPasswordSuper!Secret
EMAIL_USER=email@anbieter.de
EMAIL_PASSWORD=MyHisPasswordSuper!Secret
EMAIL_TO=email@anbieter.de
SMTP_SERVER=smtp.server.de
SMTP_PORT=587
```
Of course you'll need to use your own HIS Login Data

3) Run 
```bash
python3 main.py init
```

This will create a file `.grades` which will conrtain a list of all module's numbers that you already have your grades for. 
```
his-scrapper
├── .env
├── .grades
└── main.py
```
4) Now you are ready to go. Everytime you start your computer you can run the script with:
```bash
python3 main.py fetch
```
And the script will fetch your grades from HIS every 5 minutes and check if there is any new grade. If there is, it will make a sound and display the new grade on the console. To test if that actually worsk, you can just go ahead an delete one of the module numbers in `.grades` and the run the script.

