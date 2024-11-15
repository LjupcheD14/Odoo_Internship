# -*- coding: utf-8 -*-

from odoo import fields, models

class Student(models.Model):
    _name = "student.student"
    _description = "This is student profile"

    name = fields.Char("Name")
    name1 = fields.Char("Name1")
    name2 = fields.Char("Name2")
    name3 = fields.Char("Name3")
    name4 = fields.Char("Name4")
