#-*- coding: utf-8 -*-

import logging
import sqlite3 as sq
from factory import dict_factory

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


class IdeaModel(object):

    def __init__(self, database, connection=None):

        self.database = database

        if connection:
            self.connection = connection
        else:
            self.connection = sq.connect(self.database, detect_types=sq.PARSE_DECLTYPES)

        self.connection.row_factory = dict_factory
        self.cr = self.connection.cursor()

    def add_idea(self, data):
        self.cr.execute('INSERT INTO Ideas (id, id_task, id_attachment, name, description, archived) VALUES (:id, :id_task, :id_attachment, :name, :description, :archived);', data)
        self.connection.commit()

    def delete_idea(self, data):
        self.cr.execute('DELETE FROM Ideas WHERE id=:id;', data)
        self.connection.commit()

    def update_idea(self, data):
        self.cr.execute('UPDATE Ideas SET id_task=:id_task, id_attachment=:id_attachment, name=:name, description=:description, archived=:archived WHERE id=:id;', data)
        self.connection.commit()

    def set_archived_idea(self, data):
        self.cr.execute('UPDATE Ideas SET archived=:archived WHERE id=:id;', data)
        self.connection.commit()

    def load_ideas(self, offset=0, limit=20):
        result = self.cr.execute("SELECT * from Ideas LIMIT {} OFFSET {}".format(limit, offset))
        ideas = result.fetchall()
        return ideas
      
    def load_idea(self, id):
        result = self.cr.execute("SELECT * from Ideas WHERE id={}".format(id))
        idea = result.fetchone()
        return idea

    def load_idea_by_task_id(self, id):
        #TODO: handle more than one task
        result = self.cr.execute("SELECT * from Ideas WHERE id_task={}".format(id))
        idea = result.fetchone()
        return idea

    def create_table(self):
        result = None
        try:
            result = self.cr.execute("""
                CREATE TABLE Ideas (
                    id INTEGER PRIMARY KEY ASC,
                    id_task INTEGER,
                    id_attachment INTEGER,
                    name TEXT,
                    description TEXT,
                    archived BOOLEAN
                    )
            """)
        except sq.OperationalError as err:
            _logger.info("Database already exists: {}".format(err))
        except Exception as err:
            _logger.info("Can't create database: {}".format(err))
        finally:
            return result
