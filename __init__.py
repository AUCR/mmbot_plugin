"""AUCR mmbot blueprint plugin."""
# coding=utf-8
# If you want the model to create the a table for the database at run time, import it here in the init
import os
from aucr_app.plugins.tasks.mq import get_a_task_mq
from aucr_app.plugins.mmbot_plugin.mmbot_run import call_back
from aucr_app.plugins.mmbot_plugin.routes import mmbot_page
from multiprocessing import Process


def load(app):
    """Load overrides for Tasks plugin to work properly."""
    mmbot_processor = os.environ.get('MMBOT')
    tasks = "mmbot"
    rabbitmq_server = os.environ.get('RABBITMQ_SERVER')
    rabbitmq_username = os.environ.get('RABBITMQ_USERNAME')
    rabbitmq_password = os.environ.get('RABBITMQ_PASSWORD')
    if mmbot_processor:
        p = Process(target=get_a_task_mq, args=(tasks, call_back, rabbitmq_server, rabbitmq_username,
                                                rabbitmq_password))
        p.start()

