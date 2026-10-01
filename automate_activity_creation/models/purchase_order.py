from odoo import models, api,fields


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"


    @api.model
    def action_create_activity(self):
        """Checks whether the delivery date is less than current date and if it
        is then an activity will be created to the vendor and a mail also be
        sent to the user"""
        today = fields.Datetime.today()
        orders = self.search([('state', '!=', 'cancel'),('date_planned','<', today)])
        print(orders)
        for order in orders:
            print("working")
            print(self.env['ir.model']._get_id('res.partner'))
            self.env['mail.activity'].create({
                        'activity_type_id': self.env.ref(
                            'mail.mail_activity_data_meeting').id,
                        'res_model_id': self.env['ir.model']._get_id('res.partner'),
                        'res_id': order.partner_id.id
                        })
            template = self.env.ref(
                        'automate_activity_creation.email_template_notify_user')
            template.send_mail(self.id, email_values=
                    {'email_to': self.env.user.email}, force_send=True)

