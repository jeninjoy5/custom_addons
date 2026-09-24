from odoo import models, fields,api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    # FIELDS

    is_prime_customer = fields.Boolean(string="Is Prime Customer",
                                       compute="_compute_is_prime_customer")

    @api.depends("partner_id")
    def _compute_is_prime_customer(self):
        """For computing the is_prime_customer field for the sale order"""
        for order in self:
            if order.partner_id.is_prime_customer == True:
                order.is_prime_customer = True
            else:
                order.is_prime_customer = False
