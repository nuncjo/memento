#-*- coding: utf-8 -*-

import logging
import sqlite3 as sq
from factory import dict_factory

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


class TaskModel(object):
    def __init__(self, database, connection=None):

        self.database = database

        if connection:
            self.connection = connection
        else:
            self.connection = sq.connect(self.database, detect_types=sq.PARSE_DECLTYPES, check_same_thread=False)

        self.connection.row_factory = dict_factory
        self.cr = self.connection.cursor()


    def add_task(self, data):
        self.cr.execute(
            'INSERT INTO Tasks (id, id_idea, date, datetime, cyclic, action, message, priority, done) VALUES (:id, :id_idea, :date, :datetime, :cyclic, :action, :message, :priority, :done);',
            data)
        self.connection.commit()

    def delete_task(self, data):
        self.cr.execute('DELETE FROM Tasks WHERE id=:id;', data)
        self.connection.commit()

    def set_done_task(self, data):
        self.cr.execute('UPDATE Tasks SET done=:done WHERE id=:id;', data)
        self.connection.commit()

    def update_task(self, data):
        self.cr.execute(
            'UPDATE Tasks SET id_idea=:id_idea, priority=:priority, date=:date, datetime=:datetime, cyclic=:cyclic, action=:action, message=:message,  done=:done WHERE id=:id;',
            data)
        self.connection.commit()

    def update_task_date(self, data):
        self.cr.execute('UPDATE Tasks SET date=:date, datetime=:datetime WHERE id=:id;', data)
        self.connection.commit()

    def delay_task(self, data):
        self.cr.execute('UPDATE Tasks SET datetime=:datetime WHERE id=:id;', data)
        self.connection.commit()

    def update_task_short(self, data):
        self.cr.execute('UPDATE Tasks SET priority=:priority, datetime=:datetime, date=:date WHERE id=:id;', data)
        self.connection.commit()

    def refresh_daily(self, data):
        self.cr.execute('UPDATE Tasks SET showed=:showed, done=:done WHERE cyclic=:cyclic and showed<:showed;', data)
        self.connection.commit()

    def load_tasks(self, offset=0, limit=100):
        result = self.cr.execute("SELECT * from Tasks LIMIT ? OFFSET ?", (limit, offset))
        tasks = result.fetchall()
        return tasks

    def load_tasks_period(self, date_start, date_end, done=0, cyclic=1):
        result = self.cr.execute(
            "SELECT * from Tasks WHERE datetime>='{}' AND datetime<='{}' AND done=={} OR cyclic=={} AND done=={} ORDER BY datetime ASC".format(
                date_start, date_end, done, cyclic, done))
        tasks = result.fetchall()
        return tasks

    def load_task(self, id):
        result = self.cr.execute("SELECT * from Tasks WHERE id={}".format(id))
        task = result.fetchone()
        return task

    def create_table(self):
        result = None
        try:
            result = self.cr.execute("""
                CREATE TABLE Tasks(
                    id INTEGER PRIMARY KEY ASC,
                    id_idea INTEGER,
                    date DATE,
                    datetime TIMESTAMP,
                    cyclic BOOLEAN,
                    action INTEGER,
                    message TEXT,
                    priority CHAR,
                    done BOOLEAN,
                    showed DATE
                    )
            """)
        except sq.OperationalError as err:
            _logger.info("Database already exists: {}".format(err))
        except Exception as err:
            _logger.debug("Can't create database: {}".format(err))
        finally:
            return result
