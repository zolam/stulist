#! /usr/bin/env python3
# -*- coding:UTF-8 -*-

from dbconn import db_cursor

def create_db():
    sqlstr = """
    DROP TABLE IF EXISTS student;

    CREATE TABLE IF NOT EXISTS student  (
        stu_sn   INTEGER,     --内部序号
        stu_id   INTEGER,     --学号
        name     TEXT,        --姓名
        stu_bir   DATE,       --出生日期
        stu_no   INTEGER,     --班级        
        gda      TEXT,        --性别
        PRIMARY KEY(stu_id)
    );
    -- CREATE UNIQUE INDEX idx_student_no ON student(stu_no);

    CREATE SEQUENCE seq_stu_sn 
        START 10000 INCREMENT 1 OWNED BY student.stu_sn;

    """
    with db_cursor() as cur :
        cur.execute(sqlstr) # 执行SQL语句
    
def init_data():
    sqlstr = """
    DELETE FROM student;

    INSERT INTO student (stu_sn,stu_id,stu_bir,stu_no, name,gda)  VALUES 
        (101, '1310201' , '19950101' , 1302 ,  '张三' , '男'), 
        (102, '1310401' , '19950202' , 1304 ,  '李四' , '女'),
        (103, '1310301' , '19950303' , 1303 ,  '王五' , '男');

    """
    with db_cursor() as cur :
        cur.execute(sqlstr)    

if __name__ == '__main__':
    create_db()
    init_data()
    print('数据库已初始化完毕！')

