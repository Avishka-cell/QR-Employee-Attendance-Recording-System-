# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for

import pymysql
import logging

logging.basicConfig(level=logging.DEBUG) 

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

# Function to check if data already exists in the database
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

# Function to insert form data into the database
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

# Function to fetch employee details from the database
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

# Function to delete employee data from the database
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

# Function to fetch employee details by ID
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



# Route to submit the form data
@app.route('/register', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        # Extract form data
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

        # Check if data already exists
        existing_data = check_existing_data(id, email, nic)
        if existing_data:
            return '<script>alert("Id, Email, or Nic already exists");window.location.href="/empDtls";</script>'

        # Insert data if it doesn't exist
        data = (id, fname, lname, tpnumber, email, gender, address, nic, city, marital, position, dob)
        insert_data(data)
        return  '<script>alert("Id, Email, or Nic already exists");window.location.href="/empDtls";</script>'

# Route to display employee details
@app.route('/empDtls')
def empDtls():
    employees = fetch_employee_details()
    return render_template('empDtls.html', employees=employees)

# Route to handle delete employee request
@app.route('/delete/<int:employee_id>', methods=['POST'])
def delete_employee_route(employee_id):
    if delete_employee(employee_id):
        return redirect(url_for('empDtls'))
    else:
        return 'Failed to delete employee'
    
    

# Route to handle edit employee request
@app.route('/edit/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    if request.method == 'GET':
        employee = fetch_employee_by_id(employee_id)
        if employee:
            return render_template('edit.html', employee=employee)
        else:
            return 'Employee not found'
    elif request.method == 'POST':
        # Update employee data in the database
        # Extract form data
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

        # Update employee data
        try:
            conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
            cursor = conn.cursor()
            sql = "UPDATE empdtls SET fname=%s, lname=%s, tpnumber=%s, email=%s, gender=%s, address=%s, nic=%s, city=%s, marital=%s, position=%s, dob=%s WHERE id=%s"
            cursor.execute(sql, (fname, lname, tpnumber, email, gender, address, nic, city, marital, position, dob, id))
            conn.commit()
            conn.close()
            return redirect(url_for('empDtls'))
        except pymysql.Error as e:
            print("Error while updating employee:", e)
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
                return '<script>alert("Employee already has a schedule!");window.location.href="/shedule";</script>'
            else:
                data = (id, at, dt,fd,td)
                if insert_schedule_data(data):
                    return '<script>alert("Schedule submitted successfully!");window.location.href="/shedule";</script>'
                else:
                    return '<script>alert("Error inserting schedule data!");window.location.href="/shedule";</script>'
        else:
            return '<script>alert("Employee ID does not exist!");window.location.href="/shedule";</script>'

#shedule end


# display shedule
def fetch_schedule_data():
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM shedule"
        cursor.execute(sql)
        schedules = cursor.fetchall()
        conn.close()
        return schedules
    except pymysql.Error as e:
        logging.error(f"Error while fetching schedule data: {e}")
        return []

@app.route('/scheduleDtls')
def display_schedules():
    schedules = fetch_schedule_data()
    return render_template('scheduleDtls.html', schedules=schedules)


#delete schedule
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

# Route to handle delete schedule request
@app.route('/delete-schedule/<int:schedule_id>', methods=['POST'])
def delete_schedule_route(schedule_id):
    if delete_schedule(schedule_id):
        return 'OK', 200
    else:
        return 'Failed', 500


#edit schedule details
# Route to handle GET and POST requests for editing schedule
# Function to fetch schedule details by ID from the database
def fetch_schedule_by_id(schedule_id):
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM shedule WHERE id = %s"
        cursor.execute(sql, (schedule_id,))
        schedule = cursor.fetchone()
        conn.close()
        return schedule
    except pymysql.Error as e:
        print("Error while fetching schedule details by ID:", e)
        return None


@app.route('/edit-schedule/<int:schedule_id>', methods=['GET', 'POST'])
def edit_schedule(schedule_id):
    if request.method == 'GET':
        # Fetch schedule data by ID
        schedule = fetch_schedule_by_id(schedule_id)
        if schedule:
            return render_template('editShedule.html', schedule=schedule)
        else:
            return 'Schedule not found'
    elif request.method == 'POST':
        # Update schedule data in the database
        # Extract form data
        arrival = request.form['at']
        departure = request.form['dt']
        fromDate = request.form['fd']
        toDate = request.form['td']
        # Update schedule data
        try:
            conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
            cursor = conn.cursor()
            sql = "UPDATE shedule SET arrival=%s, depature=%s, fromDate=%s, toDate=%s WHERE id=%s"
            cursor.execute(sql, (arrival, departure, fromDate, toDate, schedule_id))
            conn.commit()
            conn.close()
            return redirect(url_for('display_schedules'))  # Redirect to schedule details page
        except pymysql.Error as e:
            print("Error while updating schedule:", e)
            return 'Failed to update schedule'

#edit schedule details 


# Existing routes...

# display shedule end

#leave sart  


# Function to insert leave data into the database
def insert_leave_data(data):
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conn.cursor()
        sql = "INSERT INTO leavedtls (id, fromdate, todate, noOfDates) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, data)
        conn.commit()
        conn.close()
        logging.info("Leave data inserted successfully")
        return True
    except pymysql.Error as e:
        logging.error(f"Error while inserting leave data: {e}")
        return False

def check_leave_exists(id):
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conn.cursor()
        sql = "SELECT * FROM leavedtls WHERE id = %s"
        cursor.execute(sql, (id,))
        leave = cursor.fetchone()
        conn.close()
        return leave is not None
    except pymysql.Error as e:
        logging.error(f"Error while checking leave data: {e}")
        return False

@app.route('/submit-leave', methods=['POST'])
def submit_leave():
    if request.method == 'POST':
        id = request.form['id']
        fromdate = request.form['fromdate']
        todate = request.form['todate']
        noOfDates = request.form['nd']

        logging.debug(f"Received leave form data - ID: {id}, From Date: {fromdate}, To Date: {todate}, Number of Days: {noOfDates}")

        if check_leave_exists(id):
            return '<script>alert("Employee already applied leaves!");window.location.href="/leaveDtls";</script>'
        else:
            data = (id, fromdate, todate, noOfDates)
            if insert_leave_data(data):
                return '<script>alert("Leave submitted successfully!");window.location.href="/leaveDtls";</script>'
            else:
                return '<script>alert("Error inserting leave data!");window.location.href="/leaveDtls";</script>'

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
#leave end  




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
        conn.close()
        return attendance
    except pymysql.Error as e:
        logging.error(f"Error while fetching attendance details: {e}")
        return []

@app.route('/attendance')
def display_attendance():
    attendance = fetch_attendance_details()
    return render_template('attendance.html', attendance=attendance)
#end 

#fetch leave details 

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
def display_leaves():
    leaves = fetch_leave_data()
    return render_template('leaveDtls.html', leaves=leaves)
#end

#absent start 
def fetch_absent_employees():
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # SQL query to fetch employees who are absent and their schedule details
        sql = """
            SELECT e.id, e.fname, e.tpnumber, e.email, e.position, s.arrival, s.depature
            FROM empdtls e
            LEFT JOIN attendance a ON e.id = a.id
            LEFT JOIN leavedtls l ON e.id = l.id
            LEFT JOIN shedule s ON e.id = s.id
            WHERE a.id IS NULL AND l.id IS NULL
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
    return render_template('absentEmployees.html', employees=absent_employees)


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

@app.route('/dash')
def dash():
    counts = get_counts()
    return render_template('dash.html', counts=counts)

#dash end

# Routes for other pages
@app.route('/leave')
def leave():
    return render_template('addleave.html')

# @app.route('/dash')
# def dash():
#     return render_template('dash.html')

@app.route('/reg')
def registration():
    return render_template('reg.html')


@app.route('/shedule')
def shedule():
    return render_template('newShedule.html')


if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode

