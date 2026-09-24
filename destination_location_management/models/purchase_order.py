from odoo import models,fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    #
    # def button_confirm(self):
    #     print("working")
    #     super().button_confirm()
    #     lines = self.order_line.filtered(lambda move:
    #                                    move.product_id.weight > 20)
    #     print(lines)
    #     if lines:
    #         location = self.env.ref(
    #             'destination_location_management.location_type_name_data')
    #         print(location)
    #         print(self.picking_ids.location_dest_id)
    #         # self.picking_ids.location_dest_id=location
    #         self.picking_ids.write({'location_dest_id': location})
    #         # print(self.location_dest_id.name)
    #     else:
    #         location = self.env.ref('stock.stock_location_stock')
    #         self.picking_ids.write({'location_dest_id': location})


