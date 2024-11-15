# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Hobby(models.Model):
    _name = 'hobby.hobby'
    _description = 'This is hobby profile.'

    name = fields.Char(string='Name')
    # student_list = fields.One2many("student.student", "school_id", string='Student List')
