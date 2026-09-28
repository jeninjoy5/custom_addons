from odoo import models, fields,api

class ProductTemplate(models.Model):
    _inherit = "product.template"




    def action_open_purchase_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Order',
            'res_model': 'purchase.order.confirm',
            'view_mode': 'form',
            'target': 'new',
            'context':{'default_product_id': self.id},
        }

