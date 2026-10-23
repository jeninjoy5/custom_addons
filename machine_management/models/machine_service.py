
from odoo import models,fields,api
from odoo.exceptions import UserError


class MachineService(models.Model):
    _name = 'machine.service'
    _description = 'Machine Service'
    _rec_name = 'machine_name_id'
    _inherit = ['mail.thread']

    machine_name_id = fields.Many2one('machine.management',
                                      string="Machine Name",
                                      required=True)
    customer_id = fields.Many2one(comodel_name='res.partner',
                                  string='Customer',
                                  tracking=True)
    description = fields.Text(string='Description')
    internal_notes = fields.Html('Internal Notes')
    service_state = fields.Selection([('open', 'Open'),
                                       ('started', 'Started'),
                                      ('done', 'Done'),
                                      ('cancelled', 'Cancelled')],
                                      string="Status",
                                      default='open',
                                     tracking=True)
    company_id = fields.Many2one('res.company',
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    service_order_line_ids = fields.One2many(comodel_name='service.order.line',
                                     inverse_name='order_id',
                                     string="Order Lines", copy=True)
    user_ids = fields.Many2many('res.users',
                                string='Tech Person',
                                tracking=True)
    invoice_count = fields.Integer(string="Invoice")
    invoice_id = fields.Many2one(comodel_name='account.move')
    invoice_status = fields.Selection([('to_invoice', 'To Invoice'),
                                       ('invoiced', 'Invoiced'),
                                       ('invoice_posted', 'Invoice Posted'),
                                       ('paid', 'Paid'),],
                                      default='to_invoice',
                                      compute='_compute_invoice_status')
    # service_frequency = fields.Selection([('weekly', 'Weekly'),
    #                                       ('monthly', 'Monthly'),
    #                                       ('yearly', 'Yearly')])
    next_service_date = fields.Datetime(string='Next Service Date')
    serial_number = fields.Char(string='Serial Number',
                                related="machine_name_id.serial_number")
    active = fields.Boolean(default=True)
    service_date = fields.Date(string="Date")








    #
    # def _compute_allowed_parts_ids(self):
    #     parts = self.env['machine.management'].search(
    #         [('order_line_ids', '!=', False)])
    #     self.update({'allowed_parts_ids': [(fields.Command.set(parts.ids))]})
    #     print(parts)

    def action_service_start(self):
        """Changing the status of the service to started"""
        self.write({'service_state': 'started'})

    def action_service_close(self):
        """Changing the status of the service to done and sending email
        to customer"""
        self.write({'service_state': 'done'})
        template=self.env.ref('machine_management.email_template_service_close')
        template.send_mail(self.id,email_values=
        {'email_to':self.customer_id.email},force_send=True)

    def action_create_invoice(self):
        """Creating the invoice"""
        service_product=self.env['product.product'].search([
            ('name','=','Service Charge')])
        invoice_lines = []
        # self.write({'invoice_status': 'invoiced'})
        draft_invoices = self.env['account.move'].search([
            ('partner_id', '=', self.customer_id.id),
            ('state', 'in', 'posted')])
        lines=draft_invoices.mapped('invoice_line_ids')
        draft_invoices.write({'state': 'cancel'})
        for line in lines:
            invoice_lines.append((fields.Command.create({
                            'product_id' : line.product_id.id,
                            'quantity' : line.quantity,
                            'price_subtotal' : line.price_subtotal})))


        for service in self:
            for record in service.service_order_line_ids:
                invoice_lines.append((fields.Command.create({
                            'product_id' : record.parts_id.id,
                            'quantity' : record.parts_qty,
                            'price_subtotal' : record.price_total
                })))

            invoice_lines.append((fields.Command.create({
                    'product_id' : service_product.id
            })))
        invoice = self.env['account.move'].create([{
                'move_type': 'out_invoice',
                'partner_id': self.customer_id.id,
                'invoice_line_ids': invoice_lines,

        }])
        self.invoice_id=invoice.id
        self.invoice_count=self.invoice_count+1


        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "form",
            "res_id": invoice.id
        }


    def action_view_invoice(self):
        """To view the invoice"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "name": "Invoices",
            "view_mode": "list,form",
            "domain": [('id', '=', self.invoice_id.id)]
        }

    @api.depends('invoice_id.state','invoice_id.payment_state')
    def _compute_invoice_status(self):
        """Setting invoice status field based on invoice state for ribbon"""
        print("working")
        for record in self:
            if record.invoice_id.state == 'draft':
                record.write({'invoice_status': 'invoiced'})
            elif record.invoice_id.payment_state == 'paid':
                record.write({'invoice_status': 'paid'})
            elif record.invoice_id.state == 'posted':
                record.write({'invoice_status': 'invoice_posted'})
            else:
                record.write({'invoice_status': 'to_invoice'})

    def action_cancel_service(self):
        self.write({'service_state': 'cancelled'})


    def action_archive(self):
        if not self.env.user.has_group('machine_management.group_machine_manager'):
            raise UserError("You are not allowed to archive this service")
        else:
            return super().action_archive()










    # def _allowed_machine_ids(self):
    #     machines = self.env['machine.management'].search([
    #         ('state', '=', 'in_service')])
    #     self.update({'allowed_machine_ids':[(fields.Command.set(
    #         machines.ids))]})
    #     print(machines)

    # @api.model
    # def recurring_maintenance(self):
    #     services = self.env['machine.management'].search([('state', '=', 'in_service')])
    #     # print(serial_numbers)
    #     existing_services = self.search([('machine_name_id', '!=', False)])
    #     serial_numbers = existing_services.mapped('serial_number')
    #     print(serial_numbers)
    #     for record in services:
    #         print(record)
    #         # for rec in existing_services:
    #         if record.service_frequency == 'weekly':
    #             print('weekly')
    #             next_service_date = self.service_date + relativedelta(weeks=1)
    #             print(next_service_date)
    #         elif record.service_frequency == 'monthly':
    #             print('monthly')
    #             next_service_date = self.service_date + relativedelta(months=1)
    #         elif record.service_frequency == 'yearly':
    #             next_service_date = self.service_date + relativedelta(years=1)
    #
    #         if record.serial_number not in serial_numbers:
    #             self.create({
    #                 'machine_name_id': record.id,
    #                 'customer_id': record.customer_id.id,
    #                 'service_date': next_service_date,
    #             })
    #         else:
    #             self.update({
    #                 'service_date': next_service_date})









    # @api.depends('service_order_line_ids')
    # def _compute_invoice_count(self):
    #     for order in self:
    #         invoices = order.service_order_line_ids.invoice_lines.move_id.filtered(lambda r: r.move_type in ('out_invoice', 'out_refund'))
    #         order.invoice_count = len(invoices)
    #








    # def action_create_invoice(self):
    #     self.env['machine.service'].write("invoice_status")


    # @api.depends('order_id')
    # def _onchange_machine_name_id(self):
    #     parts = self.env['machine.order.line'].mapped('parts_id')
    #     print(parts)


