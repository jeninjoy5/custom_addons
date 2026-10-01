from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    state = fields.Selection(selection_add=[('to approve','To Approve')])


    def button_validate(self):
        self.write({'state': 'to approve'})
    #
    #
    # def action_approve_transfer(self):
    #     super().butt

