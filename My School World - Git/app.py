from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from flask import Flask, render_template, request, redirect, url_for, make_response, session, Response, flash, send_from_directory, send_file, jsonify
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from variables import DB_VARS
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from html import unescape
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import date
import secrets
import pandas as pd
import emoji
import re
import shutil
import os
import time
import io
import base64
from PIL import Image
import random
import string
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


x = DB_VARS
app = Flask(__name__)
app.config.from_object(x)
mysql = MySQL(app)


# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'kiranadigopula2708@gmail.com'
app.config['MAIL_PASSWORD'] = 'fprm rraa bqmx kdsz'
app.config['MAIL_DEFAULT_SENDER'] = 'kiranadigopula2708@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = False
mail = Mail(app)





#####   INDEX PAGE FUNCTIONALITIES  #####
# Route to Index Page
@app.route("/")
def index():
    return render_template("index.html")






# Route to Index Contact Us
@app.route("/contact_us", methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        name = request.form.get("name").strip()
        email = request.form.get("email").strip()
        subject = request.form.get("subject").strip()
        message = request.form.get("message").strip()
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO help_desk (name, email, subject, message) VALUES (%s, %s, %s, %s)", (name, email, subject, message))
            mysql.connection.commit()
            cur.close()
            try:
                msg = Message(
                "Issue Raised",
                sender="kiranadigopula2708@gmail.com",
                recipients=[email]
            )
                msg.body = f"""Dear {name},
                        
        You Have Raised an Issue.
                            
        Issue Raised Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        Issue: {message}

        Our Team will get back with the Issue within 2 - 3 working days.

        Thank you,
                            
        MySchool World Team...
        """
                mail.send(msg)
                print("Issue Raised Alert Sent.")
                flash('Login Alert Sent to {email}', 'success')
            except:
                print("Error in sending Issue Raised Alert.")
                flash('Error in sending Issue Raised Alert. Please try again.', 'error')
                return render_template("index.html")
            flash("Message Sent Successfully", "success")
            print("Message Sent Successfully")
            return render_template("index.html")
        except:
            print("Error in Sending Message")
            flash("Error in Sending Message", "error")
            return render_template("index.html")
    return render_template("index.html")

#####   END OF INDEX PAGE FUNCTIONALITIES  #####









#####   ADMIN FUNCTIONALITIES   #####
# Route to Admin Login
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
 cur = mysql.connection.cursor()
 if request.method == 'POST':
     try:
         username = request.form.get("username")
         password = request.form.get("password")
         cur.execute("SELECT * FROM administration WHERE username = %s", (username,))
         admin = cur.fetchone()
         if admin:
             print(f"Admin found: {admin[6]}")
             if admin[10] == password:
                 session['admin'] = admin[1]
                 session['school_ID'] = admin[1]
                 print(admin[6] + " " + "Login Successful")
                 return render_template("admin_dashboard.html", admin=admin)
             else:
                 print("Invalid Admin Password")
                 flash("Invalid Admin Password", "error")
                 return render_template("admin_login.html")
         else:
             print("Invalid Admin Credentials")
             flash("Invalid Credentials", "error")
             return render_template("admin_login.html")
     except Exception as e:
         print(f"Error Occurred in Admin Login: {e}")
         flash("Error Occurred in Login", "error")
         return render_template("admin_login.html")
     finally:
         cur.close()
         # Sending login alert email
         try:
             msg = Message(
                 "Security Alert - Login Check",
                 sender="kiranadigopula2708@gmail.com",
                 recipients=[admin[3]]
             )
             msg.body = f"""Dear {admin[6]},
             
Someone has tried or logged into your account.
                 
Login Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                 
If this wasn't you, please reset your password immediately.
                 
Thank you,
                 
MySchool World...
"""
             mail.send(msg)
             print("Admin Login Alert Sent.")
             flash(f'Login Alert Sent to {admin[3]}', 'success')
         except Exception as e:
             print(f"Error in sending Admin Login Alert: {e}")
             flash('Error sending Login Alert. Please try again.', 'error')
 return render_template("admin_login.html")









# Route to Admin Dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    school_ID = session.get('school_ID')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM administration WHERE school_ID = %s", (school_ID,))
    admin = cur.fetchone()
    if not admin:
        return render_template("admin_login.html")
    return render_template("admin_dashboard.html", admin = admin)








# --------------------------
# STAFF REGISTRATION ROUTE
# --------------------------
@app.route('/staff_registration', methods=['GET', 'POST'])
def staff_registration():
    cur = mysql.connection.cursor()
    cur.execute("SELECT staff_email, staff_mobile, staff_ID, staff_aadhar FROM staff")
    staff = cur.fetchall()
    cur.close()
    try:
        admin = session.get('admin')
        school_ID = session.get('school_ID')
        if not school_ID:
            return redirect(url_for('admin_login'))

        if request.method == 'POST':
            staff_ID = request.form.get("staff_id", "").strip()
            staff_name = request.form.get("staff_name", "").strip()
            staff_aadhar = request.form.get("staff_aadhar", "").strip()
            gender = request.form.get("gender", "").strip()
            standard = request.form.get("standard", "").strip()
            staff_email = request.form.get("staff_email", "").strip()
            staff_mobile = request.form.get("staff_mobile", "").strip()
            qualification = request.form.get("qualification", "").strip()
            date_of_joining = request.form.get("date_of_joining", "")

            if not re.match(r'[^@]+@[^@]+\.[^@]+', staff_email):
                flash('Invalid email address', 'error')
                return render_template("staff_registration.html", school_ID=school_ID)

            if not re.match(r'^[0-9]{10}$', staff_mobile):
                flash('Invalid mobile number', 'error')
                return render_template("staff_registration.html", school_ID=school_ID)

            username = staff_ID
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            otp = ''.join(secrets.choice(string.digits) for _ in range(6))

            if staff_email in [staff[0] for staff in staff] or staff_mobile in [staff[1] for staff in staff] or staff_ID in [staff[2] for staff in staff] or staff_aadhar in [staff[3] for staff in staff]:
                print("Duplicate Entry Not Inserted")
                return redirect(url_for('staff_registration'))
            else:
            
                session['otp'] = otp
                session['otp_time'] = time.time()
                session['pending_staff'] = {
                    'school_ID': school_ID,
                    'admin': admin,
                    'staff_ID': staff_ID,
                    'staff_name': staff_name,
                    'standard': standard,
                    'staff_email': staff_email,
                    'staff_mobile': staff_mobile,
                    'username': username,
                    'password': password,
                    'qualification': qualification,
                    'date_of_joining': date_of_joining,
                    'staff_aadhar': staff_aadhar,
                    'gender': gender
                }

                try:
                    msg = Message('Email Verification',
                                sender='kiranadigopula2708@gmail.com',
                                recipients=[staff_email])
                    msg.body = f'''Dear {staff_name},

    Your OTP: {otp}

    This OTP will expire in 5 minutes.

    Thank You,

    MySchool World...'''
                    mail.send(msg)
                    flash('OTP sent to your email. Please verify!', 'success')
                    return redirect(url_for('verify_otp'))
                except Exception as e:
                    flash('Error sending OTP. Please try again.', 'error')
                    return redirect(url_for('staff_registration'))
    except Exception as e:
        flash('Unexpected error occurred during registration.', 'error')

    return render_template("staff_registration.html", admin=session.get('admin'), school_ID=session.get('school_ID'))










# --------------------------
# VERIFY OTP ROUTE
# --------------------------
@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    school_ID = session.get('school_ID')

    if request.method == 'POST':
        entered_otp = str(request.form.get('otp'))
        expected_otp = session.get('otp')
        otp_time = session.get('otp_time')
        staff_data = session.get('pending_staff')

        if not expected_otp or not otp_time or not staff_data:
            flash('OTP session expired or not set. Please register again.', 'error')
            return redirect(url_for('staff_registration'))

        if time.time() - otp_time > 300:
            flash('OTP has expired. Please click "Resend OTP".', 'error')
            session.pop('otp', None)
            session.pop('otp_time', None)
            return redirect(url_for('verify_otp'))
        

        if entered_otp == expected_otp:
            try:
                cur = mysql.connection.cursor()
                cur.execute("SELECT staff_ID FROM staff WHERE standard = %s", (staff_data['standard'],))
                staff = cur.fetchall()
                if staff:
                    cur.execute(
                        "UPDATE staff SET standard = %s WHERE standard = %s",
                        ("No Standard is Assigned", staff_data['standard'])
                    )
                    mysql.connection.commit()
                cur.execute("""
                    INSERT INTO staff (school_ID, staff_ID, staff_name, staff_aadhar, gender, standard, staff_email, staff_mobile, username, password, qualification, date_of_joining)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    staff_data['school_ID'],
                    staff_data['staff_ID'],
                    staff_data['staff_name'],
                    staff_data['staff_aadhar'],
                    staff_data['gender'],
                    staff_data['standard'],
                    staff_data['staff_email'],
                    staff_data['staff_mobile'],
                    staff_data['username'],
                    staff_data['password'],
                    staff_data['qualification'],
                    staff_data['date_of_joining']
                ))
                mysql.connection.commit()

                try:
                    cur.execute("UPDATE student SET staff_ID = %s WHERE standard = %s",
                                (staff_data['staff_ID'], staff_data['standard']))
                    mysql.connection.commit()
                except Exception as e:
                    print("Error in updating student table:", e)

                cur.close()

                try:
                    msg = Message('Registration Successful',
                                  sender='kiranadigopula2708@gmail.com',
                                  recipients=[staff_data['staff_email']])
                    msg.body = f'''Dear {staff_data['staff_name']},

You are successfully assigned as a staff member in our organization.

Your Staff Login Credentials:

Username: {staff_data['username']}
Password: {staff_data['password']}

Thank You,

MySchool World...
'''
                    mail.send(msg)
                except Exception as e:
                    print("Email sending failed:", e)

                # ✅ Clear session only after successful DB & optional email
                session.pop('pending_staff', None)
                session.pop('otp', None)
                session.pop('otp_time', None)

                flash('Staff registered and credentials sent successfully.', 'success')
                return redirect(url_for('staff_details'))

            except Exception as e:
                print("DB Insert Error:", str(e))
                flash('Error inserting staff data.', 'error')
                return redirect(url_for('staff_registration'))

        else:
            flash('Invalid OTP. Please try again.', 'error')
            return redirect(url_for('verify_otp'))

    return render_template("verify_otp.html", school_ID=school_ID)








# --------------------------
# RESEND OTP ROUTE
# --------------------------
@app.route('/resend_otp', methods=['GET', 'POST'])
def resend_otp():
    print("===== RESEND OTP TRIGGERED =====")  # DEBUG
    staff_data = session.get('pending_staff')
    if not staff_data:
        print("Session Data Not Found")
        flash('Session expired. Please register again.', 'error')
        return redirect(url_for('staff_registration'))

    new_otp = ''.join(secrets.choice(string.digits) for _ in range(6))
    session['otp'] = new_otp
    session['otp_time'] = time.time()

    try:
        msg = Message('Resend OTP - Email Verification',
                      sender='kiranadigopula2708@gmail.com',
                      recipients=[staff_data['staff_email']])
        msg.body = f'''Dear {staff_data['staff_name']},

Your new OTP: {new_otp}

This OTP will expire in 5 minutes.

Thank You,

MySchool World...'''
        mail.send(msg)
        flash('A new OTP has been sent to your email.', 'success')
        print("Resend OTP Mail Sent:", new_otp)
        return redirect(url_for('verify_otp')) 
    except Exception as e:
        flash('Error resending OTP. Please try again later.', 'error')
        print("Error in Resending OTP Mail:", str(e))
    return redirect(url_for('verify_otp'))











# Route to Staff Details
@app.route('/staff_details')
def staff_details():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM staff ORDER BY staff_ID ASC")
    staff = cur.fetchall()
    cur.close()
    return render_template("staff_details.html", staff = staff)










# Route to Update Staff
@app.route('/update_staff/<staff_ID>', methods=['POST'])
def update_staff(staff_ID):
    try:
        # Get the form data, including the new 'gender' field
        update_staff_name = request.form.get("update_staff_name").strip()
        update_standard = request.form.get("update_standard").strip()
        update_qualification = request.form.get("update_qualification").strip()
        update_date_of_joining = request.form.get("update_date_of_joining").strip()
        update_staff_email = request.form.get("update_staff_email").strip()
        update_staff_mobile = request.form.get("update_staff_mobile").strip()
        update_staff_aadhar = request.form.get("update_staff_aadhar").strip()
        update_gender = request.form.get("update_gender").strip()  # Gender added here

        # Open cursor and execute the update query
        cur = mysql.connection.cursor()
        cur.execute("SELECT staff_ID FROM staff WHERE standard = %s", (update_standard,))
        staff = cur.fetchall()

        # If any staff are found with the standard, update them
        if staff:
            cur.execute(
                "UPDATE staff SET standard = %s WHERE standard = %s",
                ("No Standard is Assigned", update_standard)
            )
            mysql.connection.commit()
        cur.execute("""
            UPDATE staff SET 
                staff_name = %s,
                standard = %s, 
                qualification = %s, 
                date_of_joining = %s,
                staff_email = %s, 
                staff_mobile = %s,
                staff_aadhar = %s,
                gender = %s  # Gender update included here
            WHERE staff_ID = %s
        """, (
            update_staff_name, update_standard, update_qualification, update_date_of_joining,
            update_staff_email, update_staff_mobile, update_staff_aadhar, update_gender, staff_ID
        ))

        # Commit and close
        mysql.connection.commit()
        try:
            cur.execute("SELECT DISTINCT standard FROM staff")
            staff_standards = set(row[0] for row in cur.fetchall())  # set of staff standards
            cur.execute("SELECT DISTINCT standard FROM student")
            student_standards = set(row[0] for row in cur.fetchall())  # set of student standards
            if update_standard in staff_standards:
                cur.execute("UPDATE student SET staff_ID = %s WHERE standard = %s", (staff_ID, update_standard))
                mysql.connection.commit()
            # Find standards with students but no staff
            standards_without_staff = student_standards - staff_standards

            for std in standards_without_staff:
                cur.execute("UPDATE student SET staff_ID = %s WHERE standard = %s", ("No Staff is Assigned", std))
                mysql.connection.commit()
                print("Updated student records With the Updation of Staff Details")
        except Exception as e:
            print("Error in Updation of Student Records Along with Staff Details:", e)
        cur.close()
        print("Staff details updated successfully")
        flash("Staff details updated successfully.", "success")
    except Exception as e:
        print("Error updating staff:", e)
        flash("An error occurred while updating staff details.", "error")

    return redirect(url_for('staff_details'))






# Route to Delete Staff
@app.route('/delete_staff/<staff_ID>', methods=['POST'])
def delete_staff(staff_ID):
    if not staff_ID:
        flash("Invalid staff ID for deletion", "error")
        return redirect(url_for('staff_details'))

    try:
        cur = mysql.connection.cursor()

        # Fetch existing staff data, including gender
        cur.execute("SELECT staff_ID, staff_name, staff_aadhar, gender, standard, staff_email, staff_mobile, date_of_joining FROM staff WHERE staff_ID = %s", (staff_ID,))
        staff = cur.fetchone()

        if not staff:
            flash("Staff not found", "error")
            return redirect(url_for('staff_details'))

        staff_with_releaving_date = staff + (date.today(),)

        # Insert into alumni
        cur.execute("""
            INSERT INTO staff_alumni (
                staff_ID, staff_name, staff_aadhar, gender, standard, 
                staff_email, staff_mobile, date_of_joining, date_of_releaving
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, staff_with_releaving_date)
        mysql.connection.commit()

        # Delete from staff
        cur.execute("DELETE FROM staff WHERE staff_ID = %s", (staff_ID,))
        mysql.connection.commit()
        cur.execute("DELETE FROM staff_leaves WHERE staff_ID = %s", (staff_ID,))
        mysql.connection.commit()
        cur.execute("DELETE FROM leave_history WHERE staff_ID = %s", (staff_ID,))
        mysql.connection.commit()
        cur.execute("UPDATE student SET staff_ID = %s WHERE staff_ID = %s", ("No Staff is Assigned", staff_ID, ))
        mysql.connection.commit()
        cur.close()
        print("Staff deleted and archived successfully")
        flash("Staff deleted and archived successfully.", "success")

    except Exception as e:
        print("Error during staff deletion:", e)
        flash("An error occurred while deleting the staff.", "error")

    return redirect(url_for('staff_details'))









# Route to Staff Alumni
@app.route('/staff_alumni')
def staff_alumni():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM staff_alumni ORDER BY date_of_releaving DESC")
    staff_alumni = cur.fetchall()
    cur.close()
    return render_template("staff_alumni.html", staff_alumni = staff_alumni)





    



# Route to Help Desk
@app.route('/help_desk')
def help_desk():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM help_desk ORDER BY ID DESC")
    help_desk = cur.fetchall()
    cur.close()
    return render_template("help_desk.html", help_desk = help_desk)








# Route to Resolve Issue
@app.route('/resolve_issue/<issue_ID>', methods=['GET', 'POST'])
def resolve_issue(issue_ID):
    if request.method == 'POST':
        try:
            response = request.form.get("response").strip()
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM help_desk WHERE ID = %s", (issue_ID,))
            help = cur.fetchone()
            cur.close()

            if help:
                msg = Message(
                    "Issue Resolve Mail",
                    sender="kiranadigopula2708@gmail.com",
                    recipients=[help[2]]
                )
                msg.body = f"""Dear {help[1]},

Your Issue: {help[4]}

Response for your Issue: {response}

Thank you,

MySchool World...
"""
                mail.send(msg)
                print("Resolved Mail Sent.")
                flash(f'Resolve Mail Sent to {help[2]}', 'success')

                # Delete issue after resolving
                try:
                    cur = mysql.connection.cursor()
                    cur.execute("DELETE FROM help_desk WHERE ID = %s", (issue_ID,))
                    mysql.connection.commit()
                    cur.close()
                    print("Resolved Issue Deleted Successfully")
                    return redirect(url_for('help_desk'))
                except Exception as e:
                    print(f"Error in Removing Resolved issue: {e}")
                    flash('Error in Removing Resolved issue', 'error')
                    return redirect(url_for('help_desk'))
        except Exception as e:
            print(f"Error in resolving issue: {e}")
            flash('Error resolving issue', 'error')
            return redirect(url_for('help_desk'))
    return redirect(url_for('help_desk'))









# Route to Leave Requests
@app.route('/leave_requests', methods=['GET', 'POST'])
def leave_requests():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM staff_leaves ORDER BY ID DESC")
    leaves = cur.fetchall()
    disable = None
    cur.execute("SELECT * FROM staff")
    staff = cur.fetchall()

    leave_history = []  # Default to an empty list or None
    row_disables = []
    selected_id = None
    if request.method == 'POST':    
        staff_ID = request.form.get("staff_ID").strip()
        selected_id = staff_ID
        cur.execute("SELECT * FROM leave_history WHERE staff_ID = %s ORDER BY ID DESC", (staff_ID,))
        leave_history = cur.fetchall()
        today_date = datetime.now().date()

        for leave in leave_history:
            start_date = leave[5]  # This must be a `datetime.date` object
            if isinstance(start_date, datetime):  # Convert if necessary
                start_date = start_date.date()
            if start_date <= today_date:
                row_disables.append("disabled")
            else:
                row_disables.append("")
    cur.close()
    return render_template('leave_requests.html', leaves = leaves, staff = staff, row_disables = row_disables, leave_history = leave_history, selected_id = selected_id)










# Route to Update Leave Status
@app.route('/update_leave_status', methods=['POST'])
def update_leave_status():
    leave_id = request.form.get('leave_id').strip()
    new_status = request.form.get('status').strip()
    try:
        if leave_id and new_status:
            cur = mysql.connection.cursor()

            # Check if the leave exists in the 'staff_leaves' table
            cur.execute("SELECT * FROM staff_leaves WHERE ID = %s ORDER BY applied_on DESC", (leave_id,))
            leave = cur.fetchone()

            if leave:
                # Move to history table
                cur.execute(""" 
                    INSERT INTO leave_history (ID, school_ID, staff_ID, staff_name, leave_type, start_date, 
                        end_date, days, applied_on, status) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (leave[0], leave[1], leave[2], leave[3], leave[4], leave[5], leave[6], leave[7], leave[8], new_status))
                mysql.connection.commit()

                # Delete from active requests
                cur.execute("DELETE FROM staff_leaves WHERE ID = %s", (leave_id,))
                mysql.connection.commit()
                print("Moved leave request to history and updated status.")
                
                try:
                    cur.execute("SELECT staff_name, staff_email FROM staff WHERE staff_ID = %s", (leave[2],))
                    staff_data = cur.fetchone()
                    if not staff_data:
                        return redirect(url_for("leave_requests"))
                    staff_name = staff_data[0]
                    staff_email = staff_data[1]
                    msg = Message('Update Regarding Leave Request',
                                sender='kiranadigopula2708@gmail.com',
                                recipients=[staff_email])
                    msg.body = f'''Dear {staff_name},

Your Leave request from {leave[5]} to {leave[6]} has been {new_status}.

Thank You,

MySchool World...
                    '''
                    mail.send(msg)
                    print("Update has been sent to Email")
                    return redirect(url_for('leave_requests', message="success"))
                except Exception as e:
                    print("Update Not Send to Email", e)
                    return redirect(url_for('leave_requests', message="email_failed"))
            
            else:
                # If already in history, update status directly
                cur.execute("UPDATE leave_history SET status = %s WHERE ID = %s", (new_status, leave_id))
                mysql.connection.commit()
                print("Updated status in leave_history.")
                
                try:
                    cur.execute("SELECT * FROM leave_history WHERE ID = %s", (leave_id,))
                    leave = cur.fetchone()
                    cur.execute("SELECT staff_name, staff_email FROM staff WHERE staff_ID = %s", (leave[2],))
                    staff_data = cur.fetchone()
                    if not staff_data:
                        return redirect(url_for("leave_requests"))
                    staff_name = staff_data[0]
                    staff_email = staff_data[1]
                    msg = Message('Update Regarding Leave Request',
                                sender='kiranadigopula2708@gmail.com',
                                recipients=[staff_email])
                    msg.body = f'''Dear {staff_name},

Your Leave request from {leave[5]} to {leave[6]} has been {new_status}.

Thank You,

MySchool World...
                    '''
                    mail.send(msg)
                    print("Update Send to Email")
                    return redirect(url_for('leave_requests', message="success"))
                except Exception as e:
                    print("Update didn't Send to Email", e)
                    return redirect(url_for('leave_requests', message="email_failed"))

            cur.close()
        else:
            return redirect(url_for("leave_requests", message="invalid_data"))
    except Exception as e:
        print("Error: ", e)    
        return redirect(url_for("leave_requests", message="error"))











# Route to Login Credentials of Students and Parents
@app.route('/login_credentials', methods=['GET', 'POST'])
def login_credentials():
    login_credentials = []
    standard = None
    if request.method == 'POST':
        standard = request.form.get("standard").strip()
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT roll_number, student_name, student_username, student_password, username, password, standard 
                FROM student 
                WHERE standard = %s
            """, (standard,))
            login_credentials = cur.fetchall()
        except Exception as e:
            print("Error fetching login credentials:", str(e))
            flash("An error occurred while fetching login credentials.", "danger")
        finally:
            cur.close()

    return render_template("login_credentials.html", login_credentials=login_credentials, standard=standard)


    








# Route to Students Details
@app.route('/students_details_in_admin', methods=["GET", "POST"])
def students_details_in_admin():
    cur = mysql.connection.cursor()

    # Get list of standards
    cur.execute("SELECT DISTINCT standard FROM staff")
    staff_standards = cur.fetchall()

    students = []  # Initialize students as an empty list
    standard = None

    if request.method == "POST":
        # Get the selected standard from the form
        standard = request.form.get("standard").strip()
        
        # Fetch students based on the selected standard
        if standard:
            cur.execute("SELECT * FROM student WHERE standard = %s ORDER BY roll_number ASC", (standard,))
            students = cur.fetchall()  # Assign the result of cur.fetchall() to the students list
            print(f"Fetched students: {students}")
    cur.close()

    return render_template(
        "students_details_in_admin.html",
        staff_standards=staff_standards,
        students=students,
        standard = standard
    )









# Route to Student Details in Admin
@app.route('/student_details_in_admin/<student_ID>')
def student_details_in_admin(student_ID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student WHERE student_ID = %s", (student_ID,))
    student = cur.fetchone()
    cur.close()
    return render_template("student_details_in_admin.html", student = student)











# Route to get standards for selected academic year
@app.route('/get_standards/<academic_year>', methods=['GET', 'POST'])
def get_standards(academic_year):
    print(f"Fetching standards for academic year: {academic_year}")  # Debug log
    cur = mysql.connection.cursor()
    try:
        # Get standards from both current and history tables
        cur.execute("SELECT DISTINCT standard FROM test_results WHERE academic_year = %s", (academic_year,))
        standards_current = [row[0] for row in cur.fetchall()]
        print(f"Current standards: {standards_current}")  # Debug log

        cur.execute("SELECT DISTINCT standard FROM test_results_history WHERE academic_year = %s", (academic_year,))
        standards_history = [row[0] for row in cur.fetchall()]
        print(f"History standards: {standards_history}")  # Debug log

        # Combine and sort standards
        standards = sorted(list(set(standards_current + standards_history)))
        print(f"Combined standards: {standards}")  # Debug log
        
        # If no standards found, check if the academic year exists in the database
        if not standards:
            print(f"No standards found for academic year: {academic_year}")
            # Check if academic year exists in test_results
            cur.execute("SELECT COUNT(*) FROM test_results WHERE academic_year = %s", (academic_year,))
            count_current = cur.fetchone()[0]
            # Check if academic year exists in test_results_history
            cur.execute("SELECT COUNT(*) FROM test_results_history WHERE academic_year = %s", (academic_year,))
            count_history = cur.fetchone()[0]
            print(f"Count in test_results: {count_current}, Count in test_results_history: {count_history}")
        
        response = jsonify(standards)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print(f"Error in get_standards: {str(e)}")  # Debug log
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()











# Route to get roll numbers for selected academic year and standard
@app.route('/get_roll_numbers/<academic_year>/<standard>', methods=['GET'])
def get_roll_numbers(academic_year, standard):
    print(f"Fetching roll numbers for academic year: {academic_year} and standard: {standard}")  # Debug log
    cur = mysql.connection.cursor()
    try:
        # Get roll numbers from both current and history tables
        cur.execute("""
            SELECT roll_number FROM test_results WHERE academic_year = %s AND standard = %s 
        """, (academic_year, standard,))
        roll_numbers_current = [row[0] for row in cur.fetchall()]
        cur.execute("""
            SELECT roll_number FROM test_results_history WHERE academic_year = %s AND standard = %s 
        """, (academic_year, standard,))
        roll_numbers_history = [row[0] for row in cur.fetchall()]
        roll_numbers = sorted(list(set(roll_numbers_current + roll_numbers_history)))
        print(f"Found roll numbers: {roll_numbers}")  # Debug log
        
        # Add CORS headers
        response = jsonify(roll_numbers)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print(f"Error in get_roll_numbers: {str(e)}")  # Debug log
        return jsonify([])
    finally:
        cur.close()










# Route to Students Results in Admin 
@app.route('/students_results_in_admin', methods=["GET", "POST"])
def students_results_in_admin():
    # Check if admin is logged in
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
        
    try:
        cur = mysql.connection.cursor()

        # Fetch standards
        cur.execute("SELECT DISTINCT standard FROM test_results")
        standards_current = set([row[0] for row in cur.fetchall()])
        cur.execute("SELECT DISTINCT standard FROM test_results_history")
        standards_history = set([row[0] for row in cur.fetchall()])
        standards = sorted(list(standards_current.union(standards_history)))
        print(f"Available standards: {standards}")

        # Fetch roll numbers
        cur.execute("SELECT DISTINCT roll_number FROM student")
        roll_numbers = [row[0] for row in cur.fetchall()]
        print(f"Available roll numbers: {roll_numbers}")

        # Fetch academic years
        cur.execute("SELECT DISTINCT academic_year FROM test_results")
        academic_years_current = set([row[0] for row in cur.fetchall()])
        cur.execute("SELECT DISTINCT academic_year FROM test_results_history")
        academic_years_history = set([row[0] for row in cur.fetchall()])
        all_academic_years = sorted(list(academic_years_current.union(academic_years_history)))
        print(f"Available academic years: {all_academic_years}")

        # Initialize variables
        academic_year = None
        test_results = []
        test_results_history = []
        subject_results = {}
        subject_results_history = {}

        if request.method == "POST":
            academic_year = request.form.get("academic_year")
            standard = request.form.get("standard").strip()
            roll_number = request.form.get("roll_number").strip()
            print(f"Received POST request with: academic_year={academic_year}, standard={standard}, roll_number={roll_number}")

            # Get student ID from roll number
            cur.execute("""SELECT student_ID FROM test_results WHERE roll_number = %s AND standard = %s AND academic_year = %s
                        UNION
                        SELECT student_ID FROM test_results_history WHERE roll_number = %s AND standard = %s AND academic_year = %s
                    """, 
                        (roll_number, standard, academic_year, roll_number, standard, academic_year))
            student_ids = [row[0] for row in cur.fetchall()]

            for student_ID in student_ids:
                print(f"Found student_ID: {student_ID}")

                # Fetch current test results
                cur.execute("""
                    SELECT * FROM test_results
                    WHERE student_id = %s AND academic_year = %s AND standard = %s
                """, (student_ID, academic_year, standard))
                test_results = cur.fetchall()
                print(f"Found {len(test_results)} current test results")
                print(f"Current test results: {test_results}")

                # Fetch subject results for current tests
                for test in test_results:
                    test_id = test[0]
                    cur.execute("SELECT * FROM subject_results WHERE test_id = %s", (test_id,))
                    subject_results[test_id] = cur.fetchall()
                    print(f"Found {len(subject_results[test_id])} subject results for test {test_id}")
                    print(f"Subject results for test {test_id}: {subject_results[test_id]}")

                # Fetch historical test results
                cur.execute("""
                    SELECT * FROM test_results_history
                    WHERE student_id = %s AND academic_year = %s AND standard = %s
                """, (student_ID, academic_year, standard))
                test_results_history = cur.fetchall()
                print(f"Found {len(test_results_history)} historical test results")
                print(f"Historical test results: {test_results_history}")

                # Fetch subject results for historical tests
                for history_test in test_results_history:
                    history_test_id = history_test[0]
                    cur.execute("SELECT * FROM subject_results_history WHERE test_id = %s", (history_test_id,))
                    subject_results_history[history_test_id] = cur.fetchall()
                    print(f"Found {len(subject_results_history[history_test_id])} subject results for historical test {history_test_id}")
                    print(f"Subject results for historical test {history_test_id}: {subject_results_history[history_test_id]}")

        cur.close()

        return render_template(
            "students_results_in_admin.html",
            academic_years=all_academic_years,
            selected_year=academic_year,
            test_results=test_results,
            test_results_history=test_results_history,
            subject_results=subject_results,
            subject_results_history=subject_results_history,
            standards=standards,
            roll_numbers=roll_numbers
        )

    except Exception as e:
        print(f"Error in students_results_in_admin: {str(e)}")
        flash(f'An error occurred: {str(e)}', 'error')
        return render_template('students_results_in_admin.html', academic_years=[])









# Route to Upload Time Tables
@app.route('/upload_time_tables')
def upload_time_tables():
    cur = mysql.connection.cursor()
    print(mysql.connection)
    # Always fetch staff list
    cur.execute("SELECT staff_ID FROM staff")
    staff = cur.fetchall()
    cur.execute("SELECT * FROM students_time_table")
    students_timetables = cur.fetchall()
    cur.execute("SELECT * FROM staff_time_table")
    staff_timetables = cur.fetchall()
    cur.close()
    return render_template("upload_time_tables.html", staff = staff, students_timetables = students_timetables, staff_timetables = staff_timetables)    
    
    








# Route to Upload Students Time Table
@app.route('/upload_students_timetable', methods=['GET', 'POST'])
def upload_students_timetable():
    cur = mysql.connection.cursor()
    cur.execute("SELECT standard, timetable_type FROM students_time_table")
    time_tables = cur.fetchall()
    cur.close()
    if request.method == "POST":
        standard = request.form.get("standard").strip()
        timetable_type = request.form.get("timetable_type").strip()
        time_table = request.files.get("time_table")
        file_name = time_table.filename
        mime_type = time_table.mimetype
        file_data = time_table.read()
        try:
            cur = mysql.connection.cursor()
            for timetable in time_tables:
                if timetable[0] == standard and timetable[1] == timetable_type:
                    cur.execute("UPDATE students_time_table SET file_name = %s, mime_type = %s, file_data = %s WHERE standard = %s AND timetable_type = %s", (file_name, mime_type, file_data, standard, timetable_type))
                    mysql.connection.commit()
                    print("Students Time Table Updated Successfully")
                    return redirect(url_for("upload_time_tables"))
        except Exception as e:
            print("Error in Updating Students Time Table: ", str(e))
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                        INSERT INTO students_time_table (standard, timetable_type, file_name, mime_type, file_data)
                        VALUES (%s, %s, %s, %s, %s)
                        """, (standard, timetable_type, file_name, mime_type, file_data))
            mysql.connection.commit()
            print("Students Time Table Uploaded Succesfully")
            return redirect(url_for("upload_time_tables"))
        except Exception as e:
            print("Error in Uploading Students Time Table: ", str(e))
    return render_template("upload_time_tables.html")











# Route to View Students Time Table
@app.route('/view_students_timetable/<timetable_ID>')
def view_students_timetable(timetable_ID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT file_name, mime_type, file_data FROM students_time_table WHERE id = %s", (timetable_ID,))
    result = cur.fetchone()
    if result:
        file_name, mime_type, file_data = result
        return send_file(
            io.BytesIO(file_data),
            mimetype=mime_type,
            as_attachment=False
        )
    else:
        return Response("File not found", status=404)
    
    









# Route to Delete Students Time Table
@app.route('/delete_students_timetable/<timetable_ID>')
def delete_students_timetable(timetable_ID):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM students_time_table WHERE id = %s", (timetable_ID,))
        mysql.connection.commit()
        cur.close()
        print("Students Time Table Deleted Successfully")
        return redirect(url_for("upload_time_tables"))
    except Exception as e:
        print("Error in Deleting Students Time Table: ", str(e))
    return redirect(url_for("upload_time_tables"))











# Route to Upload Students Time Table
@app.route('/upload_staff_timetable', methods=['GET', 'POST'])
def upload_staff_timetable():    
    cur = mysql.connection.cursor()
    cur.execute("SELECT staff_ID FROM staff_time_table")
    staff_timetables = cur.fetchall()
    cur.close()
    if request.method == "POST":
        staff_ID = request.form.get("staff_ID").strip()
        time_table = request.files.get("time_table")
        file_name = time_table.filename
        mime_type = time_table.mimetype
        file_data = time_table.read()
        try:
            cur = mysql.connection.cursor()
            for timetable in staff_timetables:
                if timetable[0] == staff_ID:
                    cur.execute("UPDATE staff_timr_table SET file_name = %s, mime_type = %s, file_data = %s WHERE staff_ID = %s", (file_name, mime_type, file_data, staff_ID))
                    mysql.connection.commit()
                    print("Staff Time Table Updated Successfully")
                    return redirect(url_for("upload_time_tables"))
        except Exception as e:
            print("Error in Updating Staff Time Table: ", str(e))
        try:
            cur.execute("""
                INSERT INTO staff_time_table (staff_ID, file_name, mime_type, file_data)
                VALUES (%s, %s, %s, %s)
            """, (staff_ID, file_name, mime_type, file_data))
            mysql.connection.commit()
            print("Staff Time Table Uploaded Successfully")
            return redirect(url_for("upload_time_tables"))
        except Exception as e:
            print("Error in Uploading Staff Time Table: ", str(e))

    return render_template("upload_time_tables.html")









# Route to View Staff Time Table
@app.route('/view_staff_timetable/<ID>')
def view_staff_timetable(ID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT file_name, mime_type, file_data FROM staff_time_table WHERE id = %s", (ID,))
    result = cur.fetchone()
    if result:
        file_name, mime_type, file_data = result
        return send_file(
            io.BytesIO(file_data),
            mimetype=mime_type,
            as_attachment=False
        )
    else:
        return Response("File not found", status=404)
    
    









# Route to Delete Staff Time Table
@app.route('/delete_staff_timetable/<ID>')
def delete_staff_timetable(ID):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM staff_time_table WHERE id = %s", (ID,))
        mysql.connection.commit()
        cur.close()
        print("Staff Time Table Deleted Successfully")
        return redirect(url_for("upload_time_tables"))
    except Exception as e:
        print("Error in Deleting Staff Time Table: ", str(e))
    return redirect(url_for("upload_time_tables"))









# Route to Transferred Students
@app.route('/transferred_students')
def transferred_students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM transferred_students ORDER BY transferred_date DESC")
    transferred_students = cur.fetchall()
    cur.close()
    return render_template("transferred_students.html", transferred_students = transferred_students)









# Route to Students Details
@app.route('/students_alumni', methods=["GET", "POST"])
def students_alumni():
    cur = mysql.connection.cursor()

    # Get list of standards
    cur.execute("SELECT DISTINCT passed_out_year FROM student_alumni")
    passed_out_years = cur.fetchall()

    students = []  # Initialize students as an empty list
    passed_out_year = None

    if request.method == "POST":
        # Get the selected standard from the form
        passed_out_year = request.form.get("passed_out_year").strip()
        
        # Fetch students based on the selected standard
        if passed_out_year:
            cur.execute("SELECT * FROM student_alumni WHERE passed_out_year = %s ORDER BY roll_number ASC", (passed_out_year,))
            students = cur.fetchall()  # Assign the result of cur.fetchall() to the students list
            print(f"Fetched students: {students}")
    cur.close()

    return render_template(
        "students_alumni.html",
        passed_out_years=passed_out_years,
        students=students,
        passed_out_year=passed_out_year
    )









# Route to Student Alumni in Admin
@app.route('/student_alumni/<student_ID>')
def student_alumni(student_ID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student_alumni WHERE student_ID = %s", (student_ID,))
    student = cur.fetchone()
    print(student)
    cur.close()
    return render_template("student_alumni.html", student = student)











# Route to Delete Student Alumni
@app.route("/delete_student_alumni/<student_ID>")
def delete_student_alumni(student_ID):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM student_alumni_results WHERE student_ID = %s", (student_ID,))
        mysql.connection.commit()
        print("Student Alumni Results Deleted Successfully")
        cur.execute("DELETE FROM student_alumni WHERE student_ID = %s", (student_ID,))
        mysql.connection.commit()
        cur.close()
        print("Student Alumni Deleted Successfully")
        return redirect(url_for("students_alumni"))
    except Exception as e:
        print("Error in Deleting Student Alumni: ", str(e))
    return redirect(url_for("students_alumni"))









# Route to Alumni Results
@app.route("/upload_alumni_results/<student_ID>", methods=["GET", "POST"])
def upload_alumni_results(student_ID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT student_ID, student_name, passed_out_year FROM student_alumni WHERE student_ID = %s", (student_ID,))
    student = cur.fetchone()
    cur.execute("SELECT student_ID FROM student_alumni_results WHERE student_ID = %s",(student_ID,))
    exist = cur.fetchone()     
    if request.method == "POST":
        ssc_hall_ticket = request.form.get("ssc_hall_ticket", "").strip()
        try:
            percentage = request.form.get("percentage")
            cgpa = request.form.get("cgpa")

            if not ssc_hall_ticket:
                flash("SSC Hall Ticket is required.", "error")
                return render_template("upload_alumni_results.html", student=student)
            
            if exist:
                cur.execute("""UPDATE student_alumni_results 
                            SET ssc_hall_ticket = %s, percentage = %s, cgpa = %s WHERE student_ID = %s
                            """, (ssc_hall_ticket, percentage, cgpa, exist[0]))
                mysql.connection.commit()
                return redirect(url_for('alumni_results'))
                    

            cur.execute("""
                INSERT INTO student_alumni_results 
                (student_ID, student_name, ssc_hall_ticket, passed_out_year, percentage, cgpa) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """, 
                (student_ID, student[1], ssc_hall_ticket, student[2], percentage, cgpa)
            )
            mysql.connection.commit()
            cur.close()
            flash("Alumni Results Uploaded Successfully", "success")
            return redirect(url_for("alumni_results"))

        except ValueError:
            flash("Percentage and CGPA must be valid numbers.", "error")
        except Exception as e:
            print("Error in Uploading Alumni Results: ", str(e))
            flash("An error occurred while uploading results.", "error")

    return render_template("upload_alumni_results.html", student=student)










# Route to Alumni Results
@app.route("/alumni_results")
def alumni_results():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student_alumni_results ORDER BY passed_out_year DESC")
    results = cur.fetchall()
    cur.close()
    return render_template("alumni_results.html", results = results)


#####   END OF ADMIN FUNCTIONALITIES  #####









#####   STAFF FUNCTIONALITIES  #####
# Route to Staff Login
@app.route('/staff_login', methods=['GET', 'POST'])
def staff_login():
    if request.method == 'POST':
        try:
            username = request.form.get("username")
            password = request.form.get("password")
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM staff WHERE username = %s", (username,))
            staff = cur.fetchone()
            cur.close()

            if staff:
                print("Staff Found")
                if staff[8] == password:  # Password field
                    session['staff_ID'] = staff[2]  # Store staff ID in session
                    print(str(staff[2]) + " Login Successful")  # Convert staff[2] to string

                    try:
                        msg = Message(
                            "Security Alert - Login Check",
                            sender="kiranadigopula2708@gmail.com",
                            recipients=[staff[5]]  # staff_email
                        )
                        msg.body = f"""Dear {staff[3]},
                        
We Noticed a Login to your account.

Login Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

If this wasn't you, please reset your password immediately.

Thank you,
MySchool World...
"""
                        mail.send(msg)
                        print("Staff Login Alert Sent.")
                        flash(f'Login Alert Sent to {staff[5]}', 'success')
                    except Exception as e:
                        print("Error in sending Staff Login Alert.")
                        flash('Error sending login alert email.', 'error')

                    # Redirect to staff_dashboard.html after successful login
                    return redirect(url_for('staff_dashboard'))  # Use redirect here to move to the dashboard

                else:
                    print("Invalid Staff Password")
                    flash("Invalid Password")
                    return render_template("staff_login.html")
            else:
                print("Invalid Staff Credentials")
                flash("Invalid Credentials", "error")
                return render_template("staff_login.html")
        except Exception as e:
            print("Error Occurred in Staff Login:", e)
            flash("Error Occurred in Login", "error")
            return render_template("staff_login.html")

    return render_template("staff_login.html")










# Route to Staff Dashboard
@app.route('/staff_dashboard')
def staff_dashboard():
    staff_ID = session.get('staff_ID')
    if not staff_ID:
        return redirect(url_for('staff_login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM staff WHERE staff_ID = %s", (staff_ID,))
    staff = cur.fetchone()

    if not staff:
        return render_template("staff_login.html")

    standard = staff['standard'] if isinstance(staff, dict) else staff[4]
    functionalities = standard != "No Standard is Assigned"

    return render_template("staff_dashboard.html", staff=staff, functionalities = functionalities)











# Route to Student Registration
@app.route('/student_registration', methods=['GET', 'POST'])
def student_registration():
    # Retrieve staff details from session
    staff_ID = session.get('staff_ID')

    if not staff_ID:
        return redirect(url_for('staff_login'))

    # Get school_ID and standard from staff table
    cur = mysql.connection.cursor()
    cur.execute("SELECT school_ID, standard FROM staff WHERE staff_ID = %s", (staff_ID,))
    staff = cur.fetchone()
    cur.close()

    if staff is None:
        return redirect(url_for('staff_login'))

    school_ID, standard = staff
    today = datetime.today()
    year = today.year
    if today.month < 6:
        academic_year = f"{year - 1}-{year}"
    else:
        academic_year = f"{year}-{year + 1}"
    cur = mysql.connection.cursor()
    standard = standard.strip()
    student_ID = ""
    student_username=""
    while True:
        index = ''.join(random.choices('0123456789', k=7))
        student_ID = f"{academic_year}{standard}{index}".replace(" ", "")
        cur.execute("SELECT student_ID FROM student WHERE student_ID = %s", (student_ID,))
        exist1 = cur.fetchone()
        cur.execute("SELECT student_ID FROM student_alumni WHERE student_ID = %s", (student_ID,))
        exist2 = cur.fetchone()
        cur.execute("SELECT student_ID FROM transferred_students WHERE student_ID = %s", (student_ID,))
        exist3 = cur.fetchone()
        if exist1 or exist2 or exist3:
            continue
        break
    if request.method == "POST":
        # List of all form fields
        field_names = [
            "roll_number", "student_name", "gender", "date_of_birth",
            "student_aadhar", "student_email", "student_mobile", "resident_type",
            "father_name", "father_aadhar", "father_mobile",
            "mother_name", "mother_aadhar", "mother_mobile",
            "guardian_name", "guardian_aadhar", "guardian_mobile",
            "contact_email", "address", "blood_group", "date_of_joining",
            "parent_or_guardian", "relation"
        ]

        # Dictionary to hold sanitized values
        data = {}
        for field in field_names:
            value = request.form.get(field, "").strip()
            data[field] = value if value else "-NA-"
            
        cur = mysql.connection.cursor()
        cur.execute("SELECT roll_number FROM student WHERE standard = %s", (standard,))
        roll_numbers = cur.fetchall()
        for roll_number in roll_numbers:
            if str(data["roll_number"]) == str(roll_number[0]):
                print("Roll Number must be Unique While Inserting")
                return redirect(url_for("student_registration"))

        # Conditional cleaning based on parent_or_guardian field
        if data["parent_or_guardian"].lower() == "parent":
            data["guardian_name"] = data["guardian_aadhar"] = data["guardian_mobile"] = "-NA-"
        elif data["parent_or_guardian"].lower() == "guardian":
            data["father_name"] = data["father_aadhar"] = data["father_mobile"] = "-NA-"
            data["mother_name"] = data["mother_aadhar"] = data["mother_mobile"] = "-NA-"

        # Generate student username and password
        cur = mysql.connection.cursor()
        cur.execute("SELECT school_name FROM administration WHERE school_ID = %s", (school_ID,))
        school_name = cur.fetchone()[0][:3].lower().strip()
        cur.execute("SELECT student_aadhar FROM student")
        student_aadhar = [row[0] for row in cur.fetchall()]
        for aadhar in student_aadhar:
            if str(data["student_aadhar"]) == str(aadhar) and str(aadhar) != "-NA-":
                print("Student Aadhar must be Unique While Inserting")
                return redirect(url_for("student_registration"))
        cur.close()

        # Remove any spaces from roll number and ensure proper formatting
        roll_number = str(data['roll_number']).strip()
        while True:
            index = ''.join(random.choices('0123456789', k=8))
            student_username = index.replace(" ", "")
            cur = mysql.connection.cursor()
            cur.execute("SELECT student_username FROM student WHERE student_username = %s", (student_username,))
            exist_user1 = cur.fetchone()
            cur.execute("SELECT student_username FROM student_alumni WHERE student_username = %s", (student_username,))
            exist_user2 = cur.fetchone()
            if exist_user1 or exist_user2:
                continue
            break            
        student_password = student_username  # Default password (optional: hash it)

        # Alternate password from DOB digits reversed
        username = student_username
        password = datetime.strptime(data["date_of_birth"], "%Y-%m-%d").strftime("%d%m%Y")

        # Insert data into the student table
        try:
            cur = mysql.connection.cursor()
            if data['student_aadhar']!="-NA-" and (data['student_aadhar'] == data['father_aadhar'] or data['student_aadhar'] == data['mother_aadhar'] or data['student_aadhar'] == data['guardian_aadhar']):
                print("Student Aadhar Clashes with Another aadhars")
                return redirect(url_for("student_registration"))
            if data['father_aadhar']!="-NA-" and (data['father_aadhar'] == data['mother_aadhar'] or data['father_aadhar'] == data['guardian_aadhar'] or data['father_aadhar'] == data['student_aadhar']):
                print("Father Aadhar Clashes with Another aadhars")
                return redirect(url_for("student_registration"))
            if data['mother_aadhar']!="-NA-" and (data['mother_aadhar'] == data['guardian_aadhar'] or data['mother_aadhar'] == data['student_aadhar'] or data['mother_aadhar'] == data['father_aadhar']):
                print("Mother Aadhar Clashes with Another aadhars")
                return redirect(url_for("student_registration"))
            if data['guardian_aadhar']!="-NA-" and (data['guardian_aadhar'] == data['student_aadhar'] or data['guardian_aadhar'] == data['father_aadhar'] or data['guardian_aadhar'] == data['mother_aadhar']):
                print("Guardian Aadhar Clashes with Another aadhars")
                return redirect(url_for("student_registration"))
             
            cur.execute("""
                INSERT INTO student (
                    school_ID, staff_ID, student_ID, roll_number, student_name, standard, date_of_birth, gender,
                    student_aadhar, student_email, student_mobile, resident_type, father_name, father_aadhar,
                    father_mobile, mother_name, mother_aadhar, mother_mobile, guardian_name, guardian_aadhar,
                    guardian_mobile, relation, contact_email, address, blood_group, date_of_joining, student_username,
                    student_password, username, password
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                school_ID, staff_ID, student_ID, data["roll_number"], data["student_name"], standard, data["date_of_birth"],
                data["gender"], data["student_aadhar"], data["student_email"],
                data["student_mobile"], data["resident_type"], data["father_name"], data["father_aadhar"],
                data["father_mobile"], data["mother_name"], data["mother_aadhar"], data["mother_mobile"],
                data["guardian_name"], data["guardian_aadhar"], data["guardian_mobile"], data["relation"],
                data["contact_email"], data["address"], data["blood_group"], data["date_of_joining"],
                student_username, student_password, username, password
            ))
            mysql.connection.commit()
            cur.close()
            print("Student Registered Successfully")
            flash("Student Registered Successfully", "success")
            return redirect(url_for("students_details_in_staff"))

        except Exception as e:
            print("Error in Registering Student:", str(e))
            flash("Error in Registering Student", "error")
            return redirect(url_for("student_registration"))

    return render_template("student_registration.html", school_ID = school_ID, staff_ID = staff_ID, standard = standard)











# Route to Student Details in Staff
@app.route('/students_details_in_staff')
def students_details_in_staff():
    staff_ID = session.get('staff_ID')
    if not staff_ID:
        return redirect(url_for('staff_login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT standard FROM staff WHERE staff_ID = %s", (staff_ID,))
    standard = cur.fetchone()[0]
    if not standard:
        print("Invalid Staff")
    cur.execute("SELECT * FROM student WHERE staff_ID = %s AND standard = %s ORDER BY roll_number ASC", (staff_ID, standard,))
    students = cur.fetchall()
    cur.close()
    return render_template("students_details_in_staff.html", students = students)











# Route to Student Details
@app.route('/student_details_in_staff/<student_ID>')
def student_details_in_staff(student_ID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student WHERE student_ID = %s", (student_ID,))
    student = cur.fetchone()
    cur.close()
    return render_template("student_details_in_staff.html", student = student, student_ID = student_ID)











# Route to Update Student Details
@app.route('/update_student_details/<student_ID>', methods=['GET', 'POST'])
def update_student_details(student_ID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student WHERE student_ID = %s", (student_ID,))
    student = cur.fetchone()
    cur.close()

    if not student:
        print("Invalid Student")

    if request.method == "POST":
        # Logging the incoming form data for debugging
        print("POST Request Received")
        print(request.form)  # Log all submitted form data for debugging

        update_roll_number = request.form.get("update_roll_number").strip() or "-NA-"
        update_student_name = request.form.get("update_student_name").strip() or "-NA-"
        update_date_of_birth = request.form.get("update_date_of_birth").strip() or "-NA-"
        update_blood_group = request.form.get("update_blood_group").strip() or "-NA-"
        update_gender = request.form.get("update_gender").strip() or "-NA-"
        update_student_aadhar = request.form.get("update_student_aadhar").strip() or "-NA-"
        update_student_email = request.form.get("update_student_email").strip() or "-NA-"
        update_student_mobile = request.form.get("update_student_mobile").strip() or "-NA-"
        update_resident_type = request.form.get("update_resident_type").strip() or "-NA-"
        update_contact_email = request.form.get("update_contact_email").strip() or "-NA-"
        update_father_name = request.form.get("update_father_name").strip() or "-NA-"
        update_father_aadhar = request.form.get("update_father_aadhar").strip() or "-NA-"
        update_father_mobile = request.form.get("update_father_mobile").strip() or "-NA-"
        update_mother_name = request.form.get("update_mother_name").strip() or "-NA-"
        update_mother_aadhar = request.form.get("update_mother_aadhar").strip() or "-NA-"
        update_mother_mobile = request.form.get("update_mother_mobile").strip() or "-NA-"
        update_guardian_name = request.form.get("update_guardian_name").strip() or "-NA-"
        update_guardian_aadhar = request.form.get("update_guardian_aadhar").strip() or "-NA-"
        update_guardian_mobile = request.form.get("update_guardian_mobile").strip() or "-NA-"
        update_relation = request.form.get("update_relation").strip() or "-NA-"
        update_address = request.form.get("update_address").strip() or "-NA-"
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE student SET roll_number = %s, student_name = %s, date_of_birth = %s, gender = %s,
                student_aadhar = %s, student_email = %s, student_mobile = %s, resident_type = %s, contact_email = %s,
                father_name = %s, father_aadhar = %s, father_mobile = %s, mother_name = %s, mother_aadhar = %s,
                mother_mobile = %s, guardian_name = %s, guardian_aadhar = %s, guardian_mobile = %s, relation = %s,
                address = %s, blood_group = %s
                WHERE student_ID = %s
            """, (
                update_roll_number, update_student_name, update_date_of_birth, update_gender,
                update_student_aadhar, update_student_email, update_student_mobile, update_resident_type,
                update_contact_email, update_father_name, update_father_aadhar, update_father_mobile,
                update_mother_name, update_mother_aadhar, update_mother_mobile, update_guardian_name,
                update_guardian_aadhar, update_guardian_mobile, update_relation, update_address,
                update_blood_group, student_ID
            ))
            mysql.connection.commit()
            cur.close()
            print("Student Details Updated Successfully")
            return redirect(url_for('student_details_in_staff', student_ID = student_ID))
        except Exception as e:
            print("Error in Updating Student Details:", str(e))
            mysql.connection.rollback()  # Rollback the transaction on error
    return render_template("student_details_in_staff.html", student = student)
 
 
 
 
 
 
 
 
 
 
# Route to Students Results in Staff
@app.route('/students_results_in_staff', methods=['GET', 'POST'])
def students_results_in_staff():
    staff_ID = session.get('staff_ID')
    if not staff_ID:
        return redirect(url_for('staff_login'))

    cur = mysql.connection.cursor()
    # Get all students under the current staff (for dropdown)
    cur.execute("SELECT student_ID, roll_number FROM student WHERE staff_ID = %s ORDER BY roll_number ASC", (staff_ID,))
    students = cur.fetchall()

    test_results = []
    subject_results = []
    results = []  # To hold the result of the selected student only

    if request.method == 'POST':
        selected_roll = request.form.get('rollNumber').strip()
        # Get student ID from selected roll number
        cur.execute("SELECT student_ID FROM student WHERE roll_number = %s AND staff_ID = %s", (selected_roll, staff_ID))
        student_row = cur.fetchone()

        if student_row:
            student_id = student_row[0]

            # Get all test results for that student
            cur.execute("""
                SELECT test_id, academic_year, standard, test_name, exam_start_date, exam_end_date,
                       total_marks, percentage_cgpa, status, created_at
                FROM test_results
                WHERE student_id = %s 
                ORDER BY test_id DESC
            """, (student_id,))
            test_results = cur.fetchall()

            # Loop over tests and fetch subjects
            for test in test_results:
                test_id = test[0]
                cur.execute("""
                    SELECT date, subject_name, obtained_marks, total_marks, grade, subject_status
                    FROM subject_results
                    WHERE test_id = %s
                """, (test_id,))
                subjects = cur.fetchall()
                results.append((test, subjects))  # A list of (test, [subject rows])
        else:
            flash("Student not found or unauthorized access.", "error")

    cur.close()
    return render_template(
        'students_results_in_staff.html',
        students=students,
        results=results,
        test_results=test_results,
        subject_results=subject_results,
        selected_roll=selected_roll if request.method == 'POST' else None
    )




    
    
    





# Route to Promote Students
@app.route('/promote_students', methods=['GET', 'POST'])
def promote_students():
    staff_ID = session.get('staff_ID')
    if not staff_ID:
        return redirect(url_for('staff_login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT standard FROM staff WHERE staff_ID = %s", (staff_ID,))
    standard = cur.fetchone()[0]
    if not standard:
        print("Invalid Staff")
    cur.execute("SELECT student_ID, roll_number, student_name, standard, staff_ID FROM student WHERE staff_ID = %s and standard = %s", (staff_ID, standard,))
    students = cur.fetchall()
    try:
        if request.method == 'POST':
            for student in students:
                student_ID = student[0]
                update_standard = request.form.get(f'update_standard_{student_ID}').strip()
                cur.execute("SELECT staff_ID FROM staff WHERE standard = %s", (update_standard,))
                staff = cur.fetchone()
                staff_ID = staff[0] if staff else "No Staff is Assigned"
                if not staff:
                    print("Staff is not Assigned for this Standard")
                cur.execute("UPDATE student SET standard = %s, staff_ID = %s WHERE student_ID = %s", (update_standard, staff_ID, student_ID,))
                if update_standard:
                    if update_standard == 'Passed Out':
                        cur.execute("""
                            SELECT serial_number, school_ID, staff_ID, student_ID, roll_number,
                                   student_name, standard, date_of_birth, gender, student_aadhar,
                                   student_email, student_mobile, resident_type, father_name,
                                   father_aadhar, father_mobile, mother_name, mother_aadhar,
                                   mother_mobile, guardian_name, guardian_aadhar, guardian_mobile,
                                   relation, contact_email, address, blood_group, date_of_joining,
                                   student_username, student_password, username, password
                            FROM student WHERE student_ID = %s
                        """, (student_ID,))
                        student_data = cur.fetchone()

                        if student_data:
                            passed_out_year = datetime.now().year
                            cur.execute("""
                                INSERT INTO student_alumni (
                                    serial_number, school_ID, staff_ID, student_ID, roll_number,
                                    student_name, standard, date_of_birth, gender, student_aadhar,
                                    student_email, student_mobile, resident_type, father_name,
                                    father_aadhar, father_mobile, mother_name, mother_aadhar,
                                    mother_mobile, guardian_name, guardian_aadhar, guardian_mobile,
                                    relation, contact_email, address, blood_group, date_of_joining,
                                    student_username, student_password, username, password,
                                    passed_out_year
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """, student_data + (passed_out_year,))
                            cur.execute("SELECT test_id FROM test_results WHERE student_ID = %s",(student_ID,))
                            test_results = cur.fetchall()
                            for test_id in test_results:
                                cur.execute("DELETE FROM subject_results WHERE test_id = %s", (test_id[0],))
                            cur.execute("DELETE FROM test_results WHERE student_ID = %s", (student_ID,))
                            cur.execute("SELECT test_id FROM test_results_history WHERE student_ID = %s",(student_ID,))
                            test_results_history = cur.fetchall()
                            for test_id in test_results_history:
                                cur.execute("DELETE FROM subject_results_history WHERE test_id = %s", (test_id[0],))
                            cur.execute("DELETE FROM test_results_history WHERE student_ID = %s", (student_ID,))                          
                            cur.execute("DELETE FROM student WHERE student_ID = %s", (student_ID,))
            mysql.connection.commit()
            cur.close()
            print("Student standards updated successfully")
            flash("Student standards updated successfully!", "success")
            return redirect(url_for('students_details_in_staff'))
    except Exception as e:
        print("Error in updating student standards:", str(e))
    cur.close()   
    return render_template('promote_students.html', students=students)












# Route to Transfer Student
@app.route('/transfer_student/<student_ID>', methods=['GET', 'POST'])
def transfer_student(student_ID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT student_ID, roll_number, student_name, standard, date_of_joining FROM student WHERE student_ID = %s", (student_ID,))
    student = cur.fetchone()
    if not student:
        print("Invalid Student")
        return redirect(url_for('students_details_in_staff'))
    roll_number = student[1]
    student_name = student[2]
    standard = student[3]
    date_of_joining = student[4]
    if request.method == "POST":
        standard_status = request.form.get("standard_status").strip()
        student_contact = request.form.get("student_contact").strip()
        transferred_date = request.form.get("transferred_date")
        print(f"form data: ",standard_status, student_contact, transferred_date)
        try:
            cur.execute("""
                        INSERT INTO transferred_students(student_ID, roll_number, student_name, standard, 
                        standard_status, student_contact, date_of_joining, transferred_date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (student_ID, roll_number, student_name, standard, standard_status, student_contact, 
                              date_of_joining, transferred_date))
            mysql.connection.commit()
            print("Student Transferred Successfully")
            try:
                # Delete from subject_results_history and test_results_history
                cur.execute("SELECT test_id FROM test_results_history WHERE student_ID = %s", (student_ID,))
                test_ids_history = cur.fetchall()
                for tid in test_ids_history:
                    cur.execute("DELETE FROM subject_results_history WHERE test_id = %s", (tid[0],))
                cur.execute("DELETE FROM test_results_history WHERE student_ID = %s", (student_ID,))
                mysql.connection.commit()

                # Delete from subject_results and test_results
                cur.execute("SELECT test_id FROM test_results WHERE student_ID = %s", (student_ID,))
                test_ids = cur.fetchall()
                for tid in test_ids:
                    cur.execute("DELETE FROM subject_results WHERE test_id = %s", (tid[0],))
                cur.execute("DELETE FROM test_results WHERE student_ID = %s", (student_ID,))
                mysql.connection.commit()
                
                cur.execute("DELETE FROM parents_help_desk WHERE parent_ID = %s", (student_ID,))

                # Finally, delete the student
                cur.execute("DELETE FROM student WHERE student_ID = %s", (student_ID,))
                mysql.connection.commit()

                cur.close()
                print("Student Deleted Successfully")
                return redirect(url_for('students_details_in_staff'))

            except Exception as e:
                print("Error in Deleting Student:", str(e))
        except Exception as e:
            print("Error in Transfer Student", str(e))
    return render_template("transfer_student.html", student = student)











# Route to Request Leave
@app.route('/request_leave', methods = ['GET', 'POST'])
def request_leave():
    staff_ID = session.get('staff_ID')
    cur = mysql.connection.cursor()
    cur.execute("SELECT school_ID, staff_name FROM staff WHERE staff_ID = %s", (staff_ID,))
    staff = cur.fetchone()
    if staff is None:
        print("Invalid Staff")
        return redirect(url_for('staff_login'))
    school_ID = staff[0]
    staff_name = staff[1]
    cur.close()
    if not staff_ID:
        return redirect(url_for('staff_login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM staff_leaves WHERE staff_ID = %s ORDER BY ID DESC", (staff_ID,))
    leaves = cur.fetchall()
    cur.execute("SELECT * FROM leave_history WHERE staff_ID = %s ORDER BY ID DESC", (staff_ID,))
    leave_history = cur.fetchall()
    cur.close()
    if request.method == "POST":
        leave_type = request.form.get("leave_type").strip()
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
            if end_date_obj < start_date_obj:
                flash("End date cannot be before start date", "danger")
                return redirect(url_for('request_leave'))
            today = datetime.today().date()
            if start_date_obj < today:
                flash("Start date cannot be less than Today Date", "danger")
                print("Start Date Cannot be less than Today Date")
            else:
                days = (end_date_obj - start_date_obj).days + 1
                applied_on = today
                cur = mysql.connection.cursor()
                cur.execute("""
                            SELECT start_date, end_date FROM staff_leaves 
                            WHERE staff_ID = %s AND (
                                %s BETWEEN start_date AND end_date OR 
                                %s BETWEEN start_date AND end_date OR 
                                start_date = %s OR end_date = %s
                            )
                        """, (staff_ID, start_date_obj, end_date_obj, start_date_obj, end_date_obj))
                existing_leave = cur.fetchone()
                if existing_leave:
                    existing_start_date = existing_leave[0]
                    existing_end_date = existing_leave[1]

                    if start_date_obj > existing_end_date:
                        # New leave starts after existing leave ends – insert it
                        try:
                            cur.execute("""
                                INSERT INTO staff_leaves 
                                (school_ID, staff_ID, staff_name, leave_type, start_date, end_date, days, applied_on)
                                VALUES (%s, %s, %s, %s, %s, %s, %s ,%s)
                            """, (school_ID, staff_ID, staff_name, leave_type, start_date_obj, end_date_obj, days, applied_on))
                            mysql.connection.commit()
                            cur.close()
                            print("New Leave is Inserted")
                            flash("New leave request submitted (non-overlapping).", "success")
                            return redirect(url_for('request_leave'))
                        except Exception as e:
                            print("Leave is not inserted: ", e)
                            return redirect(url_for('request_leave'))
                    else:
                        # Overlapping – update the existing leave
                        try:
                            cur.execute("""
                                UPDATE staff_leaves 
                                SET leave_type = %s, start_date = %s, end_date = %s, days = %s, applied_on = %s 
                                WHERE staff_ID = %s AND start_date = %s AND end_date = %s
                            """, (leave_type, start_date_obj, end_date_obj, days, applied_on,
                                staff_ID, existing_start_date, existing_end_date))
                            mysql.connection.commit()
                            cur.close()
                            flash("Existing leave updated (overlap or exact match found).", "info")
                            print("Existing Leave Updated")
                            return redirect(url_for('request_leave'))
                        except Exception as e:
                            print("Leave Not Updated: ", e)
                            return redirect(url_for('request_leave'))
                else:
                    # No overlap or match – insert new leave
                    try:
                        cur.execute("""
                            INSERT INTO staff_leaves 
                            (school_ID, staff_ID, staff_name, leave_type, start_date, end_date, days, applied_on)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (school_ID, staff_ID, staff_name, leave_type, start_date_obj, end_date_obj, days, applied_on))
                        mysql.connection.commit()
                        cur.close()
                        print("New Leave is Submitted")
                        flash("New leave request submitted.", "success")
                        return redirect(url_for('request_leave'))
                    except Exception as e:
                        print("Leave is not submitted: ", e)
                        return redirect(url_for('request_leave'))
        except Exception as e:
            print("ERROR: ", e)
            return redirect(url_for('request_leave'))
        except ValueError as v:
            print("VALUE ERROR: ", v)
            return redirect(url_for('request_leave'))
    return render_template("request_leave.html", staff_ID = staff_ID, staff_name = staff_name, leaves = leaves, leave_history = leave_history)









# Route to Staff Time Table
@app.route('/staff_timetable')
def staff_timetable():
    staff_ID = session.get('staff_ID')
    print("Logged in Staff ID:", staff_ID)  # Debug

    if not staff_ID:
        return redirect(url_for('staff_login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM staff_time_table WHERE staff_ID = %s", (staff_ID,))
    timetables = cur.fetchall()
    print("Timetables fetched:", timetables)  # Debug
    cur.close()
    return render_template("staff_timetable.html", staff_ID=staff_ID, timetables=timetables)








# Route to Download Staff Time Table
@app.route('/download_staff_timetable/<id>')
def download_staff_timetable(id):
    print("Download requested for ID:", id)  # Debug

    cur = mysql.connection.cursor()
    cur.execute("SELECT file_name, mime_type, file_data FROM staff_time_table WHERE id = %s", (id,))
    file_record = cur.fetchone()
    cur.close()

    if not file_record:
        print("No file found for ID:", id)  # Debug
        return "File not found", 404

    file_name, mime_type, file_data = file_record
    print(f"Sending file: {file_name}, Type: {mime_type}, Size: {len(file_data)} bytes")  # Debug

    return send_file(
        io.BytesIO(file_data),
        mimetype=mime_type,
        download_name=file_name,
        as_attachment=True
    )











# Utility function to determine academic year
def get_academic_year():
    today = datetime.today()
    year = today.year
    if today.month < 6:
        return f"{year - 1}-{year}"
    return f"{year}-{year + 1}"










# Route to Upload Results
@app.route('/upload_results', methods=['GET', 'POST'])
def upload_results():
    # Session check
    if not session.get('staff_ID'):
        return redirect(url_for('staff_login'))

    # DB connection
    cur = mysql.connection.cursor()

    # Fetch standard for staff
    cur.execute("SELECT standard FROM staff WHERE staff_ID = %s", (session.get('staff_ID'),))
    result = cur.fetchone()
    standard = result[0] if result else None

    # Fetch students associated with staff
    cur.execute("SELECT roll_number FROM student WHERE staff_ID = %s ORDER BY roll_number ASC", (session.get('staff_ID'),))
    roll_numbers = cur.fetchall()

    if request.method == 'POST':
        try:
            roll_number = request.form.get('roll_number').strip()
            cur.execute("SELECT student_ID FROM student WHERE roll_number = %s AND standard = %s", (roll_number, standard,))
            student_id = cur.fetchone()
            
            test_name = request.form.get('testName').strip()
            exam_start_date = request.form.get('examStartDate')
            exam_end_date = request.form.get('examEndDate')
            total_marks = request.form.get('total_marks').strip()
            percentage_cgpa = request.form.get('percentage_cgpa').strip()
            academic_year = get_academic_year()

            # Insert test result header
            cur.execute("""
                INSERT INTO test_results (
                    student_id, roll_number, academic_year, standard,
                    test_name, exam_start_date, exam_end_date,
                    total_marks, percentage_cgpa, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                student_id[0], roll_number, academic_year, standard,
                test_name, exam_start_date, exam_end_date,
                total_marks, percentage_cgpa, datetime.now()
            ))
            mysql.connection.commit()
            test_id = cur.lastrowid
            print("Test Results Submitted Successfully")

            # Process subject-wise data
            index = 0
            fail_found = False
            subject_found = False

            while True:
                date = request.form.get(f'date_{index}')
                if not date:
                    break

                subject_name = request.form.get(f'subject_name_{index}').strip()
                if not subject_name:
                    break

                subject_found = True  # At least one subject was submitted

                obtained = request.form.get(f'obtained_{index}', 0).strip() or ""
                total = request.form.get(f'total_{index}', 0).strip()
                grade = request.form.get(f'grade_{index}').strip()

                print(f"date: {date}, subject_name: {subject_name}, obtained: {obtained}, total: {total}, grade: {grade}")
                
                if grade == "F" and obtained:
                    subject_status = 'Fail'
                    fail_found = True
                elif (not obtained or obtained == None or obtained == "") and grade:
                    subject_status = 'Absent'
                    fail_found = True
                elif grade != "F":
                    subject_status = 'Pass'

                # Insert subject result regardless of pass/fail
                cur.execute("""
                    INSERT INTO subject_results (
                        test_id, date, subject_name, obtained_marks, total_marks, grade, subject_status
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    test_id, date, subject_name, obtained, total, grade, subject_status
                ))

                index += 1  # Continue loop regardless of fail_found

            # After all subjects are processed, update the overall test status
            if not subject_found:
                # No subject data submitted, mark test as absent
                cur.execute("UPDATE test_results SET status = %s WHERE test_id = %s", ('Absent', test_id))
            elif fail_found:
                # If any subject failed or absent, mark test as fail
                cur.execute("UPDATE test_results SET status = %s WHERE test_id = %s", ('Fail', test_id))
            else:
                # If all subjects passed, mark test as pass
                cur.execute("UPDATE test_results SET status = %s WHERE test_id = %s", ('Pass', test_id))

            mysql.connection.commit()
            cur.close()
            print("Subject Results Submitted Successfully")
            flash("Test results submitted successfully!", "success")
            return redirect(url_for('students_results_in_staff'))

        except Exception as e:
            print("Error submitting results:", str(e))
            flash("Error submitting results. Please try again.", "danger")

    return render_template("upload_results.html", roll_numbers = roll_numbers)









# Route to Upload Materials
@app.route('/upload_materials', methods=['GET', 'POST'])
def upload_materials():
    staff_ID = session.get('staff_ID')
    if not staff_ID:
        print("Invalid Staff")
        return redirect(url_for('staff_login')) 
    cur = mysql.connection.cursor()
    cur.execute("SELECT standard FROM staff WHERE staff_ID = %s", (staff_ID,))
    result = cur.fetchone()
    standard = result[0] if result else None
    cur.execute("SELECT * FROM materials WHERE staff_ID = %s", (staff_ID,))
    materials = cur.fetchall()
    try:
        if request.method == 'POST':
            file_header = request.form.get("file_header").strip()
            subject = request.form.get("subject").strip()
            material_file = request.files.get("material_file")
            if not file_header or not material_file:
                return "File header and file are required", 400
            file_name = material_file.filename.strip()
            mime_type = material_file.mimetype
            file_data = material_file.read()
            cur.execute("""
                INSERT INTO materials (staff_ID, standard, file_header, subject, file_name, mime_type, file_data)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (staff_ID, standard, file_header, subject, file_name, mime_type, file_data))
            mysql.connection.commit()
            print("Material Uploaded Successfully")
            cur.close()
            return redirect(url_for('upload_materials'))
    except Exception as e:
        print("Error in uploading material:", str(e))
        cur.close()
    return render_template("upload_materials.html", materials = materials)










# Route to View Uploaded Materials
@app.route("/view_material/<int:material_ID>")
def view_material(material_ID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT file_name, mime_type, file_data FROM materials WHERE id = %s", (material_ID,))
    result = cur.fetchone()
    if result:
        file_name, mime_type, file_data = result
        return send_file(
            io.BytesIO(file_data),
            mimetype=mime_type,
            as_attachment=False
        )
    else:
        return Response("File not found", status=404)












# Route to Delete Material
@app.route("/delete_material/<int:material_ID>")
def delete_material(material_ID):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM materials WHERE id = %s", (material_ID,))
        mysql.connection.commit()
        print("Material Deleted Successfully")
        cur.close()
        return redirect("/upload_materials")
    except Exception as e:
        print("Error in deleting material:", str(e))
    return render_template("upload_materials.html")












# Route to Upload Question Papers
@app.route('/upload_question_papers', methods=['GET', 'POST'])
def upload_question_papers():
    staff_ID = session.get('staff_ID')
    if not staff_ID:
        print("Invalid Staff")
        return redirect(url_for('staff_login')) 
    cur = mysql.connection.cursor()
    cur.execute("SELECT standard FROM staff WHERE staff_ID = %s", (staff_ID,))
    result = cur.fetchone()
    standard = result[0] if result else None
    cur.execute("SELECT * FROM question_papers WHERE staff_ID = %s", (staff_ID,))
    question_papers = cur.fetchall()
    try:
        if request.method == 'POST':
            file_header = request.form.get("file_header").strip()
            subject = request.form.get("subject").strip()
            question_paper = request.files.get("question_paper")
            if not file_header or not question_paper:
                return "File header and file are required", 400
            file_name = question_paper.filename.strip()
            mime_type = question_paper.mimetype
            file_data = question_paper.read()
            cur.execute("""
                INSERT INTO question_papers (staff_ID, standard, file_header, subject, file_name, mime_type, file_data)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (staff_ID, standard, file_header, subject, file_name, mime_type, file_data))
            mysql.connection.commit()
            print("Question Paper Uploaded Successfully")
            cur.close()
            return redirect(url_for('upload_question_papers'))
    except Exception as e:
        print("Error in uploading Question Paper:", str(e))
        cur.close()
    return render_template("upload_question_papers.html", question_papers = question_papers)










# Route to View Uploaded Materials
@app.route("/view_question_paper/<int:question_paper_ID>")
def view_question_paper(question_paper_ID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT file_name, mime_type, file_data FROM question_papers WHERE id = %s", (question_paper_ID,))
    result = cur.fetchone()
    if result:
        file_name, mime_type, file_data = result
        return send_file(
            io.BytesIO(file_data),
            mimetype=mime_type,
            as_attachment=False
        )
    else:
        return Response("File not found", status=404)











# Route to Delete Material
@app.route("/delete_question_paper/<int:question_paper_ID>")
def delete_question_paper(question_paper_ID):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM question_papers WHERE id = %s", (question_paper_ID,))
        mysql.connection.commit()
        print("Question Deleted Successfully")
        cur.close()
        return redirect("/upload_question_papers")
    except Exception as e:
        print("Error in deleting Question Paper:", str(e))
    return render_template("upload_question_papers.html")









# Route to Complaints
@app.route('/complaints')
def complaints():
    staff_ID = session.get('staff_ID')
    solve = []
    if not staff_ID:
        return redirect(url_for('staff_login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT standard FROM staff WHERE staff_ID = %s", (staff_ID,))
    standard = cur.fetchone()
    if standard:
        standard = standard[0]
    cur.execute("""
    SELECT 
        phd.id, phd.child_roll_number, phd.child_standard, phd.subject, 
        phd.message, phd.documents, phd.documents_filename, 
        phd.audio, phd.audio_filename, phd.submitted_at, phd.status,
        s.roll_number, s.student_name
    FROM parents_help_desk phd
    JOIN student s ON phd.parent_ID = s.student_ID
    WHERE phd.child_standard = %s ORDER BY phd.submitted_at DESC
""", (standard,))
    complaints = cur.fetchall()
    cur.close()
    return render_template("complaints.html", complaints = complaints)









# Route to Get Audio
@app.route('/get_audio/<int:complaint_id>')
def get_audio(complaint_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT audio, audio_filename FROM parents_help_desk WHERE id = %s", (complaint_id,))
    result = cur.fetchone()
    cur.close()

    if result and result[0]:
        audio_data = result[0]
        filename = result[1] or "audio.wav"
        return send_file(
            io.BytesIO(audio_data),
            mimetype="audio/wav",
            as_attachment=False,
            download_name=filename
        )
    return "Audio not found", 404








# Route to Get Document
@app.route('/get_document/<int:complaint_id>')
def get_document(complaint_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT documents, documents_filename,document_mime_type FROM parents_help_desk WHERE id = %s", (complaint_id,))
    result = cur.fetchone()
    cur.close()

    if result:
        file_data, filename, mime_type = result
        return send_file(
            io.BytesIO(file_data),
            download_name=filename,  # Flask 2.0+ uses 'download_name'
            mimetype=mime_type,
            as_attachment=False
        )
    else:
        return Response("File not found", status=404)









# Route to Resolve Complaint
@app.route('/resolve_complaint/<complaint_id>')
def resolve_complaint(complaint_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE parents_help_desk SET status = 'Solved' WHERE id = %s", (complaint_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('complaints'))

#####   END OF STAFF FUNCTIONALITIES    #####









#####   START OF ARCHIEVING BEFORE STARTING OF THE NEW ACADEMIC YEAR    #####
# Route to Archieve Results
def archive_test_results():
    print("== Archiving Process Started ==")
    with app.app_context():
        try:
            cur = mysql.connection.cursor()

            # Step 1: Archive test_results
            try:
                cur.execute("INSERT INTO test_results_history SELECT * FROM test_results")
                mysql.connection.commit()
                print("✅ test_results archived.")
            except Exception as e:
                print("❌ Error archiving test_results:", repr(e))

            # Step 2: Archive subject_results
            try:
                cur.execute("INSERT INTO subject_results_history SELECT * FROM subject_results")
                mysql.connection.commit()
                print("✅ subject_results archived.")
            except Exception as e:
                print("❌ Error archiving subject_results:", repr(e))

            # Step 3: Disable safe update mode
            try:
                cur.execute("SET SESSION sql_safe_updates = 0")
                mysql.connection.commit()
                print("🔓 Safe updates disabled.")
            except Exception as e:
                print("❌ Error disabling safe updates:", repr(e))

            # Step 4: Delete data from tables
            tables_to_clear = [
                "subject_results",
                "test_results",
                "materials",
                "question_papers",
                "staff_time_table",
                "students_time_table",
                "parents_help_desk",
                "help_desk"
            ]

            for table in tables_to_clear:
                try:
                    cur.execute(f"DELETE FROM {table}")
                    mysql.connection.commit()
                    print(f"🗑️ Deleted {cur.rowcount} rows from {table}")
                except Exception as e:
                    print(f"❌ Error deleting from {table}:", repr(e))

            # Step 5: Re-enable safe update mode
            try:
                cur.execute("SET SESSION sql_safe_updates = 1")
                mysql.connection.commit()
                print("🔒 Safe updates re-enabled.")
            except Exception as e:
                print("❌ Error enabling safe updates:", repr(e))

            cur.close()
            print("✅ Archiving process completed successfully.")

        except Exception as e:
            print("❌ Unexpected error during archiving:", repr(e))

# Initialize the scheduler
scheduler = BackgroundScheduler()

# Add the job to run at May 31
scheduler.add_job(
    func=archive_test_results,
    trigger=CronTrigger(month=5, day=31, hour=0, minute=1),
    id='archive_job',
    name='Archive test results annually',
    replace_existing=True
)

# Start the scheduler
scheduler.start()

#####   END OF ARCHIEVING   #####









#####   PARENT FUNCTIONALITIES  #####
# Route to Parent Login
@app.route('/parent_login', methods=['GET', 'POST'])
def parent_login():
    if request.method == "POST":
        try:
            parent_username = request.form.get("parent_username")
            parent_password = request.form.get("parent_password")
            cur= mysql.connection.cursor()
            cur.execute("SELECT student_ID, username, password FROM student WHERE student_username = %s", (parent_username,))
            parent = cur.fetchone()
            cur.close()
            if parent:
                if parent[2] == parent_password:
                    session['parent_ID'] = parent[0]
                    print("Parent Login Successful")
                    return redirect("/parent_dashboard")
                else:
                    print("Invalid Parent Password")
                    return render_template("parent_login.html")
            else:
                print("Invalid Parent Credentials")
                return render_template("parent_login.html")
        except Exception as e:
            print("Error Occurred in Parent Login:", e)
    return render_template("parent_login.html")











# Route to Student Dashboard
@app.route('/parent_dashboard')
def parent_dashboard():
    parent_ID = session.get('parent_ID')
    if not parent_ID:
        return redirect(url_for('parent_login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT student_name FROM student WHERE student_ID = %s", (parent_ID, ))
    parent = cur.fetchone()
    cur.close()
    return render_template("parent_dashboard.html", parent = parent)










# Route to Student Details in Admin
@app.route('/child_info')
def child_info():
    parent_ID = session.get('parent_ID')
    if not parent_ID:
        return redirect(url_for('parent_login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student WHERE student_ID = %s", (parent_ID,))
    student = cur.fetchone()
    cur.close()
    return render_template("child_info.html", student = student)










# Route to Child Materials According to Standard
@app.route('/child_materials')
def child_materials():
    parent_ID = session.get('parent_ID')
    if not parent_ID:
        return redirect(url_for('parent_login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT standard FROM student WHERE student_ID = %s", (parent_ID, ))
    result = cur.fetchone()
    standard = result[0] if result else None
    cur.execute("SELECT * FROM materials WHERE standard = %s", (standard, ))
    materials = cur.fetchall()
    cur.close()
    return render_template("child_materials.html", materials = materials, standard = standard)










# Route to Download Child Materials
@app.route('/download_child_material/<int:material_id>')
def download_child_material(material_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT file_name, mime_type, file_data FROM materials WHERE id = %s", (material_id,))
    file_record = cur.fetchone()
    cur.close()
    if not file_record:
        return "File not found", 404
    file_name, mime_type, file_data = file_record
    return send_file(
        io.BytesIO(file_data),
        mimetype=mime_type,
        download_name=file_name,
        as_attachment=True
    )








# Route to Child Question Papers According to Standard
@app.route('/child_question_papers')
def child_question_papers():
    parent_ID = session.get('parent_ID')
    if not parent_ID:
        return redirect(url_for('parent_login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT standard FROM student WHERE student_ID = %s", (parent_ID, ))
    result = cur.fetchone()
    standard = result[0] if result else None
    cur.execute("SELECT * FROM question_papers WHERE standard = %s", (standard, ))
    question_papers = cur.fetchall()
    cur.close()
    return render_template("child_question_papers.html", question_papers = question_papers, standard = standard)










# Route to Download Child Question Papers
@app.route('/download_child_question_paper/<int:question_paper_id>')
def download_child_question_paper(question_paper_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT file_name, mime_type, file_data FROM question_papers WHERE id = %s", (question_paper_id,))
    file_record = cur.fetchone()
    cur.close()
    if not file_record:
        return "File not found", 404
    file_name, mime_type, file_data = file_record
    return send_file(
        io.BytesIO(file_data),
        mimetype=mime_type,
        download_name=file_name,
        as_attachment=True
    )









# Route to Child Results
@app.route('/child_results', methods=['GET', 'POST'])
def child_results():
    parent_ID = session.get('parent_ID')
    if not parent_ID:
        return redirect(url_for('parent_login'))
    cur = mysql.connection.cursor()
    # Fetch distinct academic years from both current and history tables
    cur.execute("SELECT DISTINCT academic_year FROM test_results WHERE student_id = %s", (parent_ID,))
    academic_years_current = set([row[0] for row in cur.fetchall()])

    cur.execute("SELECT DISTINCT academic_year FROM test_results_history WHERE student_id = %s", (parent_ID,))
    academic_years_history = set([row[0] for row in cur.fetchall()])

    # Merge and sort academic years
    all_academic_years = sorted(list(academic_years_current.union(academic_years_history)))

    # Initialize variables
    academic_year = None
    test_results = []
    test_results_history = []
    subject_results = {}
    subject_results_history = {}

    if request.method == "POST":
        academic_year = request.form.get("academic_year")

        if academic_year:
            # Fetch current test results
            cur.execute("SELECT * FROM test_results WHERE student_id = %s AND academic_year = %s", (parent_ID, academic_year))
            test_results = cur.fetchall()

            for test in test_results:
                test_id = test[0]  # Assuming test_id is at index 0
                cur.execute("SELECT * FROM subject_results WHERE test_id = %s", (test_id,))
                subject_results[test_id] = cur.fetchall()

            # Fetch historical test results
            cur.execute("SELECT * FROM test_results_history WHERE student_id = %s AND academic_year = %s", (parent_ID, academic_year))
            test_results_history = cur.fetchall()

            for history_test in test_results_history:
                history_test_id = history_test[0]
                cur.execute("SELECT * FROM subject_results_history WHERE test_id = %s", (history_test_id,))
                subject_results_history[history_test_id] = cur.fetchall()

    cur.close()

    return render_template("child_results.html",
                           academic_years = all_academic_years,
                           selected_year = academic_year,
                           test_results = test_results,
                           test_results_history = test_results_history,
                           subject_results = subject_results,
                           subject_results_history = subject_results_history)
    
    
    





# Route to Child Time Tables
@app.route('/child_time_tables')
def child_time_tables():
    parent_ID = session.get('parent_ID')
    if not parent_ID:
        return redirect(url_for('parent_login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT standard FROM student WHERE student_ID = %s", (parent_ID,))
    result = cur.fetchone()
    standard = result[0] if result else None
    cur.execute("SELECT * FROM students_time_table WHERE standard = %s", (standard,))
    time_tables = cur.fetchall()
    class_timetables = [t for t in time_tables if t[2].lower() == 'class time table']
    exam_timetables = [t for t in time_tables if t[2].lower() == 'exam time table']
    cur.close()
    print("Timetables fetched:", time_tables)
    return render_template("child_time_tables.html", time_tables = time_tables, class_timetables = class_timetables, exam_timetables = exam_timetables)










# Route to View Child Timetable
@app.route('/view_child_timetable/<int:timetable_id>')
def view_child_timetable(timetable_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT mime_type, file_data FROM students_time_table WHERE id = %s", (timetable_id,))
    result = cur.fetchone()
    cur.close()
    if result:
        mime_type, file_data = result
        return Response(file_data, mimetype=mime_type)
    return "File not found", 404









# Route to Download Child Time Table
@app.route('/download_child_timetable/<int:timetable_id>')
def download_child_timetable(timetable_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT file_name, mime_type, file_data FROM students_time_table WHERE id = %s", (timetable_id,))
    result = cur.fetchone()
    cur.close()
    if result:
        file_name, mime_type, file_data = result
        return Response(
            file_data,
            mimetype=mime_type,
            headers={"Content-Disposition": f"attachment;filename={file_name}"}
        )
    return "File not found", 404











@app.route('/parents_help_desk', methods=['GET', 'POST'])
def parents_help_desk():
    parent_ID = session.get('parent_ID')

    if not parent_ID:
        return redirect(url_for('parent_login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT roll_number, standard FROM student WHERE student_ID = %s", (parent_ID,))
    child = cur.fetchone()

    if not child:
        cur.close()
        return "Student not found", 404

    child_roll_number = child[0]
    child_standard = child[1]

    if request.method == "POST":
        subject = request.form.get('subject', '').strip() or '-NA-'
        message = request.form.get('message', '').strip() or '-NA-'

        # Document handling
        doc_file = request.files.get('documents')
        doc_data = None
        doc_name = '-NA-'
        doc_mime = None
        if doc_file and doc_file.filename != '':
            doc_name = doc_file.filename
            doc_data = doc_file.read()
            doc_mime = doc_file.mimetype

        # Audio handling
        audio_file = request.files.get('audio')
        audio_data = None
        audio_name = '-NA-'
        audio_mime = None
        if audio_file and audio_file.filename != '':
            audio_name = audio_file.filename
            audio_data = audio_file.read()
            audio_mime = audio_file.mimetype

        try:
            cur.execute("""
                INSERT INTO parents_help_desk (
                    parent_ID, child_roll_number, child_standard,
                    subject, message,
                    documents, documents_filename, document_mime_type,
                    audio, audio_filename, audio_mime_type
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                parent_ID, child_roll_number, child_standard,
                subject, message,
                doc_data, doc_name, doc_mime,
                audio_data, audio_name, audio_mime
            ))
            mysql.connection.commit()
            cur.close()
            print("Request Submitted Successfully")
            return redirect(url_for('raised_complaints'))
        except Exception as e:
            print("Request not submitted:", e)
            cur.close()
            return "There was an error submitting your request", 500

    return render_template("parents_help_desk.html")










# Route to Raised Complaints
@app.route('/raised_complaints')
def raised_complaints():
    parent_ID = session.get('parent_ID')
    if not parent_ID:
        return redirect(url_for('parent_login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM parents_help_desk WHERE parent_ID = %s ORDER BY submitted_at DESC", (parent_ID,))
    complaints = cur.fetchall()
    cur.close()
    return render_template("raised_complaints.html", complaints = complaints)

#####   END OF PARENT FUNCTIONALITIES   #####








#####   STUDENT FUNCTIONALITIES    #####
# Route to Student Login
@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == "POST":
        try:
            student_username = request.form.get("student_username")
            student_password = request.form.get("student_password")
            cur= mysql.connection.cursor()
            cur.execute("SELECT student_ID, student_username, student_password FROM student WHERE student_username = %s", (student_username,))
            student = cur.fetchone()
            cur.close()
            if student:
                if student[2] == student_password:
                    session['student_ID'] = student[0]
                    print("Student Login Successful")
                    return redirect(url_for('student_dashboard'))
                else:
                    print("Invalid Student Password")
                    return render_template("student_login.html")
            else:
                print("Invalid Student Credentials")
                return render_template("student_login.html")
        except Exception as e:
            print("Error Occurred in Student Login:", e)
    return render_template("student_login.html")











# Route to Student Dashboard
@app.route('/student_dashboard')
def student_dashboard():
    student_ID = session.get('student_ID')
    if not student_ID:
        return redirect(url_for('student_login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT student_name FROM student WHERE student_ID = %s", (student_ID,))
    student = cur.fetchone()
    cur.close()
    return render_template("student_dashboard.html", student = student)










# Route to Student Info
@app.route('/student_info')
def student_info():
    student_ID = session.get('student_ID')
    if not student_ID:
        return redirect(url_for('student_login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student WHERE student_ID = %s", (student_ID,))
    student = cur.fetchone()
    cur.close()
    return render_template("student_info.html", student = student)










# Route to Materials According to Standard
@app.route('/materials')
def materials():
    student_ID = session.get('student_ID')
    if not student_ID:
        return redirect(url_for('student_login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT standard FROM student WHERE student_ID = %s", (student_ID, ))
    result = cur.fetchone()
    standard = result[0] if result else None
    cur.execute("SELECT * FROM materials WHERE standard = %s", (standard, ))
    materials = cur.fetchall()
    cur.close()
    return render_template("materials.html", materials = materials, standard = standard)










# Route to Download Materials
@app.route('/download_material/<int:material_id>')
def download_material(material_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT file_name, mime_type, file_data FROM materials WHERE id = %s", (material_id,))
    file_record = cur.fetchone()
    cur.close()
    if not file_record:
        return "File not found", 404
    file_name, mime_type, file_data = file_record
    return send_file(
        io.BytesIO(file_data),
        mimetype=mime_type,
        download_name=file_name,
        as_attachment=True
    )








# Route to Question Papers According to Standard
@app.route('/question_papers')
def question_papers():
    student_ID = session.get('student_ID')
    if not student_ID:
        return redirect(url_for('student_login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT standard FROM student WHERE student_ID = %s", (student_ID, ))
    result = cur.fetchone()
    standard = result[0] if result else None
    cur.execute("SELECT * FROM question_papers WHERE standard = %s", (standard, ))
    question_papers = cur.fetchall()
    cur.close()
    return render_template("question_papers.html", question_papers = question_papers, standard = standard)










# Route to Download Question Papers
@app.route('/download_question_paper/<int:question_paper_id>')
def download_question_paper(question_paper_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT file_name, mime_type, file_data FROM question_papers WHERE id = %s", (question_paper_id,))
    file_record = cur.fetchone()
    cur.close()
    if not file_record:
        return "File not found", 404
    file_name, mime_type, file_data = file_record
    return send_file(
        io.BytesIO(file_data),
        mimetype=mime_type,
        download_name=file_name,
        as_attachment=True
    )









# Route to Student Results
@app.route('/student_results', methods=['GET', 'POST'])
def student_results():
    student_ID = session.get('student_ID')
    if not student_ID:
        return redirect(url_for('student_login'))

    cur = mysql.connection.cursor()

    # Fetch distinct academic years from both current and history tables
    cur.execute("SELECT DISTINCT academic_year FROM test_results WHERE student_id = %s", (student_ID,))
    academic_years_current = set([row[0] for row in cur.fetchall()])

    cur.execute("SELECT DISTINCT academic_year FROM test_results_history WHERE student_id = %s", (student_ID,))
    academic_years_history = set([row[0] for row in cur.fetchall()])

    # Merge and sort academic years
    all_academic_years = sorted(list(academic_years_current.union(academic_years_history)))

    # Initialize variables
    academic_year = None
    test_results = []
    test_results_history = []
    subject_results = {}
    subject_results_history = {}

    if request.method == "POST":
        academic_year = request.form.get("academic_year")

        if academic_year:
            # Fetch current test results
            cur.execute("SELECT * FROM test_results WHERE student_id = %s AND academic_year = %s", (student_ID, academic_year))
            test_results = cur.fetchall()

            for test in test_results:
                test_id = test[0]  # Assuming test_id is at index 0
                cur.execute("SELECT * FROM subject_results WHERE test_id = %s", (test_id,))
                subject_results[test_id] = cur.fetchall()

            # Fetch historical test results
            cur.execute("SELECT * FROM test_results_history WHERE student_id = %s AND academic_year = %s", (student_ID, academic_year))
            test_results_history = cur.fetchall()

            for history_test in test_results_history:
                history_test_id = history_test[0]
                cur.execute("SELECT * FROM subject_results_history WHERE test_id = %s", (history_test_id,))
                subject_results_history[history_test_id] = cur.fetchall()
    cur.close()
    return render_template("student_results.html",
                           academic_years = all_academic_years,
                           selected_year = academic_year,
                           test_results = test_results,
                           test_results_history = test_results_history,
                           subject_results = subject_results,
                           subject_results_history = subject_results_history)
    
    
    
    
    
    
    


# Route to Student Time Table
@app.route('/student_time_tables')
def student_time_tables():
    student_ID = session.get('student_ID')
    if not student_ID:
        return redirect(url_for('student_login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT standard FROM student WHERE student_ID = %s", (student_ID,))
    result = cur.fetchone()
    standard = result[0] if result else None
    cur.execute("SELECT * FROM students_time_table WHERE standard = %s", (standard,))
    time_tables = cur.fetchall()
    class_timetables = [t for t in time_tables if t[2].lower() == 'class time table']
    exam_timetables = [t for t in time_tables if t[2].lower() == 'exam time table']
    cur.close()
    print("Timetables fetched:", time_tables)
    return render_template("student_time_tables.html", time_tables = time_tables, class_timetables = class_timetables, exam_timetables = exam_timetables)









# Route to View Student Timetable
@app.route('/view_student_timetable/<int:timetable_id>')
def view_student_timetable(timetable_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT mime_type, file_data FROM students_time_table WHERE id = %s", (timetable_id,))
    result = cur.fetchone()
    cur.close()
    if result:
        mime_type, file_data = result
        return Response(file_data, mimetype=mime_type)
    return "File not found", 404









# Route to Download Student Time Table
@app.route('/download_student_timetable/<int:timetable_id>')
def download_student_timetable(timetable_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT file_name, mime_type, file_data FROM students_time_table WHERE id = %s", (timetable_id,))
    result = cur.fetchone()
    cur.close()
    if result:
        file_name, mime_type, file_data = result
        return Response(
            file_data,
            mimetype=mime_type,
            headers={"Content-Disposition": f"attachment;filename={file_name}"}
        )
    return "File not found", 404

#####   END OF STUDENT FUNCTIONALITIES    #####









# Add CORS headers to all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response










# Route to Logout
@app.route('/logout')
def logout():
    session.clear()
    return render_template("index.html")







# Running the Application
if __name__ == "__main__":
    app.run(host="192.168.0.9", debug=True)