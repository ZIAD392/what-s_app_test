# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CustomPayslipModel(models.Model):
    _inherit = 'hr.payslip'

    bank = fields.Char(
        string="Bank",
        compute="_get_bank_acc_information"
    )
    account_number = fields.Char(
        string="Account Number",
        compute="_get_bank_acc_information"
    )
    other_earnings = fields.Float(
        string="Earnings",
        default=0.0,
        compute="_get_other_earnings",
    )
    deductions = fields.Float(
        string="Deductions",
        default=0.0,
        compute="_get_deductions",
    )
    net_salary = fields.Float(
        string="Net Salary",
        default=0.0,
        compute="_get_net_salary",
    )

    @api.depends('employee_id')
    def _get_bank_acc_information(self):
        for record in self:
            bank_info = record.employee_id.bank_account_id
            record.bank = bank_info.bank_id.name
            record.account_number = bank_info.acc_number

    @api.depends('employee_id', 'line_ids')
    def _get_other_earnings(self):
        value = 0.0
        for line in self.line_ids:
            if line.category_id.name == "Allowance" and line.name != "Housing Allowance":
                value += float(line.amount)
        self.other_earnings = value

    @api.depends('employee_id', 'line_ids')
    def _get_deductions(self):
        value = 0.0
        for line in self.line_ids:
            if line.category_id.name == "Deduction":
                value += float(line.amount)
        self.deductions = value

    @api.depends('employee_id', 'line_ids')
    def _get_net_salary(self):
        value = 0.0
        for line in self.line_ids:
            if line.category_id.name == "Net":
                value += float(line.amount)
        self.net_salary = value

