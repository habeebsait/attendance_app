from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options

from datetime import datetime

today = datetime.now()
day_name = today.strftime("%A")
# export GMAIL_PASSWORD="ldgeekzegduqbzqn"


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


app = Flask(__name__)

@app.route('/scrape-attendance', methods=['GET'])
def scrape_attendance():
    usn = request.args.get('usn')  # Get the username from query parameter
    print(usn)
    day_value = request.args.get('day')  # Get the day value from query parameter
    print(day_value)
    month_value = request.args.get('month')  # Get the month value from query parameter
    print(month_value)
    year_value = request.args.get('year')  # Get the year value from query parameter
    print(year_value)

    # Validate parameters
    if not usn:
        return jsonify({'error': 'USN parameter is required'}), 400
    if not day_value:
        return jsonify({'error': 'Day parameter is required'}), 400
    if not month_value:
        return jsonify({'error': 'Month parameter is required'}), 400
    if not year_value:
        return jsonify({'error': 'Year parameter is required'}), 400

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("detach", True)
    
    # Replace path with your chromedriver's path if necessary
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://parents.msrit.edu/newparents/")

        # Input USN
        usn_field = driver.find_element(By.XPATH, '//*[@id="username"]')
        usn_field.send_keys(usn)

        # Select day
        day_option = driver.find_element(By.XPATH, f'//*[@id="dd"]/option[{day_value}]')
        day_option.click()

        # Select month
        month_option = driver.find_element(By.XPATH, f'//*[@id="mm"]/option[{month_value}]')
        month_option.click()

        # Select year
        year_option = driver.find_element(By.XPATH, f'//*[@id="yyyy"]/option[{year_value}]')
        year_option.click()

        # Submit the login form
        login = driver.find_element(By.XPATH, '//*[@id="login-form"]/div[3]/input[1]')
        login.click()

        # Wait for the button to appear and click it
        button = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/p/button"))
        )
        button.click()

        # Allow some time for the page to load
        time.sleep(5)

        # Scrape subjects
        subjects = []
        for i in range(1, 11):
            cell = driver.find_element(By.XPATH, f'//*[@id="page_bg"]/div[1]/div/div/div[5]/div/div/div/table/tbody/tr[{i}]/td[2]')
            subject = driver.execute_script("return arguments[0].textContent;", cell)
            subjects.append(subject)

        # Scrape attendance
        attendance = []
        for i in range(1, 11):
            attendance.append(driver.find_element(By.XPATH, f'//*[@id="page_bg"]/div[1]/div/div/div[5]/div/div/div/table/tbody/tr[{i}]/td[5]/a/button').text)

        driver.quit()
        
    
       
        from smtplib import SMTP
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        server = SMTP('smtp.gmail.com', 587)
        server.starttls()

        sender_email = "habeebsait04@gmail.com"
        password = "ldgeekzegduqbzqn"

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

        return jsonify({'subjects': subjects, 'attendance': attendance})

    except Exception as e:
        driver.quit()
        return jsonify({'error': str(e)}), 500
    
    


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)

