from odoo import models,fields

class PurchaseOrderConfirm(models.TransientModel):
    _name = 'purchase.order.confirm'


    product_id = fields.Many2one('product.template',)
    quantity = fields.Float(string='Quantity')
    price = fields.Float(string='Price')




    def action_confirm_purchase_order(self):
        vendor=self.product_id.seller_ids.partner_id[0]
        draft_purchase_order=self.env['purchase.order'].search([
            ('state','in','draft'),('partner_id','=',vendor.id)],limit=1)
        print(draft_purchase_order)
        if draft_purchase_order:
            draft_purchase_order.write({'order_line': [(fields.Command.create({
                    'product_id':self.product_id.id,
                    'product_qty': self.quantity,
                    'price_unit': self.price}))]})
            draft_purchase_order.button_confirm()
        else:
            purchase_order=self.env['purchase.order'].create({
                'partner_id': vendor.id,
                'order_line': [(fields.Command.create({
                        'product_id':self.product_id.id,
                        'product_qty': self.quantity,
                        'price_unit': self.price}))]})
            print(purchase_order)
            purchase_order.button_confirm()


