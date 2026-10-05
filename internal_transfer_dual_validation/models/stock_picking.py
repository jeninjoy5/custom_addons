from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    state = fields.Selection(selection_add=[('to_approve','To Approve')])


    def button_validate(self):
        if not self.env.user.has_group('stock.group_stock_manager'):
            self.write({'state': 'to_approve'})
        else:
            return super().button_validate()



    def action_approve_transfer(self):
        return self.button_validate()

