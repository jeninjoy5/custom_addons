from typing import Self

from odoo import models, api
from odoo.orm.types import ValuesType


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # @api.onchange('move_ids')
    # def _onchange_product_id(self):
    #     """Changing the destination location if the product weight is greater
    #     than 20kg"""
    #     print("gggggg", self)
    #     lines = self.move_ids.filtered(lambda move:
    #                                       move.product_id.weight > 20)
    #     if lines:
    #         location = self.env.ref(
    #                 'destination_location_management.location_type_name_data')
    #         print(location)
    #         print(self.location_dest_id.name)
    #         self.write({'location_dest_id' : location.id})
    #         print(self.location_dest_id.name)
    #     else:
    #         location = self.env.ref('stock.stock_location_stock')
    #         self.write({'location_dest_id' : location})


    # def destination_location_action(self):
    #     print("working...")
    #     lines = self.move_ids.filtered(lambda move:
    #                                    move.product_id.weight > 20)
    #     if lines:
    #         print("if working...")
    #         location = self.env.ref(
    #             'destination_location_management.location_type_name_data')
    #         print(location)
    #         print(self.location_dest_id.name)
    #         self.write({'location_dest_id': location})
    #         print(self.location_dest_id.name)
    #     else:
    #         location = self.env.ref('stock.stock_location_stock')
    #         self.write({'location_dest_id': location})



    @api.model_create_multi
    def create(self, vals_list):
        print("working...")
        pickings=super().create(vals_list)
        # lines = self.move_ids.filtered(lambda move:
        #                                move.product_id.weight > 20)
        # print(lines)
        # if lines:
        for pick in self:
            if pick.product_id.weight > 20:
                print("if working...")
                location = self.env.ref(
                    'destination_location_management.location_type_name_data')
                print(location)
                print(self.location_dest_id.name)
                self.write({'location_dest_id': location})
                print(self.location_dest_id.name)
            else:
                location = self.env.ref('stock.stock_location_stock')
                self.write({'location_dest_id': location})
        return pickings





