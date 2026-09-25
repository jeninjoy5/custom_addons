from odoo import models, fields,api


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    is_product = fields.Boolean(string="Is Product")


    @api.onchange('is_product')
    def onchange_is_product(self):
        if self.is_product:
            print("working")
            print(self.partner_id.product_ids)
            # for product in self.partner_id.product_ids:
            products=self.partner_id.mapped('product_ids')
            print(products)
            for product in products:
            #     values={
            #     'order_line':[
            #         fields.Command.create({
            #         'product_id': self.product.id
            #     })
            # ]}
                self.update({'order_line':[(fields.Command.link(product.id))]})
                print(product.name)
        # else:
        #     self.update({'order_line': [(fields.Command.clear())]})

