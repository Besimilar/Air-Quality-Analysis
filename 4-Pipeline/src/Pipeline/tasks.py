# @author Hongwei
from __future__ import absolute_import, unicode_literals
from .celery import app
import subprocess


@app.task(name='tasks.run')
def run():
    subprocess.call(['./Pipeline/run.sh'])
    return 0
