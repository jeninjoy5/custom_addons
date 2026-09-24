from odoo import models,fields


class ProductBrand(models.Model):
    _name = "product.brand"

    # FIELDS

    name = fields.Char(string="Name")