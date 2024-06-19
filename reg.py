# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for,jsonify
from datetime import datetime
import pymysql
import logging
from flask_sqlalchemy import SQLAlchemy


logging.basicConfig(level=logging.DEBUG) 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask app
app = Flask(__name__)

# Database configuration
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'abc'

# Function to authenticate users
def authenticate(username, password):
    return username == 'admin' and password == 'admin@123'

def check_existing_data(id, email, nic):
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conn.cursor()
        sql = "SELECT * FROM empdtls WHERE id = %s OR email = %s OR nic = %s"
        cursor.execute(sql, (id, email, nic))
        existing_data = cursor.fetchone()
        conn.close()
        return existing_data
    except pymysql.Error as e:
        print("Error while checking existing data:", e)
        return None

def insert_data(data):
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conn.cursor()
        sql = "INSERT INTO empdtls (id, fname, lname, tpnumber, email, gender, address, nic, city, marital, position, dob) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, data)
        conn.commit()
        conn.close()
    except pymysql.Error as e:
        print("Error while inserting data:", e)

def fetch_employee_details():
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM empdtls"
        cursor.execute(sql)
        employees = cursor.fetchall()
        conn.close()
        return employees
    except pymysql.Error as e:
        print("Error while fetching employee details:", e)
        return []

def delete_employee(employee_id):
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conn.cursor()
        sql = "DELETE FROM empdtls WHERE id = %s"
        cursor.execute(sql, (employee_id,))
        conn.commit()
        conn.close()
        print("Employee deleted successfully")
        return True
    except pymysql.Error as e:
        print("Error while deleting employee:", e)
        return False

def fetch_employee_by_id(employee_id):
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM empdtls WHERE id = %s"
        cursor.execute(sql, (employee_id,))
        employee = cursor.fetchone()
        conn.close()
        return employee
    except pymysql.Error as e:
        print("Error while fetching employee details by ID:", e)
        return None

