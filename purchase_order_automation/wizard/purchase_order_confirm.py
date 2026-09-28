from odoo import models,fields

class PurchaseOrderConfirm(models.TransientModel):
    _name = 'purchase.order.confirm'


    product_id = fields.Many2one('product.template',)
    quantity = fields.Float(string='Quantity')
    price = fields.Float(string='Price')




    def action_confirm_purchase_order(self):
        print(self.product_id.seller_ids.partner_id)
        # partner=self.env['product.supplierinfo'].search([(self.product_id.seller_ids.partner_id.id)],limit=1)
        # print(partner)
        order=self.env['purchase.order'].create({'partner_id': self.product_id.seller_ids.partner_id.id,
            'order_line': [(fields.Command.create({
                    'product_id':self.product_id.id,
                    'product_qty': self.quantity,
                    'price_unit': self.price}))]})
        order.button_confirm()
