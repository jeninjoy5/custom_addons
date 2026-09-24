from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = "sale.order.line"


    # FIELDS

    product_brand = fields.Many2one(comodel_name="product.brand",
                                    string="Brand",
                                    related="product_template_id.product_brand")
