from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # FIELDS

    is_prime_customer = fields.Boolean(string="Is Prime Customer")
