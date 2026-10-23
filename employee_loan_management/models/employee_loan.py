from odoo import models,fields,api
from odoo.exceptions import ValidationError


class EmployeeLoan(models.Model):
    _name = 'employee.loan'
    _description = 'Employee Loan'
    _inherit = ['mail.thread']



    name = fields.Char(string="Reference",required=True, copy=False,
                       readonly=True,default=lambda self: 'New')
    employee_id = fields.Many2one(comodel_name='hr.employee',string="Employee",tracking=True,required=True)
    loan_amount = fields.Float(string="Loan Amount",tracking=True)
    installment_count = fields.Integer(string="Installment Count")
    start_date = fields.Date(string="Start Date")
    state = fields.Selection([('draft','Draft'),('approved','Approved'),('ongoing','Ongoing'),('paid','Paid')],string="State",default='draft')
    loan_line_ids = fields.One2many(comodel_name='employee.loan.line',inverse_name='loan_id')
    installment_amount = fields.Float(string="Installment Amount")
    total_payable = fields.Float(string="Total Payable",compute='_compute_total_payable')
    count_smart_button = fields.Integer(compute='_compute_count_smart_button')
    paid_amount=fields.Float(string="Paid Amount",compute='_compute_paid_amount')
    balance_amount = fields.Float(string="Balance Amount",compute='_compute_balance_amount')



    @api.model_create_multi
    def create(self, vals_l):
        """Creating sequence number"""
        for vals in vals_l:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'employee.loan') or 'New'
        return super(EmployeeLoan, self).create(vals_l)

    @api.onchange('loan_amount','installment_count')
    def onchange_loan_amount(self):
        if self.installment_count != 0:
            self.installment_amount = self.loan_amount / self.installment_count

    @api.depends('loan_amount')
    def _compute_total_payable(self):
        for loan in self:
            loan.total_payable = loan.loan_amount

    def action_employee_loan_form_view(self):
        if self.loan_amount > 0 and self.installment_count>0:
            self.write({'state':'approved'})
        else:
            raise ValidationError("Loan amount and installment count should be greater than 0")

    def _compute_count_smart_button(self):
        if self.loan_line_ids:
            self.count_smart_button=len(self.loan_line_ids)
        else:
            self.count_smart_button=0



    def action_installment(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "employee.loan.line",
            "name": "Installments",
            "view_mode": "list",
            "domain": [('loan_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def action_installment_form_view(self):
        for i in range(self.installment_count):
            self.env['employee.loan.line'].create({
            'loan_id': self.id,
            'amount': self.installment_amount
        })
        self.write({'state':'ongoing'})

    def action_pay_form_view(self):
        for line in self.loan_line_ids:
            if line.is_paid==False:
                line.is_paid=True
                break
        if self.balance_amount==0:
            self.write({'state':'paid'})

    def _compute_paid_amount(self):
        self.paid_amount=0
        for line in self.loan_line_ids:
            if line.is_paid==True:
                self.paid_amount=self.paid_amount+line.amount


    def _compute_balance_amount(self):
        self.balance_amount=self.total_payable
        for line in self.loan_line_ids:
            if line.is_paid==True:
                self.balance_amount=self.balance_amount-line.amount








