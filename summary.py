
from flask import Flask, render_template, request, redirect, url_for
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