from odoo import fields, models, api

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    is_require_attachment = fields.Boolean(string="Require Attachment on "
                                                  "Purchase Order Confirmation",
                                           config_parameter="purchase_order"
                                                            "_attachment.require"
                                                            "_attachment")



