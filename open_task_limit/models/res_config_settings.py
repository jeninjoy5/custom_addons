from odoo import fields, models, api

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    is_limit_task = fields.Boolean(string="Limit Task for Users",
                                   config_parameter="open_task_limit.limit_task")
    max_tasks = fields.Integer(string="Maximum number of tasks",
                               config_parameter="open_task_limit.max_tasks")



