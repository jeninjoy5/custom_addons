from odoo import models, fields,api


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    is_partner_product = fields.Boolean(string="Is Product")
    is_empty = fields.Boolean(string="Is Empty",compute="_compute_is_empty")



    @api.depends('partner_id')
    def _compute_is_empty(self):
        products = self.partner_id.mapped('product_ids')
        if products:
            self.is_empty = True
        else:
            self.is_empty = False


    @api.onchange('is_partner_product','partner_id')
    def onchange_is_partner_product(self):
        self.update({'order_line': [(fields.Command.clear())]})
        if self.is_partner_product:
            print("working")
            print(self.customer_related.id)
            products=self.partner_id.mapped('product_ids')
            print(products)
            for product in products:
                self.update({'order_line':[(fields.Command.create({
                    'product_id':product.id}))]})
                print(product.name)
        else:
            self.update({'order_line': [(fields.Command.clear())]})

