from odoo import models, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id.weight > 20:
            location=self.env.ref('product_fields.location_name_data')
            print(location)
            print(self.location_dest_id.name)
            # self.location_dest_id=False
            self.write({'location_dest_id' : location.id})
            print(self.location_dest_id.name)