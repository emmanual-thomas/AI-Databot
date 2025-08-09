import google.generativeai as genai
import sqlite3
import pandas as pd
import os
import numpy as np


api_key1='AIzaSyCEyKMGgq1VAkuoGAdyeZR3FcUHQSjKiKI'
api_key2="AIzaSyDAxglkJMZiptI5U7iiEajpbGi3DglgR2E"
api_key3='AIzaSyDAxglkJMZiptI5U7iiEajpbGi3DglgR2E'
genai.configure(api_key=api_key1)
class Bot():
    def __init__(self,mode=0):
        self.model=genai.GenerativeModel('gemini-pro')
        self.mode=mode
        self.cache_data=None
        self.mode_used=None
        self.db="database_adress"
        self.normal_mode=["""
        You are a normal chatbot with no limitations.
                          
                          
                          
                          """]
        self.analytics_mode=["You are a god level data analyst"]
        self.english_qprompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the following schema:
   -- Employees Table
CREATE TABLE Employees (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone_number VARCHAR(20),
    address VARCHAR(255),
    department_id INT,
    manager_id INT,
    FOREIGN KEY (department_id) REFERENCES Departments(department_id),
    FOREIGN KEY (manager_id) REFERENCES Employees(employee_id)
);

-- Departments Table
CREATE TABLE Departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100)
);

-- LeaveRequests Table
CREATE TABLE LeaveRequests (
    leave_request_id INT PRIMARY KEY,
    employee_id INT,
    leave_type VARCHAR(50),
    start_date DATE,
    end_date DATE,
    status VARCHAR(20),
    reason TEXT,
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

-- Attendance Table
CREATE TABLE Attendance (
    attendance_id INT PRIMARY KEY,
    employee_id INT,
    date DATE,
    clock_in_time TIME,
    clock_out_time TIME,
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

-- CalendarEvents Table
CREATE TABLE CalendarEvents (
    event_id INT PRIMARY KEY,

    event_name VARCHAR(100),
    start_datetime DATETIME,
    end_datetime DATETIME,
    description TEXT
);

-- TrainingPrograms Table
CREATE TABLE TrainingPrograms (
    program_id INT PRIMARY KEY,
    program_name VARCHAR(100),
    program_description TEXT,
    start_date DATE,
    end_date DATE
);

-- TrainingEnrollments Table
CREATE TABLE TrainingEnrollments (
    enrollment_id INT PRIMARY KEY,
    employee_id INT,
    program_id INT,
    enrollment_date DATE,
    completion_status VARCHAR(20),
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id),
    FOREIGN KEY (program_id) REFERENCES TrainingPrograms(program_id)
);

-- Payroll Table
CREATE TABLE Payroll (
    payroll_id INT PRIMARY KEY,
    employee_id INT,
    pay_period_start_date DATE,
    pay_period_end_date DATE,
    gross_salary DECIMAL(10, 2),
    deductions DECIMAL(10, 2),
    net_salary DECIMAL(10, 2),
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

-- PerformanceMetrics Table
CREATE TABLE PerformanceMetrics (
    metric_id INT PRIMARY KEY,
    employee_id INT,
    metric_name VARCHAR(100),
    metric_value DECIMAL(10, 2),
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

-- HRAnalytics Table
CREATE TABLE HRAnalytics (
    analytics_id INT PRIMARY KEY,
    metric_name VARCHAR(100),
    metric_value DECIMAL(10, 2),
    date DATE
);/n
you have to convert given instruction into sql statement according to the schema 
also the sql code should not have ``` in beginning or end and sql word in output



    """


        ]
        self.eng_response_prompt = [
        """
            I see you're an expert in understanding SQL queries! 
        I'll provide you with an SQL statement and its output. 
            Your task is to translate the sql statement and the result in simple English form in leeat possible words. and strictly don't output sql statements. \n\n
        For example,\nExample 1 - 
        SELECT COUNT(*) FROM randomtable ; : some random number 
        your output should be something like , There are five students. also don't include any info about the sql query just provide the result in normal form
    
    """
        ]
    def response(self,question,prompt):
        response=self.model.generate_content([prompt[0],question])
        return response.text
    def read_sql_query(self,sql,db):
        conn=sqlite3.connect(db)
        cur=conn.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        conn.commit()
        conn.close()
        return rows
    def eng_response(self,question):
        if self.mode==0:
            self.mode_used=self.normal_mode
        elif self.mode==1:
            self.mode_used=self.analytics_mode
        else :
            self.mode_used=self.english_qprompt     
        
        
        response=self.response(question,self.mode_used)
        print(response)
        if self.mode==0:
            return response
        elif self.mode==2:    
            data=self.read_sql_query(response,self.db)
            
            self.cache_data=self.convert_to_csv(data)
            english_res=self.response(str(response)+":"+str(data),self.eng_response_prompt)
        else:
            pass    
        return english_res
    def convert_to_csv(self,response_from_db):
        frame=pd.DataFrame(response_from_db)
        frame.to_csv(self.is_filename_valid())
        return frame
    def is_filename_valid(self):
        current_dir=os.getcwd()
        filename="output"
        files=os.listdir(current_dir)
        random_num=""
        if filename+".csv" in files:
            random_num=np.random.randint(0,500)


        return filename+str(random_num)+".csv"
    
        