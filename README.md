# his-scrapper

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

In the .env file add two lines:

HIS_LOGIN=12345678
HIS_PW=MyHisPasswordSuper!Secret

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

