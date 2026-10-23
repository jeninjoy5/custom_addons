from odoo import http
from odoo.http import request
class WebFormController(http.Controller):
   @http.route('/webform', auth='public', website=True)
   def display_web_form(self, **kwargs):
       print("working1")
       machines = self.env['machine.management'].search([])
       customers = self.env['res.partner'].search([])
       print(machines)
       return request.render('machine_management.web_form_template',{'machines':machines,'customers':customers})
   @http.route('/webform/submit', type='http', auth='public', website=True, methods=['POST'],csrf=True)
   def handle_web_form_submission(self, **post):
       print("working2")
       request.env['machine.service'].sudo().create({
           'machine_name_id': post.get('machine'),
           'customer_id': post.get('customer'),
           'service_date':post.get('date'),
           'description':post.get('description')
       })
       return request.redirect('/contactus-thank-you')

   @http.route('/webform_customer', auth='public', website=True)
   def display_web_form_customer(self, **kwargs):
       return request.render('machine_management.web_form_customer')

   @http.route('/webform/customer', type='http', auth='public', website=True, methods=['POST'],csrf=True)
   def handle_customer(self, **post):
       request.env['res.partner'].sudo().create({
           'name':post.get('name')
       })
       return request.redirect('/customer_success')

   @http.route('/customer_success', auth='public', website=True)
   def display_customer_success(self, **kwargs):
       return request.render('machine_management.web_form_create_success')


