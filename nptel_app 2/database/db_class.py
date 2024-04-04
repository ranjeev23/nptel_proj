import mysql.connector

#create a class for populating mysql values
class mysql_connector:
    
    #initializing the host, user, password and database
    def __init__(self,host,user,password,database):
        self.host = host
        self.user = user
        self.password = password 
        self.database = database
        self.cursor = self.init_mysql_conn()

    #initialize database_connection
    def init_mysql_conn(self):
        try:
            mydb = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password =self.password,
                database = self.database
            )
            print('successfully_connected')
            self.db=mydb
            return mydb.cursor()
        except:
            print('error occured in setting connection with database')

    #create the table in the given database
    def create_table(self,table_name,col_dtype_dict:dict):
        
        values = ''

        values+='('
        for key in col_dtype_dict:
            values+=str(key)
            values+=' '
            values+=str(col_dtype_dict[key])
            values+=','
        values=values[0:len(values)-1]
        values+=')'

        sql ='create table if not exists ' + table_name + values + ';'

        self.cursor.execute(sql)

    #insert table given table_name,values type is list
    def insert(self,table_name,values:tuple):

        sql = 'INSERT INTO '+ table_name + ' VALUEs ' + str(values)

        self.cursor.execute(sql)

        self.db.commit()


    #fetch all values given a databse,tuple of values
    def fetchall(self,table_name):
        
        self.cursor.execute('select * from ' + table_name)

        results = self.cursor.fetchall()

        for values in results:
            print(values)

    def validate_password(self,email,pwd):
        #function to validate the password given by the user
        #input is email and password
        self.cursor.execute("SELECT pass_word FROM student WHERE email_id = %s", (email,))
        student = self.cursor.fetchone()

        # Check if the username exists in the teacher table
        self.cursor.execute("SELECT pass_word FROM teacher WHERE email_id = %s", (email,))
        teacher = self.cursor.fetchone()

        if student:
            if student[0] == pwd:
                return 'student'
        elif teacher:
            if teacher[0] == pwd:
                return 'teacher'
        else:
            return None

      
    def get_details_student(self,email):
        #function to get details of students for home page of student
        #input is email of the  student
        dic = dict()

        self.cursor.execute(f"select st_name, regno, dept, acc_year from student where email_id = '{email}'")

        std_details = self.cursor.fetchone()

        

        format = ('name','regno','dept','acc_year')

        for i in range(len(std_details)):
            dic[format[i]] = std_details[i]

        print(dic)

        #output is the details in formatt 
        #{'st_name': 'Emily Davis', 'regno': 1004, 'dept': 'Civil Engineering', 'acc_year': '2025-2026'}
        return dic
    
    def completed_course_details(self,email):
        #function to get th student completed course details given email
        #input is the email of the student
        dic = dict()

        self.cursor.execute(f"select nm.c_code, c.c_name, c.weeks, nm.verified_marks from course c join nptel_marks nm on nm.c_code = c.c_code where nm.email_id = '{email}'")

        comp_course_details = self.cursor.fetchall()

        format = ('c_code', 'c_name', 'weeks', 'marks')

        for i in range(len(comp_course_details)):
            for j in range(len(format)):
                if i ==0:
                    dic[format[j]] = [comp_course_details[i][j]]
                else:
                    dic[format[j]].append(comp_course_details[i][j])

        print(dic)
        #output is in the formatt
        #{'c_code': ['EE201', 'ME301'], 'c_name': ['Electrical Circuits', 'Mechanical Dynamics'], 'weeks': [10, 14], 'marks': [88, 90]}
        return dic

    def add_course(self,c_code,c_name,weeks,nptel_link,if_yes):
        #function to add the course to the course_table
        #input is the (c_code,c_name,weeks,nptel_link,if_yes)
        #example input 'CHEM501', 'Chemical Kinetics', 8, 'https://nptel.com/chem501', 'Yes'
        #output data is added to db successfully
        self.insert('course',(c_code,c_name,weeks,nptel_link,if_yes))
    
    def display_c_code(self):
        self.cursor.execute('select c_code from courses')
        data = self.cursor.fetchall()
        return data
    
    def display_c_name(self):
        self.cursor.execute('select c_name from courses')
        data = self.cursor.fetchall()
        return data

    def display_dept(self):
        self.cursor.execute('select distinct(dept) from student')
        data = self.cursor.fetchall()
        return data
    
    def display_sem(self):
        self.cursor.execute('select distinct(sem) from student')
        data = self.cursor.fetchall()
        return data
    
    def register_course(self,email,c_code):
        #code to insert into the registered course for the user
        self.insert('register_course',(email,c_code))

    def upload_marksheet(self,email,c_code,marks,pdf,verified,qr_code):
        #function to upload marksheet of user to data base
        #input is email,c_code,marks,pdf,verified,qr_code
        #no output as it is insert stmt only
        self.insert('certificate',(email,c_code,marks,pdf,verified,qr_code))

    #needs to be changed
    def get_available_course(self, email):
        #function to get the available courses that the user has registered needs to be changes
        #input is email id
        #output in formatt
        self.cursor.execute(f"select c.c_name from course c join set_course s on c.c_code = s.c_code where sem = (select sem from student where email_id = '{email}')")
        data = self.cursor.fetchall()

        data = [sub[0] for sub in data]
        print(data)
        return data
    
    #get course details
    def get_course_details(self,lis_c_name):
        #req dic
        dic = dict()
        for c_name in lis_c_name:
            dic.update(self._get_course_details(c_name))
        print(dic)
        return dic
    
    #get the course details
    def _get_course_details(self,c_name):
        #write sql query to get the course details
        query = f"""select c.c_code,c.c_name,weeks,nptel_link,dept,acc_year from course c join set_course s on c.c_code = s.c_code where c.c_name = '{c_name}'"""
        #executre the query
        self.cursor.execute(query)
        #get all the data 
        details = self.cursor.fetchall()
        #set a dictionary
        dic = {}
        #set value as a dictionary of detail_name and detail
        order = ('c_code','c_name','weeks','nptel_link','dept','acc_year')
        #loop through data
        for data in details:
            #set the course as key
            key = data[1] 
            value = {}
            for index in range(len(data)):
                value[order[index]] = data[index]
            #set the primary key's value as value
            dic[key] = value
        #end
        print(dic)
        return dic
    
    #get the name sem sub marks from table
    def student_details(self):
        #write query
        query = '''select s.st_name, s.sem, c.c_name, ce.marks from student s join certificate ce on ce.email_id = s.email_id join course c on c.c_code = ce.c_code order by s.sem;'''
        #execute query 
        self.cursor.execute(query)
        #fetch the query
        details = self.cursor.fetchall()
        #convert to req formatt
        order = ('name','sem','c_name','ce_marks')
        lis = []
        for data in details:
            dic = {}
            for index in range(len(order)):
                dic[order[index]] = data[index]
            print(dic)
            lis.append(dic)
        #return
        print(lis)
        return lis
    
    #get data from nptel_marks table
    def verified_details(self):
        #query to get student id, name subject_name, score
        query = '''
        select n.email_id,s.st_name, c.c_name, n.verified_marks 
        from nptel_marks n
        join student s on s.email_id = n.email_id
        join course c on c.c_code = n.c_code;
        '''
        #excetue and fetch the query
        self.cursor.execute(query)
        details = self.cursor.fetchall()
        #convert to req format json
        order = ('email','name','subject','marks')
        lis = []
        for data in details:
            dic = {}
            for index in range(len(order)):
                dic[order[index]] = data[index]
            print(dic)
            lis.append(dic)
        #return
        print(lis)
        return lis
    
    
    


    
my_db_connect = mysql_connector('localhost','root','password','nptel_management')

#my_db_connect.create_table('sample2',{'name':'TEXT','age':'TEXT'})

#my_db_connect.create_table('sample2',{'dig_id':'NUM','age':'TEXT'})

#my_db_connect.insert('nptel_marks',('emily.d@email.com', 'ME301', 90, 85))

#my_db_connect.fetchall('course')

#print(my_db_connect.validate_password('rahul.sharma@ssn.edu.in','rahulpass123'))

#my_db_connect.get_details_student('rahul.sharma@ssn.edu.in')

#my_db_connect.completed_course_details('emily.d@email.com')

#my_db_connect.add_course('CHEMS501', 'Chemicals Kinetics', 8, 'https://nptel.com/chem501', 'Yes')

#my_db_connect.get_available_course('rahul.sharma@ssn.edu.in')

#my_db_connect.get_course_details(['Database Management Systems','Mechatronics'])

#my_db_connect.student_details()

my_db_connect.verified_details()