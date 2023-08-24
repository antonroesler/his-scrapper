from typing import List
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from beepy import beep
from selenium.webdriver.chrome.options import Options
import os
import sys
from dotenv import load_dotenv

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

o = Options()
o.add_argument("--headless")


new_garde = 0
COUNTER = 0


class Grade:
    def __init__(self, num: int, name: str, grade:float, bonus:int) -> None:
        self.num = num
        self.name = name
        self.grade = grade
        self.bonus = bonus

    def __str__(self) -> str:
        return f"{self.name}: {self.grade}"


def load_nums():
    temp = []
    try:
        with open(".grades", 'r') as file:
            for line in file:
                temp.append(int(line.split(",")[0]))
    except FileNotFoundError:
        with open(".grades", 'w') as file:
            file.write('')
    return temp

def add_grade(module_id: int, grade: float, name: str):
    with open('.grades', 'a') as file:
        file.write(str(module_id)+",\t" + str(grade) + ",\t"+str(name))
        file.write("\n")


def get_all_grades_from_his() -> List[Grade]:
    grades = []
    driver = webdriver.Chrome(options=o)
    driver.get("https://his.frankfurt-university.de")
    sleep(1)
    user_field = driver.find_element(By.ID, "asdf")
    pw_field = driver.find_element(By.ID, "fdsa")

    user_field.send_keys(os.environ.get("HIS_LOGIN"))
    pw_field.send_keys(os.environ.get("HIS_PW"))

    login_btn = driver.find_element(By.ID, "loginForm:login")
    login_btn.click()

    sleep(2)
    l = driver.find_elements(By.CSS_SELECTOR, "a")

    for e in l:
        if h := e.get_attribute("href"):
            s = h.split("=")
            for i, x in enumerate(s):
                if x =="password&asi":
                    asi= s[i+1]
    if asi:
        driver.get(f"https://his.frankfurt-university.de/qisserver/rds?state=notenspiegelStudent&next=list.vm&nextdir=qispos/notenspiegel/student&createInfos=Y&struct=auswahlBaum&nodeID=auswahlBaum%7Cabschluss%3Aabschl%3D19%2Cstgnr%3D1&expand=0&asi={asi}#auswahlBaum%7Cabschluss%3Aabschl%3D19%2Cstgnr%3D1")
        sleep(2)
        ts = driver.find_elements(By.CSS_SELECTOR, "table")
        trs = ts[1].find_elements(By.TAG_NAME, "tr")
        for tr in trs:
            x = [td.text for td in tr.find_elements(By.TAG_NAME, "td")]
            if len(x) > 4:
                if str(x[5]) != '0' and str(x[0]) != '1':
                    grades.append(Grade(int(x[0]), x[1], float(x[3].replace(",", ".")), int(x[5])))
    driver.close()
    return grades


def add_all_existing():
    current = load_nums()
    for grade in get_all_grades_from_his():
        if grade.num not in current:
            add_grade(grade.num, grade.grade, grade.name)


def check(nums):
    for grade in get_all_grades_from_his():
        if grade.num not in nums and grade.bonus > 0 and grade.num != 1:
            print()
            print("New Grade is Out")
            print(grade)
            send_email(grade)
            add_grade(grade.num, grade.grade, grade.name)
            for _ in range(10):
                beep(5)
                sleep(1)
                if grade == 1.0:
                    beep(6)

def send_email(grade):
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")
    from_email = email_user
    to_email=os.getenv("EMAIL_TO")

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = "New Grade"

    message=(f"Modul: {grade.name}: {grade.grade}")
    
    msg.attach(MIMEText(message, "plain"))

    # E-Mail-Verbindung aufbauen
    server = smtplib.SMTP(os.getenv("SMTP_SERVER"), os.getenv("SMTP_PORT"))  # Beispielserver und Port
    server.starttls()

    server.login(email_user, email_password)

    server.sendmail(from_email, to_email, msg.as_string())

    server.quit()

if __name__ == "__main__":
    print("Welcome to the HIS Grade Scrapper. Use help to get help.")
    try:
        arg = sys.argv[1]
    except:
        arg = "help"
    user = os.environ.get("HIS_LOGIN")
    if arg.lower() == "init":
        print(f"Initiliazing Grades for {user}.")
        add_all_existing()
    elif arg.lower() == "fetch":
        print(f"Fetching Grades for {user}.")
        nums = load_nums()
        while True:
            print(".", end="", flush=True)
            check(nums)
            sleep(300)
