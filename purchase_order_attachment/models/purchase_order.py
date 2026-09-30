from odoo import models
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"




    def button_confirm(self):
        """Check whether one attachment is provided before confirming purchase
        order and also checks the attachment is PDF,image files or not"""
        state = (self.env['ir.config_parameter'].get_param
                 ('purchase_order_attachment.require_attachment'))
        attachments = self.env['ir.attachment'].search([
            ('res_model', '=', 'purchase.order'),('res_id','=',self.id)])
        for attachment in attachments:
            if (attachment.mimetype != 'application/pdf' and
                    not attachment.mimetype.startswith('image')):
                raise ValidationError("Only PDF and image files are allowed")
        if state and not attachments:
            raise ValidationError("Require attachment to confirm purchase order")
        return super().button_confirm()



