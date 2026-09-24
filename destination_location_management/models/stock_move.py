from odoo import models, api,fields

class StockMove(models.Model):
    _inherit = 'stock.move'


    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id.weight > 20:
            location=self.env.ref('destination_location_management.location_type_name_data')
            print(location)
            print(self.picking_id.test.name)
            # self.location_dest_id=False
            self.picking_id.test=location.id
            # self.write({'picking_id.test' : location.id})
            print(self.picking_id.test.name)


        # print(self.picking_id.origin)
        # self.picking_id.origin="jjj"
        # # self.write({'picking_id.origin' : location.id})
        # print(self.picking_id.origin)