from flask import Flask, render_template, redirect, url_for, request,session
import mysql.connector
from database import db_class


#iinitialize db
my_db_connect = db_class.mysql_connector('localhost','root','password','nptel_management')


app = Flask(__name__)

#set a secret key
app.secret_key = 'BAD_SECRET_KEY'

'''
# Define MySQL connection parameters
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'nptel_management'
}

# Initialize MySQL connection
db_connection = mysql.connector.connect(**mysql_config)
cursor = db_connection.cursor()

# Define MySQL tables creation queries
table_queries = [
    """
    CREATE TABLE IF NOT EXISTS student (
        email_id VARCHAR(255) PRIMARY KEY,
        st_name VARCHAR(255),
        regno INT,
        dept VARCHAR(255),
        acc_year VARCHAR(255)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS course (
        c_code VARCHAR(255) PRIMARY KEY,
        c_name VARCHAR(255),
        weeks INT,
        nptel_link VARCHAR(255),
        if_yes VARCHAR(3)
    )
    """
    # Add more table creation queries as needed
]

# Execute table creation queries
for query in table_queries:
    cursor.execute(query)
db_connection.commit()
print("Tables created successfully")

'''


'''users = {
    'ksgayathri@ssn.edu.in': {'password': 'admin123', 'role': 'admin'},
    'nithyasri2210946@ssn.edu.in': {'password': 'student123', 'role': 'student'}
}'''


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']

        #store the email in the sessions
        session['username'] = email
        
        #check if user is student or user
        user = my_db_connect.validate_password(email,password)
        #if student push to student page
        if user == 'student':
            return redirect(url_for('student'))
        #else push to admin homepage
        if user == 'teacher':
            return redirect(url_for('admin_homepg'))
        else:
            return "Invalid username or password"

@app.route('/admin')
def admin_homepg():
    return render_template('admin_homepg.html')

@app.route('/student')
def student():
    #get username from session
    std_username = session['username']
    print(std_username)
    #get data from database
    std_info = my_db_connect.get_details_student(std_username)
    print(std_username,std_info)
    #pass it to html
    return render_template('student_homepg.html',std_info = std_info)

@app.route('/registration')
def registration():
    #get the username 
    std_username = session['username']
    #get the available courses for the username
    available_course = my_db_connect.get_available_course(std_username)
    course_data = {'Database Management Systems': {'c_code': 'IT101', 'c_name': 'Database Management Systems', 'weeks': 12, 'nptel_link': 'https://nptel.com/it101', 'dept': 'IT', 'acc_year': '2024-2025'}, 'Mechatronics': {'c_code': 'ME501', 'c_name': 'Mechatronics', 'weeks': 8, 'nptel_link': 'https://nptel.com/me501', 'dept': 'IT', 'acc_year': '2021-2022'}}
    #pass it to html
    return render_template('student_registration.html',available_course = available_course,course_data = course_data)


@app.route('/upload_certificate', methods=['POST'])
def upload_certificate():
    if request.method == 'POST':
        # Get form data
        email_id = session['username']
        course = request.form['course']
        marks = request.form['marks']
        certificate_file = request.files['certificate']

        if certificate_file:
            # Read file content as binary
            certificate_data = certificate_file.read()
            print(certificate_data)
            
            try:
                # Insert certificate data into MySQL table
                sql = f"INSERT INTO certificate (email_id, c_code, marks, certificate_data) VALUES (%s, %s, %s, %s)"
                my_db_connect.cursor.execute(sql, (email_id, course, marks, certificate_data))
                my_db_connect.db.commit()
            except Exception as e:
                # Handle database errors
                print("Error:", e)
                return "Upload failed. Please try again."
            
            return "Upload successful!"
        
@app.route('/results')
def results():
    return render_template('marksheet_upload.html')

# Mock data for demonstration purposes
mock_student_marks = {
    'Math': 85,
    'Science': 90,
    'History': 75,
    'English': 88,
    'Computer Science': 92
}

@app.route('/statistics')
def statistics():
    # Sort the student marks in decreasing order of scores
    sorted_marks = sorted(mock_student_marks.items(), key=lambda x: x[1], reverse=True)
    return render_template('student_history.html', student_marks=sorted_marks)

@app.route('/verification')
def verification():
    #get the list of all students who appeared for nptel
    std_marks_info = my_db_connect.student_details()
    #pass it to html
    return render_template('verify.html',std_marks_info = std_marks_info)

@app.route('/select')
def select():
    return render_template('course_select.html')

@app.route('/credits')
def credits():
    pass

@app.route('/admin_result')
def admin_result():
    #get all the verified student details
    verified_details = my_db_connect.verified_details()
    #pass it to html
    return render_template('admin_viewer.html',verified_details = verified_details)

@app.route('/verify_cert')
def verify_cert():
    return render_template('cert_check.html')

if __name__ == '__main__':
    app.run(debug=True)
