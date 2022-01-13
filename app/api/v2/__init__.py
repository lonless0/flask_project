"""
    :copyright: © 2020 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from flask import Blueprint

from app.api.v2 import student


def create_v2():
    bp_v2 = Blueprint("v2", __name__)
    student.student_api.register(bp_v2)
    return bp_v2
