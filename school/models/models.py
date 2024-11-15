# -*- coding: utf-8 -*-

from odoo import api, fields, models


class School(models.Model):
    _name = 'school.school'
    _description = 'This is school profile.'

    name = fields.Char(string='Name')
    location = fields.Char(string='Location')
    # student_list = fields.One2many("student.student", "school_id", string='Student List')

    invoice_id = fields.Many2one("account.move")
    invoice_user_id = fields.Many2one("res.users", related="invoice_id.invoice_user_id")
    # invoice_date = fields.Date(related="invoice_id.invoice_date")

    name2 = fields.Char(string='NameTest')

    ref_field_id = fields.Reference(
        [('school.school', 'School'),
         ('student.student', 'Studnet'),
         ('hobby.hobby', 'Hobby')])

    binary_field = fields.Binary("Binary Field")
    binary_field_name = fields.Char("Binary Field Name")

    school_image = fields.Image("School Image", max_width=128, max_height=128)

    currency_id = fields.Many2one("res.currency", "Currency")
    amount = fields.Monetary("Amount")

    @api.model_create_multi
    def create(self, vals):
        print(self)
        print(vals)
        rtn = super(School, self).create(vals)
        print(rtn)
        return rtn

    def print_table(self, records):
        # Print headers
        print(f"{'ID':<10}{'Name':<20}{'Amount':<15}")
        print("=" * 45)  # Just a separator line

        # Print each record in the table
        for record in records:
            print(f"{record.id:<10}{record.name:<20}{record.amount:<15}")

    def custom_method(self):
        print("Custom method called")
        print(self)

        print("=== READ ===")

        school_group_by_school = self.env['school.school'].read_group([],["name"], ["name"])
        for school in school_group_by_school:
            print(school)

        # print(self.read())
        #
        # self.write({"name": "Write updated", "amount": 40})
        # pass
        # records = self.search([("amount", ">", 0)])
        # self.print_table(records)

        # total_records = self.env['school.school'].search_count([], limit=10)
        # print(total_records)

    @api.model
    def write_method(self, vals):
        print("Write method called")
        print(self)
        print(vals)
        rtn = super(School, self).write(vals)
        print(rtn)
        return rtn
