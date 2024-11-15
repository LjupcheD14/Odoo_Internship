# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError


class Student(models.Model):
    _name = "student.student"
    _description = "This is student profile"

    # school_id = fields.Many2one(comodel_name="school.school", inverse_name="student_list", string="Select School",
    #                             index=True)

    # def delete_records(self):
    #     print(self)
    #     student_id = self.env["student.student"].browse(69).unlink()
    #     print(student_id)
    #     print(student_id.unlink())

    def unlink(self):
        print("unlink method called")
        print(self)
        rtn = super(Student, self).unlink()
        return rtn

    def delete_records(self):
        print(self)
        student_id = self.env["student.student"].browse([1, 2, 3, 4])
        for student in student_id:
            if not student.exists():
                raise UserError(f"Student does not exist {student}")
                print("Instance or Recordest is not available ", student)
            else:
                print("Instnce or Recordest is HERE", student)

    def duplicate_records(self):
        duplicate_record = self.copy({"joining_date_time": fields.Datetime.now()})

    @api.returns("self", lambda value: value.id)
    def copy(self, default=None):
        print(self)
        print(default)
        rtn = super(Student, self).copy(default=default)
        print(rtn)
        return rtn

    def unlink(self):
        print("unlink method called")
        print(self)
        rtn = super(Student, self).unlink()
        print(rtn)
        print("unlink method logic finish")
        return rtn

    hobby_list = fields.Many2many("hobby.hobby", "student_hobby_list_rel", "student_id", "hobby_id")

    joining_date_time = fields.Datetime("DateTime")

    joining_date = fields.Date("Date", default=fields.Date.today())

    school_data = fields.Json()

    @api.model
    def _get_vip_list(self):
        return [('a', '1'), ('b', '2'), ('c', '3')]

    roll_number = fields.Integer(string="Roll Number", default=200, index=True,
                                 help="Please enter student fees for current year")

    advanced_gender = fields.Selection("get_advanced_gender_list")

    vip_gender = fields.Selection(_get_vip_list, "VIP Gen")

    combobox = fields.Selection(selection=[("male", "Male"), ("female", "Female")], string="Combo Box")

    gender = fields.Selection([("male", "Male"), ("female", "Female"), ("other", "Other")], required=1)

    is_default_demo = fields.Boolean(default=False)
    is_paid = fields.Boolean("Paid?", default=False, help="This field is for this student paid or not the full fees!")
    name = fields.Char("Name")
    name1 = fields.Char("Name1")
    name2 = fields.Char("Name2")
    name3 = fields.Char("Name3")
    name4 = fields.Char("Name4", readonly=True)

    student_name = fields.Char(string="Student Name", required=True)
    address = fields.Text()

    address_html = fields.Html(string="Address HTML Field", required=1, copy=False,
                               default="<p>This is a default value from the backend</p>",
                               help="This field is used for the dynamic html code to render into the student profile")

    student_fees = fields.Float(digits="Student fees", default=0, index=True)
    discount_fees = fields.Float(digits="Discount fees", default=0, index=True)

    final_fees = fields.Float("Final Fees", compute="_compute_final_fees_cal")

    compute_address_html = fields.Html(string="Compute Address Field")

    @api.onchange("address_html")
    def _onchange_address_html(self):
        for record in self:
            record.compute_address_html = record.address_html

    @api.onchange("student_fees", "discount_fees")
    def _compute_final_fees_cal(self):
        for record in self:
            record.final_fees = record.student_fees - record.discount_fees

    def get_advanced_gender_list(self):
        return [('male', 'Male'), ('female', 'Female'), ('1', '1')]

    # def json_data_store(self):
    #     self.school_data = {"name": self.name, "fees": self.student_fees, "g":self.gender}


class Hobby(models.Model):
    _name = 'hobby.hobby'
    _description = 'This is hobby profile.'

    name = fields.Char(string='Name')
