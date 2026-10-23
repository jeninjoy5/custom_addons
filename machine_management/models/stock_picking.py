from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'


    total_price = fields.Float(string="Total Price",
                               compute='_compute_total_price')



    @api.depends('move_ids.product_id')
    def _compute_total_price(self):
        for pick in self:
            product_list=[]
            pick.total_price=0
            for line in pick.move_ids:
                # print(line)
                if line.product_id.id not in product_list:
                    pick.total_price += line.product_id.standard_price
                    product_list.append(line.product_id.id)
                    # print(product_list)




    def action_check_total_price(self):
        if (self.total_price == self.move_ids.product_id.
                property_account_income_id.current_balance):
            print("working")
            return {
                    'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'type': 'success',
                            'message': "Both are matching",
                        }
                    }
        else:
            return {
                    'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'type': 'danger',
                            'message': "Both are not matching",
                        }
                    }