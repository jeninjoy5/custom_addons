from odoo import models,fields,api



class EmployeeLoanLine(models.Model):
    _name = 'employee.loan.line'



    loan_id = fields.Many2one('employee.loan',string="Loan")
    date = fields.Date(string="Date")
    amount = fields.Float(string="Amount")
    is_paid = fields.Boolean(string="Is Paid")