from odoo import models, fields,api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    # FIELDS

    product_brand = fields.Many2one(comodel_name="product.brand",
                                    string="Brand")
    product_master_type = fields.Selection([('single','Single'),
                                            ('branded','Branded'),],)
                                           # default="single")



    @api.onchange("product_master_type")
    def _onchange_product_master_type(self):
        if self.product_master_type == "branded":
            print("jnn")
            location=self.env.ref('product_fields.product_brand_data1')
            print(location)
            print(self.product_brand)
            self.product_brand = location
            print(self.product_brand)


