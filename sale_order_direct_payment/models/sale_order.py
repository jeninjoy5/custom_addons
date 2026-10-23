from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_count = fields.Integer(compute='_compute_payment_count')


    def action_direct_payment(self):
        """Direct payment from sale order and link invoice and its payment"""
        invoice=self.invoice_ids.filtered(lambda r:
                                           r.move_type == 'out_invoice'
                                           and r.state == 'posted')
        if not invoice:
            invoice=self._create_invoices()
            invoice.action_post()
            print(invoice)
            journal=self.env.ref('account.1_bank')
            print(journal)
            self.env['account.payment.register'].create({
            'amount': invoice.amount_total,
            'journal_id': journal.id,
            'payment_date': fields.Date.today(),
            'line_ids': invoice.line_ids.filtered(lambda line: line.display_type == 'payment_term'),}).action_create_payments()

    def action_open_payment(self):
        """Smart button in sale order to see payments"""
        invoice = self.invoice_ids.filtered(lambda r:
                                            r.move_type == 'out_invoice')
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.payment",
            "view_mode": "list,form",
            "domain": [('invoice_ids', '=', invoice.id)],
            'context': "{'create': False}"
        }

    @api.depends('invoice_ids')
    def _compute_payment_count(self):
        """Payment count calculation"""
        invoice = self.invoice_ids.filtered(lambda r:
                                            r.move_type == 'out_invoice')
        payments=self.env['account.payment'].search([('invoice_ids', '=', invoice.id)])
        self.payment_count = len(payments)