@app.route('/register', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        id = request.form['id']
        fname = request.form['fname']
        lname = request.form['lname']
        tpnumber = request.form['tp']
        email = request.form['email']
        gender = request.form['gender']
        address = request.form['address']
        nic = request.form['nic']
        city = request.form['city']
        marital = request.form['marital']
        position = request.form['position']
        dob = request.form['dob']

        existing_data = check_existing_data(id, email, nic)
        if existing_data:
            return '<script>alert("Id, Email, or Nic already exists");window.location.href="/empDtls";</script>'

        data = (id, fname, lname, tpnumber, email, gender, address, nic, city, marital, position, dob)
        insert_data(data)
        return  '<script>alert("Registration Successful");window.location.href="/empDtls";</script>'

@app.route('/empDtls')
def empDtls():
    employees = fetch_employee_details()
    return render_template('empDtls.html', employees=employees)

@app.route('/delete/<int:employee_id>', methods=['POST'])
def delete_employee_route(employee_id):
    if delete_employee(employee_id):
        return redirect(url_for('empDtls'))
    else:
        return 'Failed to delete employee'
    
@app.route('/edit/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    if request.method == 'GET':
        employee = fetch_employee_by_id(employee_id)
        if employee:
            return render_template('edit.html', employee=employee)
        else:
            return 'Employee not found'
    elif request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        tpnumber = request.form['tp']
        email = request.form['email']
        gender = request.form['gender']
        address = request.form['address']
        nic = request.form['nic']
        city = request.form['city']
        marital = request.form['marital']
        position = request.form['position']
        dob = request.form['dob']

        try:
            conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
            cursor = conn.cursor()
            sql = "UPDATE empdtls SET fname=%s, lname=%s, tpnumber=%s, email=%s, gender=%s, address=%s, nic=%s, city=%s, marital=%s, position=%s, dob=%s WHERE id=%s"
            cursor.execute(sql, (fname, lname, tpnumber, email, gender, address, nic, city, marital, position, dob, employee_id))
            conn.commit()
            conn.close()
            return redirect(url_for('empDtls'))
        except pymysql.Error as e:
            print("Error while updating employee details:", e)
            return 'Failed to update employee'

        
        
    # shedule start    

def insert_schedule_data(data):
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conn.cursor()
        sql = "INSERT INTO shedule (id, arrival, depature,fromDate,	toDate) VALUES (%s, %s, %s,%s,%s)"
        cursor.execute(sql, data)
        conn.commit()
        conn.close()
        logging.info("Data inserted successfully")
        return '<script>alert("Employee already has a schedule!");window.location.href="/reg";</script>'
    except pymysql.Error as e:
        logging.error(f"Error while inserting data: {e}")
        return False

# Function to check if employee ID exists in empdtls table
def check_employee_id(employee_id):
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM empdtls WHERE id = %s"
        cursor.execute(sql, (employee_id,))
        employee = cursor.fetchone()
        conn.close()
        return employee is not None
    except pymysql.Error as e:
        logging.error(f"Error while fetching employee details by ID: {e}")
        return False

# Function to check if employee ID already has a schedule
def check_schedule_exists(employee_id):
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM shedule WHERE id = %s"
        cursor.execute(sql, (employee_id,))
        schedule = cursor.fetchone()
        conn.close()
        return schedule is not None
    except pymysql.Error as e:
        logging.error(f"Error while checking schedule: {e}")
        return False

@app.route('/submit-schedule', methods=['POST'])
def submit_schedule():
    if request.method == 'POST':
        id = request.form['id']
        at = request.form['at']
        dt = request.form['dt']
        fd = request.form['fd']
        td = request.form['td']
        logging.debug(f"Received form data - ID: {id}, Arrival Time: {at}, Departure Time: {dt},FD:{fd},td:{td}")

        # Check if employee ID exists
        if check_employee_id(id):
            # Check if schedule already exists for this employee
            if check_schedule_exists(id):
                return '<script>alert("Employee already has a schedule!");window.location.href="/scheduleDtls";</script>'
            else:
                data = (id, at, dt,fd,td)
                if insert_schedule_data(data):
                    return '<script>alert("Schedule submitted successfully!");window.location.href="/scheduleDtls";</script>'
                else:
                    return '<script>alert("Error inserting schedule data!");window.location.href="/scheduleDtls";</script>'
        else:
            return '<script>alert("Employee ID does not exist!");window.location.href="/shedule";</script>'

#shedule end


# display shedule
def fetch_schedule_data():
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM shedule")
        schedules = cursor.fetchall()
        for schedule in schedules:
            schedule['arrival'] = str(schedule['arrival'])
            schedule['depature'] = str(schedule['depature'])
            schedule['fromDate'] = schedule['fromDate'].strftime('%Y-%m-%d')
            schedule['toDate'] = schedule['toDate'].strftime('%Y-%m-%d')
        conn.close()
        return schedules
    except pymysql.Error as e:
        print("Error while fetching schedules:", e)
        return []

def fetch_schedule_by_id(schedule_id):
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM shedule WHERE id = %s"
        cursor.execute(sql, (schedule_id,))
        schedule = cursor.fetchone()
        if schedule:
            schedule['arrival'] = str(schedule['arrival'])
            schedule['depature'] = str(schedule['depature'])
            schedule['fromDate'] = schedule['fromDate'].strftime('%Y-%m-%d')
            schedule['toDate'] = schedule['toDate'].strftime('%Y-%m-%d')
        conn.close()
        return schedule
    except pymysql.Error as e:
        print("Error while fetching schedule details by ID:", e)
        return None

@app.route('/scheduleDtls')
def display_schedules():
    schedules = fetch_schedule_data()
    return render_template('scheduleDtls.html', schedules=schedules)

@app.route('/edit-schedule/<int:schedule_id>', methods=['POST'])
def edit_schedule(schedule_id):
    if request.method == 'GET':
        schedule = fetch_schedule_by_id(schedule_id)
        if schedule:
            return render_template('editShedule.html', schedule=schedule)
        else:
            return 'Schedule not found'
    elif request.method == 'POST':
        arrival = request.form['at']
        departure = request.form['dt']
        fromDate = request.form['fd']
        toDate = request.form['td']
        try:
            conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
            cursor = conn.cursor()
            sql = "UPDATE shedule SET arrival=%s, depature=%s, fromDate=%s, toDate=%s WHERE id=%s"
            cursor.execute(sql, (arrival, departure, fromDate, toDate, schedule_id))
            conn.commit()
            conn.close()
            return redirect(url_for('display_schedules'))
        except pymysql.Error as e:
            print("Error while updating schedule:", e)
            return 'Failed to update schedule'

def delete_schedule(schedule_id):
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conn.cursor()
        sql = "DELETE FROM shedule WHERE id = %s"
        cursor.execute(sql, (schedule_id,))
        conn.commit()
        conn.close()
        logging.info("Schedule deleted successfully")
        return True
    except pymysql.Error as e:
        logging.error(f"Error while deleting schedule: {e}")
        return False

@app.route('/edit-schedule', methods=['POST'])
def edit_schedule_submit():
    if request.method == 'POST':
        schedule_id = request.form['id']
        arrival = request.form['at']
        departure = request.form['dt']
        fromDate = request.form['fd']
        toDate = request.form['td']
        try:
            conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
            cursor = conn.cursor()
            sql = "UPDATE shedule SET arrival=%s, depature=%s, fromDate=%s, toDate=%s WHERE id=%s"
            cursor.execute(sql, (arrival, departure, fromDate, toDate, schedule_id))
            conn.commit()
            conn.close()
            return redirect(url_for('display_schedules'))
        except pymysql.Error as e:
            print("Error while updating schedule:", e)
            return 'Failed to update schedule'



#edit schedule details 


#login

app.secret_key = 'your_secret_key'  # Required for flash messages

# Existing routes and functions...

# Function to authenticate users
def authenticate(username, password):
    return username == 'admin' and password == 'pass@123'

# Route to handle login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if authenticate(username, password):
            return redirect(url_for('dash'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    
    return render_template('login.html')


#login end 

#feten attendance details  
def fetch_attendance_details():
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM attendance"
        cursor.execute(sql)
        attendance = cursor.fetchall()
        
        for record in attendance:
            arrival = record['arrival']  # Assuming 'arrival' is already a datetime object
            departure = record['depature']  # Assuming 'depature' is already a datetime object
            working_hours = departure - arrival
            record['workinghrs'] = working_hours
        
        conn.close()
        return attendance
    except pymysql.Error as e:
        logging.error(f"Error while fetching attendance details: {e}")
        return []

@app.route('/attendance')
def display_attendance():
    attendance = fetch_attendance_details()
    return render_template('attendance.html', attendance=attendance)




#absent start 
def fetch_absent_employees():
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # SQL query to fetch employees who are absent and their schedule details
        sql = """
            SELECT e.id, e.fname, e.tpnumber, e.email, e.position, s.arrival, s.depature, s.fromDate
            FROM empdtls e
            LEFT JOIN attendance a ON e.id = a.id
            LEFT JOIN leavedtls l ON e.id = l.id
            LEFT JOIN shedule s ON e.id = s.id
            WHERE (a.date IS NULL OR a.date = CURDATE()) AND l.id IS NULL
        """
        
        cursor.execute(sql)
        absent_employees = cursor.fetchall()
        conn.close()
        return absent_employees
    except pymysql.Error as e:
        logging.error(f"Error while fetching absent employees: {e}")
        return []

@app.route('/absentEmployees')
def display_absent_employees():
    absent_employees = fetch_absent_employees()
    current_date = datetime.now().strftime('%Y-%m-%d')
    return render_template('absentEmployees.html', employees=absent_employees, current_date=current_date)


#leave start
def insert_leave_data(data):
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conn.cursor()
        
        # Check if ID exists in accept table with status 'accepted'
        sql_check_accepted = "SELECT COUNT(*) FROM accept WHERE id = %s AND status = 'accepted'"
        cursor.execute(sql_check_accepted, (data[0],))
        accepted_count = cursor.fetchone()[0]

        if accepted_count == 0:
            logging.error("Leave request cannot be submitted: ID does not exist in accept table with status 'accepted'.")
            conn.close()
            return False

        # Insert leave data
        sql = "INSERT INTO leavedtls (id, name, email, leavetype, stDate, endDate, noDate, reason) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, data)
        conn.commit()
        conn.close()
        logging.info("Leave data inserted successfully")
        return True
    except pymysql.Error as e:
        logging.error(f"Error while inserting leave data: {e}")
        return False

@app.route('/leave', methods=['POST'])
def submit_leave():
    if request.method == 'POST':
        id = request.form.get('employeeId')
        name = request.form.get('employeeName')
        email = request.form.get('employeeEmail')
        leavetype = request.form.get('leaveType')
        stDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        reason = request.form.get('reason')

        logging.debug(f"Received leave form data - ID: {id}, Name: {name}, Email: {email}, Leave Type: {leavetype}, Start Date: {stDate}, End Date: {endDate}, Reason: {reason}")

        # Validate the dates
        try:
            start_date = datetime.strptime(stDate, '%y-%m-%d')
            end_date = datetime.strptime(endDate, '%y-%m-%d')
        except ValueError as e:
            logging.error(f"Date format error: {e}")
            return '<script>alert("Leave submitted successfully");window.location.href="/leaveform";</script>'

        # Calculate number of days
        noDate = (end_date - start_date).days + 1  # Including both start and end dates

        data = (id, name, email, leavetype, stDate, endDate, noDate, reason)
        if insert_leave_data(data):
            return '<script>alert("Leave submitted successfully!");window.location.href="/leaveform";</script>'
        else:
            return '<script>alert("Leave submitted successfully");window.location.href="/leaveform";</script>'

def fetch_leave_data():
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM leavedtls"
        cursor.execute(sql)
        leaves = cursor.fetchall()
        conn.close()
        return leaves
    except pymysql.Error as e:
        logging.error(f"Error while fetching leave data: {e}")
        return []

@app.route('/leaveDtls')
def leave_details():
    leaves = fetch_leave_data()
    return render_template('leaveDtls.html', leaves=leaves)

def insert_accept_data(data):
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conn.cursor()
        sql = "INSERT INTO accept (id, name, email, leavetype, stDate, endDate, noDate, reason, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, data)
        conn.commit()
        conn.close()
        logging.info("Leave data inserted successfully")
        return True
    except pymysql.Error as e:
        logging.error(f"Error while inserting leave data: {e}")
        return False










def fetch_accept_data():
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM accept"
        cursor.execute(sql)
        data = cursor.fetchall()
        conn.close()
        return data
    except pymysql.Error as e:
        logging.error(f"Error while fetching accept data: {e}")
        return []

@app.route('/accept_details')
def accept_details():
    data = fetch_accept_data()
    return render_template('accept_details.html', data=data)



#summary 



#summary end 

#chart start
# Fetch attendance data


#chart end 

#end

#dash start
def get_counts():
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        # Fetch total employees
        cursor.execute("SELECT COUNT(*) AS employee_count FROM empdtls")
        employee_count = cursor.fetchone()['employee_count']
        
        # Fetch total leaves
        cursor.execute("SELECT COUNT(*) AS leave_count FROM leavedtls")
        leave_count = cursor.fetchone()['leave_count']
        
        # Fetch absent today
        cursor.execute("""
            SELECT COUNT(*) AS absent_count 
            FROM empdtls e
            LEFT JOIN attendance a ON e.id = a.id
            LEFT JOIN leavedtls l ON e.id = l.id
            LEFT JOIN shedule s ON e.id = s.id
            WHERE a.id IS NULL AND l.id IS NULL
        """)
        absent_count = cursor.fetchone()['absent_count']
        
        conn.close()
        
        counts = {
            'employee_count': employee_count,
            'leave_count': leave_count,
            'absent_count': absent_count
        }
        return counts
        
    except pymysql.Error as e:
        logging.error(f"Error while fetching counts: {e}")
        return {
            'employee_count': 0,
            'leave_count': 0,
            'absent_count': 0
        }

@app.route('/summary')
def index():
    counts = get_counts()
    
    # Fetch detailed employee data
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("""
            SELECT e.id, e.fname, e.position, 
                   (SELECT COUNT(*) FROM leavedtls l WHERE l.id = e.id) AS number_of_leaves,
                   (SELECT COUNT(*) FROM attendance a WHERE a.id = e.id) AS number_of_days_attend,
                   (SELECT COUNT(*) FROM shedule s WHERE s.id = e.id) - (SELECT COUNT(*) FROM attendance a WHERE a.id = e.id) AS number_of_absent
            FROM empdtls e
        """)
        
        employees = cursor.fetchall()
        conn.close()
        
    except pymysql.Error as e:
        logging.error(f"Error while fetching employee details: {e}")
        employees = []
    
    return render_template('employee_details.html', counts=counts, employees=employees)









@app.route('/dash')
def dash():
    counts = get_counts()
    return render_template('dash.html', counts=counts)

#dash end

# Routes for other pages


# @app.route('/dash')
# def dash():
#     return render_template('dash.html')

@app.route('/reg')
def registration():
    return render_template('reg.html')


@app.route('/shedule')
def shedule():
    return render_template('newShedule.html')

@app.route('/emplog')
def emplog():
    return render_template('empLog.html')

@app.route('/leaveform')
def leaveform():
    return render_template('leave.html')

@app.route('/summary')
def summary():
    return render_template('accept_details.html')

@app.route('/qr')
def qr():
    return render_template('qr.html')




if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode

