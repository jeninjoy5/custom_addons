from odoo import http
from odoo.http import request

class MachineSnippetController(http.Controller):
    @http.route('/get_machines',auth="public", type='jsonrpc',
                website=True)
    def get_machine(self):
        print("working")
        machines=request.env['machine.management'].sudo().search([])
        print(machines)
        values={'machines':machines}
        return values
