from odoo import models, fields,api

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"


    attachment_ids = fields.Many2many('ir.attachment',
                                      string="Attachments")


    @api.model
    def purchase_order_attachment(self):
        # res = super(ResConfigSettings, self).get_values()
        param = self.env['ir.config_parameter'].sudo()
        state = param.get_param('purchase_order_attachment.require_attachment')
        print(state)
        return state
