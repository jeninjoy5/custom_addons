from odoo import models,fields,api


class MachineServiceRequest(models.Model):
    _name = 'machine.service.request'

    name = fields.Char(String="Name",required=True)
    email = fields.Char(String="Email",required=True)
    phone = fields.Char(String="Phone",required=True)