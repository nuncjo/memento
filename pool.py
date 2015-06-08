#-*- coding:utf-8 -*-
from models.task import TaskModel
from models.idea import IdeaModel

task_pool = TaskModel("memento.db")
task_pool.create_table()
idea_pool = IdeaModel("memento.db")
idea_pool.create_table()
