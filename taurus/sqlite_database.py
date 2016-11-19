#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import sqlite3
import pkg_resources
from ipy_progressbar import ProgressBar

class SQLiteDatabase:


    def __init__(self,**kwargs):
        #super().__init__(**kwargs)
        self.kwargs=kwargs
        database_name=kwargs.get('database_name','taurus.db')
        self.db_connection=sqlite3.connect(database_name)
        self.do_progressbar=kwargs.get('progressbar',True)
        #
        self.execute=self.db_connection.execute

    def get_sql_form_file(self,script_name):
        return pkg_resources.resource_stream(__name__,'SQL/'+script_name+'.sql').read().decode('ascii')

    def build_sql(self,script_string,args={}):
        return script_string.format(**args)


    def commit(self):
        self.db_connection.commit()

    def one(self,script_name,args={}):
        cursor=self.do(script_name,args)
        if cursor:
            return cursor.fetchone()

    def transaction(self,script_name,data):
        sql_string=self.get_sql_form_file(script_name)
        assert hasattr(data,'__iter__')

        self.db_connection.executemany(sql_string,data)
        self.commit()

    def do(self,script_name,args={}):
        '''
        script contains ; is script and executed without output
        script without ; is for fetching output

        :param script_name:
        :param args:
        :return:
        '''
        sql_string=self.get_sql_form_file(script_name)
        if ';' not in sql_string:
            return self.db_connection.execute(sql_string,args)
        elif ':' in sql_string:
            query_list=sql_string.split(';')
            for query in query_list:
                self.db_connection.execute(query,args)
        else:
            self.db_connection.executescript(sql_string)


    def table_exists(self,dataset_name):
        c=self.db_connection.cursor()
        return not c.execute(
            "SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?",
            [dataset_name]).fetchone()[0]==0

    def _taurus_progressbar_cursor(self,script):
        if self.do_progressbar:
            return ProgressBar(self.do(script).fetchall())
        else:
            return self.do(script).fetchall()


