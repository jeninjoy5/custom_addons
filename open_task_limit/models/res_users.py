from odoo import models,fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    max_tasks = fields.Integer(string="Maximum number of tasks")