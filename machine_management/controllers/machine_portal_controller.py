from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

class CustomPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'portal_machine' in counters:
            values['portal_machine'] = request.env[
                'machine.management'].sudo().search_count([])
        return values


    @http.route('/machine',type='http', auth="public", website=True)
    def portal_machine(self, **kwargs):
        print("list view")
        machines=request.env['machine.management'].sudo().search([('customer_id','=',self.env.user.partner_id.id)])
        return request.render('machine_management.portal_my_home_machine_views', {'machines': machines,
                                                                                  'page_name':'machine_details_tree'})

    @http.route(['/machine/<int:machine_id>'],type='http', auth="public", website=True)
    def portal_my_machine(self,machine_id, **kwargs):
        print("yes")
        print(machine_id)
        machine=request.env['machine.management'].sudo().search([('id','=',machine_id)])
        return request.render('machine_management.portal_my_machine', {'machine': machine,
                                                                       'page_name':'machine_details_page'})