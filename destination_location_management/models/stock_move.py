from odoo import models, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model_create_multi
    def create(self, vals_list):
        """Changing destination location according to the condition whenever
         a record is created."""
        print("working...")
        moves = super().create(vals_list)
        print(moves)
        for move in moves:
            if move.product_id.weight>20:
                print("if working...")
                location = move.env.ref(
                        'destination_location_management.location_type_name_data')
                print(location)
                print(move.picking_id.location_dest_id.name)
                move.picking_id.write({'location_dest_id': location})
                print(move.picking_id.location_dest_id.name)
        return moves






