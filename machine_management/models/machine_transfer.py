from odoo import models,fields,api



class MachineTransfer(models.Model):
    _name = 'machine.transfer'
    _description = 'Transfer'
    _rec_name = 'machine_name_id'
    _inherit = ['mail.thread']


    # FIELDS

    machine_name_id = fields.Many2one('machine.management',
                           string="Machine Name",
                           required=True,
                           domain="[('id','in',allowed_machine_ids)]")
    serial_number = fields.Char(string='Serial Number',
                                related="machine_name_id.serial_number")
    transfer_date = fields.Date(string="Transfer Date")
    transfer_type = fields.Selection([('install','Install'),
                                      ('remove','Remove')],
                                     string="Transfer Type")
    customer_id = fields.Many2one('res.partner',
                                  string="Customer",
                                  tracking=True)
    company_id = fields.Many2one('res.company',
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    internal_notes = fields.Html('Internal Notes')
    allowed_machine_ids=fields.Many2many('machine.management')
    transfer_state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done')],
                             string="Status",
                             default='draft')
    active = fields.Boolean(default=True)

    # sale_order_id = fields.Many2one(comodel_name="sale.order",string="Sale Order")
    # dob = fields.Datetime(string="Date of Birth")
    # age = fields.Integer(string="Age",compute="_compute_age")


    # def action_sale_order_view(self):
    #     print(self.sale_order_id.partner_id.name)
    #
    #     sale_count=self.env['sale.order'].search_count([
    #         ('partner_id','=',self.sale_order_id.partner_id.id)])
    #     print(sale_count)
    #
    #     print(self.sale_order_id.amount_total)
    #
    #     print(self.sale_order_id.partner_id.sale_order_ids)
    #
    #     print(self.sale_order_id.partner_id.sale_order_ids.mapped('amount_total'))
    #
    #     min_sale = min(self.sale_order_id.partner_id.sale_order_ids.mapped('amount_total'))
    #
    #     max_sale = max(self.sale_order_id.partner_id.sale_order_ids.mapped('amount_total'))
    #
    #     print(min_sale)
    #     print(max_sale)
    #
    #
    #
    #     invoices=self.env['account.move'].search([('partner_id','=',self.sale_order_id.partner_id.id)])
    #     amount=invoices.mapped('amount_total')
    #     total_amount=sum(amount)
    #     print(total_amount)
    #
    #     highest_amnt = 0
    #     for rec in invoices:
    #         if rec.amount_total>highest_amnt:
    #             highest_amnt=rec.amount_total
    #             invoice_id=rec.ref
    #     print(highest_amnt)
    #     print(invoice_id)
    #
    #     lowest_amnt = float('inf')
    #     for rec in invoices:
    #         if rec.amount_total<lowest_amnt:
    #             lowest_amnt=rec.amount_total
    #             invoice_id=rec.ref
    #     print(lowest_amnt)
    #     print(invoice_id)
    #
    #     sale_orders_prod=self.env['sale.order'].search([('partner_id','=',self.sale_order_id.partner_id.id)])
    #     sale_order_lines=sale_orders_prod.mapped('order_line')
    #     purchased_products=sale_order_lines.mapped('product_id.name')
    #     print(purchased_products)
    #
    #     highest_qty=0
    #     for rec in sale_order_lines:
    #         if rec.product_uom_qty>highest_qty:
    #             prod=rec.product_id.name
    #     print(prod)
    #
    #     highest_amnt_prod=0
    #     for rec in sale_order_lines:
    #         if rec.price_subtotal>highest_amnt_prod:
    #             product=rec.product_id.name
    #     print(product)



    @api.depends('dob')
    def _compute_age(self):
        if self.dob:
            today = fields.Date.today()
            date = self.dob
            self.age = today.year - date.year - (
                        (today.month, today.day) < (date.month,
                                                    date.day))

    def action_machine_form_view(self):
        '''Adding customer and changing state'''
        self.machine_name_id.write({'state':"in_service"})
        self.machine_name_id.write({'customer_id':self.customer_id})
        self.write({'transfer_state':'done'})
        # return {
        #     "type": "ir.actions.act_window",
        #     "res_model": "machine.management",
        #     "view_mode": "form",
        #     "res_id": self.machine_name_id.id
        # }


    @api.onchange('transfer_type')
    def _onchange_transfer_type(self):
        '''Showing active and in service machines according to the transfer
        type selected'''
        if self.transfer_type == "install":
            machines=self.env['machine.management'].search([
                ('state', '=', 'active')])
            print(machines)
            # self.update({'allowed_machine_ids':[(fields.Command.set(
            #     machines.ids))]})
            self.update({'allowed_machine_ids':[(fields.Command.clear())]})
            for rec in machines:
                self.update({'allowed_machine_ids': [(fields.Command.link(
                    rec.id))]})
            if self.machine_name_id and self.machine_name_id.state!='active':
                self.write({'machine_name_id': False})
        elif self.transfer_type == "remove":
            machines=self.env['machine.management'].search([
                ('state', '=', 'in_service')])
            print(machines)
            # self.update({'allowed_machine_ids':[(fields.Command.set(
            #     machines.ids))]})
            self.update({'allowed_machine_ids':[(fields.Command.clear())]})
            for rec in machines:
                self.update({'allowed_machine_ids': [(fields.Command.link(
                    rec.id))]})
            if (self.machine_name_id and self.machine_name_id.state
                    !='in_service'):
                self.write({'machine_name_id': False})
        else:
            self.update({'allowed_machine_ids':[(fields.Command.clear())]})
















    # @api.model
    # def name_search(self, name='', domain=None, operator='ilike', limit=100):
    #     domain = domain or []
    #     if name:
    #         records = self.search(
    #             ['|',
    #              ('purchase_value', operator, name)] + domain,
    #             limit=limit
    #         )
    #         return records.name_get()
    #     return super().name_search(
    #         name=name, domain=domain, operator=operator, limit=limit
    #     )




