from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    test=fields.Many2one(comodel_name="stock.location",string='Test Picking')

    # @api.onchange('picking_type_id')
    # def _onchange_product_id(self):
    #     print(self.origin)
    #     self.origin = "jjj"
    #     print(self.origin)