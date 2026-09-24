from odoo import fields,models

class TestModel(models.Model):
    _name='test.model'
    _description='Test Model for Real Estate'

    name=fields.Char(string="Name",required=True)
    description=fields.Text(string="Description")
    date_availability=fields.Date(string="Date Availability")
    selling_price=fields.Float(string="Selling Price",required=True)
    living_area=fields.Integer(string="Living Area")
    garden=fields.Boolean(string="Garden")
    garden_orientation=fields.Selection([('north','North'),('south','South'),('east','East'),('west','West')],string="Garden Orientation")