from odoo import models,api
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = 'project.task'


    @api.model_create_multi
    def create(self, vals_list):
        task=super().create(vals_list)
        # print(vals_list)
        for user in task.user_ids:
            count=self.search_count([('user_ids','in',user.id),
                                    ('personal_stage_type_id','!=','Done'),
                                    ('personal_stage_type_id','!=','Cancelled')])
            # print(user)
            user_max_task=user.max_tasks
            state = (self.env['ir.config_parameter'].get_param
                     ('open_task_limit.limit_task'))
            if state:
                settings_max_task = (self.env['ir.config_parameter'].get_param
                                     ('open_task_limit.max_tasks'))
                # print(settings_max_task)
            if user_max_task:
                max_task=user_max_task
            elif settings_max_task:
                max_task=settings_max_task
            if count > int(max_task):
                raise ValidationError(
                    "Maximum number of tasks exceeded for this user")
        return task


    def write(self, vals):
        task = super().write(vals)
        # print(vals)
        # print(task)
        # print(self)
        if 'user_ids' in vals:
            for user in self.user_ids:
                count = self.search_count([('user_ids', 'in', user.id),
                                               ('personal_stage_type_id', '!=',
                                                'Done'),
                                               ('personal_stage_type_id', '!=',
                                                'Cancelled')])
                user_max_task = user.max_tasks
                state = (self.env['ir.config_parameter'].get_param
                         ('open_task_limit.limit_task'))
                if state:
                    settings_max_task = (self.env['ir.config_parameter'].get_param
                                     ('open_task_limit.max_tasks'))
                if user_max_task:
                    max_task = user_max_task
                elif settings_max_task:
                    max_task = settings_max_task
                if count > int(max_task):
                    raise ValidationError(
                        "Maximum number of tasks exceeded for this user")
        return task

