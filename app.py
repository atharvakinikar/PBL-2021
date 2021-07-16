import email
import smtplib
from datetime import datetime
import csv
import requests
from csv import writer
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/index',methods = ['POST', 'GET'])
def student():
   if request.method== 'POST':
    username=request.form.get("name")
    password=request.form.get("password")
    List=[username,password]
    with open('loginsheet.csv', 'a', newline='') as f_object:
  
    # Pass this file object to csv.writer()
    # and get a writer object
      writer_object = writer(f_object)
  
    # Pass the list as an argument into
    # the writerow()
      writer_object.writerow(List)
  
    #Close the file object
      f_object.close()
   return render_template('index.html')
   
@app.route('/register.html')
def student1():
   return render_template('register.html')
   
@app.route('/1',methods = ['POST', 'GET'])
def vaccinationform():
   if request.method == 'POST':
      check=0
      username=request.form.get("email")
      password=request.form.get("password")
      filename = "loginsheet.csv"
      rows = []
      with open(filename, 'r') as csvfile:
      # creating a csv reader object
        csvreader = csv.reader(csvfile)
      
      # extracting field names through first row
        fields = next(csvreader)
  
      # extracting each data row one by one
        for row in csvreader:
          rows.append(row)

      for row in rows[:100]:
        if((row[0]==username) and (row[1]==password)):
          check=1 
          return render_template("1.html")
          
      if(check==0):
        return render_template("invalid.html")


@app.route('/typography.html')
def typography_page():
   return render_template('typography.html')


@app.route('/1.html')
def dashboard_page():
   return render_template('1.html')


@app.route('/index.html')
def logout_page():
   return render_template('index.html')

   
@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      def create_session_info(center, session):
          return {"name": center["name"],
            "date": session["date"],
            "capacity": session["available_capacity"],
            "age_limit": session["min_age_limit"]}

      def get_sessions(data):
          for center in data["centers"]:
            for session in center["sessions"]:
              yield create_session_info(center, session)

      def is_available(session):
        return session["capacity"] > 0

      def is_eighteen_plus(session):
       return session["age_limit"] == 18

      def get_for_seven_days(start_date,districtId):
        url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
        params = {"district_id": districtId, "date": start_date.strftime("%d-%m-%Y")}
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
        resp = requests.get(url, params=params, headers=headers)
        data = resp.json()
        return [session for session in get_sessions(data) if is_eighteen_plus(session) and is_available(session)]

      def create_output(session_info):
        return f"{session_info['date']} - {session_info['name']} ({session_info['capacity']})"
      emailid = request.form.get("email")
      districtName=request.form.get("districtName")
      thisdict ={
      "Ahmednagar":391,
      "Akola":364,
      "Amravati":366,
      "Aurangabad":397,
      "Beed":384,
      "Bhandara":370,
      "Buldhana":367,
      "Chandrapur":380,
      "Dhule":388,
      "Gadchiroli":379,
      "Gondia":378,
      "Hingoli":386,
      "Jalgaon":390,
      "Jalna":396,
      "Kolhapur":371,
      "Latur":383,
      "Mumbai":395,
      "Nagpur":365,
      "Nanded":382,
      "Nandurbar":387,
      "Nashik":389,
      "Osmanabad":381,
      "Palghar":394,
      "Parbhani":385,
      "Pune": 363,
      "Raigad":393,
      "Ratnagiri":372,
      "Sangli":373,
      "Satara":376,
      "Sindhudurg":374,
      "Solapur":375,
      "Thane":392,
      "Wardha":377,
      "Washim":369,
      "Yavatmal":368
      }
      districtId = thisdict.get(districtName)
      content = "\n".join([create_output(session_info) for session_info in get_for_seven_days(datetime.today(),districtId)])
      username = "pictpbl@gmail.com"
      password = "pictpbl@2021"
      global email_msg
      if not content:
          print("No availability")
      else:
          email_msg = email.message.EmailMessage()
          email_msg["Subject"] = "Vaccination Slot Open"
          email_msg["From"] = username
          email_msg["To"] = emailid
          email_msg.set_content(content)

      with smtplib.SMTP(host='smtp.gmail.com', port='587') as server:
        server.starttls()
        server.login(username, password)
        server.send_message(email_msg, username, emailid)

   return render_template("result.html")





