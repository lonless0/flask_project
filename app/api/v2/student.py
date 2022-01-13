"""
    a standard CRUD template of student
    通过 学生 来实现一套标准的 CRUD 功能，供学习
    :copyright: © 2020 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from flask import g, request
from lin import permission_meta
from lin.apidoc import DocResponse, api
from lin.exception import Success
from lin.jwt import group_required, login_required
from lin.redprint import Redprint

from app.exception.api import BookNotFound
from app.model.v2.student import Student
from app.validator.schema import (
    AuthorizationSchema,
    StudentInSchema,
    StudentOutSchema,
    StudentQuerySearchSchema,
    StudentSchemaList,
)

student_api = Redprint("student")


@student_api.route("/<int:id>")
@api.validate(
    resp=DocResponse(BookNotFound, r=StudentOutSchema),
    tags=["学生"],
)
def get_student(id):
    """
    获取id指定学生的信息
    """
    student = Student.get(id=id)
    if student:
        return student
    raise BookNotFound


@student_api.route("")
@api.validate(
    resp=DocResponse(r=StudentSchemaList),
    tags=["学生"],
)
def get_students():
    """
    获取学生列表
    """
    return Student.get(one=False)


@student_api.route("/search")
@api.validate(
    query=StudentQuerySearchSchema,
    resp=DocResponse(r=StudentSchemaList),
    tags=["学生"],
)
def search():
    """
    关键字搜索学生
    """
    return Student.query.filter(
        Student.name.like("%" + g.q + "%"), Student.delete_time == None
    ).all()


@student_api.route("", methods=["POST"])
@login_required
@api.validate(
    headers=AuthorizationSchema,
    json=StudentInSchema,
    resp=DocResponse(Success(12)),
    tags=["学生"],
)
def create_student():
    """
    创建学生
    """
    student_schema = request.context.json
    Student.create(**student_schema.dict(), commit=True)
    return Success(12)


@student_api.route("/<int:id>", methods=["PUT"])
@login_required
@api.validate(
    headers=AuthorizationSchema,
    json=StudentInSchema,
    resp=DocResponse(Success(13)),
    tags=["学生"],
)
def update_student(id):
    """
    更新学生信息
    """
    student_schema = request.context.json
    student = Student.get(id=id)
    if student:
        student.update(
            id=id,
            **student_schema.dict(),
            commit=True,
        )
        return Success(13)
    raise BookNotFound


@student_api.route("/<int:id>", methods=["DELETE"])
@permission_meta(name="删除学生", module="学生")
@group_required
@api.validate(
    headers=AuthorizationSchema,
    resp=DocResponse(BookNotFound, Success(14)),
    tags=["学生"],
)
def delete_student(id):
    """
    传入id删除对应学生
    """
    student = Student.get(id=id)
    if student:
        # 删除学生，软删除
        student.delete(commit=True)
        return Success(14)
    raise BookNotFound
