# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web

from dbconn import db_cursor

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("web/main.html")


class StudentListHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("web/stu_list.html", student = dal_list_student())

class StudentEditHandler(tornado.web.RequestHandler):
    def get(self, stu_sn):

        stu = None
        if stu_sn != 'new' :
            stu = dal_get_student(stu_sn)
        
        if stu is None:
            stu = dict(stu_sn='new', stu_id='', name='',stu_bir='', stu_no='',  gda='')

        self.render("web/stu_edit.html", student = stu)

    def post(self, stu_sn):
        stu_id=self.get_argument('stu_id')
        name = self.get_argument('name', '')
        stu_bir=self.get_argument('stu_bir')
        stu_no = self.get_argument('stu_no')        
        gda = self.get_argument('gda', '')

        if stu_sn == 'new' :
            dal_create_student(stu_id, name, stu_bir, stu_no, gda)
        else:
            dal_update_student(stu_sn, stu_id, name, stu_bir, stu_no, gda)

        self.redirect('/stulist')

class StudentDelHandler(tornado.web.RequestHandler):
    def get(self, stu_sn):
        dal_del_student(stu_sn)
        self.redirect('/stulist')

# -------------------------------------------------------------------------

def dal_list_student():
    data = []
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        SELECT stu_sn, stu_id, name, stu_bir, stu_no, gda FROM student ORDER BY stu_no 
        """
        cur.execute(s)      
        for r in cur.fetchall():
            stu = dict(stu_sn=r[0],stu_id=r[1] ,name=r[2], stu_bir=r[3],stu_no=r[4], gda=r[5])
            data.append(stu)
    return data


def dal_get_student(stu_sn):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        SELECT stu_sn,stu_id, name, stu_bir, stu_no, gda FROM student WHERE stu_sn=%s
        """
        cur.execute(s, (stu_sn, ))
        r = cur.fetchone()
        if r :
            return dict(stu_sn=r[0],stu_id=r[1] ,name=r[2],stu_bir=r[3], stu_no=r[4], gda=r[5])


def dal_create_student(stu_id,name,stu_bir,stu_no, gda):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        cur.execute("SELECT nextval('seq_stu_sn')")
        stu_sn = cur.fetchone()
        assert stu_sn is not None

        print('新学生学号%s: ' % stu_id)

        s = """
        INSERT INTO student (stu_sn, stu_id,name, stu_bir, stu_no,  gda) 
        VALUES (%(stu_sn)s,%(stu_id)s,%(name)s, %(stu_bir)s, %(stu_no)s,  %(gda)s)
        """
        cur.execute(s, dict(stu_sn=stu_sn,stu_id=stu_id,name=name, stu_bir=stu_bir, stu_no=stu_no,  gda=gda))


def dal_update_student(stu_sn, stu_id,name, stu_bir, stu_no,  gda):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        UPDATE student SET
          stu_no=%(stu_no)s,
          stu_id=%(stu_id)s,
          name=%(name)s, 
          stu_bir=%(stu_bir)s,          
          gda=%(gda)s 
        WHERE stu_sn=%(stu_sn)s
        """
        cur.execute(s, dict(stu_sn=stu_sn, stu_id=stu_id,name=name, stu_bir=stu_bir, stu_no=stu_no,  gda=gda))


def dal_del_student(stu_sn):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        DELETE FROM student WHERE stu_sn=%(stu_sn)s
        """
        cur.execute(s, dict(stu_sn=stu_sn))
        print('删除%d条记录' % cur.rowcount)
