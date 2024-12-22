from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import os

today = datetime.now()
day_name = today.strftime("%A")
# export GMAIL_PASSWORD="ldgeekzegduqbzqn"

gmail = os.getenv("GMAIL")
gmail_pass = os.getenv("GMAIL_PASSWORD")


timetable = {
    "Monday": [
        "Natural Language Processing",
        "Computer Organization and Architecture",
        "Research Methodology & Intellectual Property Rights",
        "Operating Systems"
    ],
    "Tuesday": [
        "Natural Language Processing",
        "Computer Organization and Architecture",
        "Fundamentals of Data Science",
        "Introduction to Machine Learning"
    ],
    "Wednesday": [
        "Introduction to Machine Learning",
        "Operating Systems",
        "Fundamentals of Data Science",
        "Computer Organization and Architecture",
        "Research Methodology & Intellectual Property Rights",
        "Natural Language Processing"
    ],
    "Thursday": [
        "Machine Learning Laboratory",
        "Introduction to Machine Learning",
        "Fundamentals of Data Science",
        "Operating Systems",
        "Environmental Studies"
    ],
    "Friday": [
        "Fundamentals of Data Science",
        "Research Methodology & Intellectual Property Rights",
        "Natural Language Processing Laboratory"
    ],
    "Saturday": [
        "Operating Systems",
        "Natural Language Processing",
        "Data Visualization using Power BI"
    ],
    "Sunday": [
       ""
    ]
}



options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")
# options.add_argument("--disable-extensions")
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
driver.get(url= "https://parents.msrit.edu/newparents/")

usn = driver.find_element(By.XPATH, value = '//*[@id="username"]')
usn.send_keys("1ms22ai032")


day = driver.find_element(By.XPATH, value='//*[@id="dd"]/option[5]')
day.click()

month = driver.find_element(By.XPATH, value= '//*[@id="mm"]/option[2]')
month.click()

year = driver.find_element(By.XPATH, value= '//*[@id="yyyy"]/option[43]')
year.click()

login = driver.find_element(By.XPATH, value= '//*[@id="login-form"]/div[3]/input[1]')
login.click()



button = WebDriverWait(driver, 100).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/p/button"))
)
button.click()


subjects = []
for i in range(1,11):
    cell = driver.find_element(By.XPATH, f'//*[@id="page_bg"]/div[1]/div/div/div[5]/div/div/div/table/tbody/tr[{i}]/td[2]')
    text = driver.execute_script("return arguments[0].textContent;", cell)
    subjects.append(text)

time.sleep(3)

attendance = []
for i in range(1,11):
    attendance.append(driver.find_element(By.XPATH,f'//*[@id="page_bg"]/div[1]/div/div/div[5]/div/div/div/table/tbody/tr[{i}]/td[5]/a/button').text)


# for i in range(10):
#     if subjects[i] in timetable[day_name]:
#         print(subjects[i])
#         print(attendance[i])
        
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

server = SMTP('smtp.gmail.com', 587)
server.starttls()

sender_email = gmail
password = gmail_pass

receiver_email = "habeebsait24@gmail.com"

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = "Attendance!!"

body = ""
for i in range(10):
  if subjects[i] in timetable[day_name]:
    body+=subjects[i]+ ": "
    body+= attendance[i]
    body+= "\n"


msg.attach(MIMEText(body, 'plain'))

text = msg.as_string()
print(text)
server.login(sender_email, password)
server.sendmail(sender_email, receiver_email, text)
# print("mail sent")
server.quit()


driver.quit()
