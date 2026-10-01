from odoo import models
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'


    def action_post(self):
        if self.move_type == "in_invoice":
            vendor_bills=self.partner_id.invoice_ids.filtered(
                lambda r: r.move_type == "in_invoice")
            duplicate = vendor_bills.filtered(lambda bill:
                                        bill.ref == self.ref and
                                        bill.amount_total == self.amount_total)
            if duplicate:
                raise ValidationError("Duplicates not allowed")
            return super().action_post()