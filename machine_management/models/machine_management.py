from odoo import models,fields,api
from odoo.exceptions import ValidationError, UserError



class MachineManagement(models.Model):
    _name = 'machine.management'
    _description = 'Machine'
    _inherit = ['mail.thread']
    _rec_name = 'machine_name'

    # FIELDS

    name = fields.Char(string='Reference',
                       required=True, copy=False,
                       readonly=True,
                       default=lambda self: 'New')
    machine_name = fields.Char(string='Name',
                               required = True,
                               help="Name of the Machine")
    date_of_purchase = fields.Datetime(string='Date of purchase',
                                 help="Date of purchase")
    company_id = fields.Many2one('res.company',
                                 store=True,
                                 copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency',
                                  string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self:
                                  self.env.user.company_id.currency_id.id)
    purchase_value = fields.Monetary(string='Purchase Value',
                                     tracking=True,
                                     help="Purchase Value")
    customer_id = fields.Many2one(comodel_name='res.partner',
                                  string='Customer',
                                  tracking=True,
                                  help="Name of the Customer")
    serial_number = fields.Char('Serial Number',
                                help="Unique Serial Number for the Machine",
                                required=True)
    machine_type_id = fields.Many2one(comodel_name='machine.type',
                                    string='Machine Type',
                                    help="Type of the Machine")
    state = fields.Selection([('active', 'Active'),
                              ('in_service', 'In Service')],
                             string="Status",
                             default='active')
    image = fields.Binary(string='Image')
    is_warranty = fields.Boolean(string='Is Warranty',
                                 default=False,
                                 tracking=True,
                                 help="Is the Machine has Warranty or not")
    machine_tag_ids=fields.Many2many(comodel_name='machine.tag',
                                   string='Tags')
    description = fields.Text(string='Description')
    instructions = fields.Html(string='Instructions')
    machine_transfer_count = fields.Integer(string='Transfers',
                                    compute='compute_machine_transfer_count')
    order_line_ids = fields.One2many(comodel_name='machine.order.line',
                                     inverse_name='order_id',
                                     string="Order Lines",copy=True)
    machine_age = fields.Integer(string='Machine Age',
                                 compute='_compute_machine_age')
    machine_service_count = fields.Integer(string='Services',
                                    compute='_compute_machine_service_count')
    active = fields.Boolean(default=True)

    sale_ids = fields.Many2many('sale.order',string='Sales Orders')
    purchase_ids = fields.Many2many(comodel_name='purchase.order',
                                    string='Purchase Orders')
    combine_ids = fields.Many2many(comodel_name='product.product',
                                   string='Combine Orders',
                                   compute='_compute_combine_ids')
    service_frequency = fields.Selection([('weekly', 'Weekly'),
                                          ('monthly', 'Monthly'),
                                          ('yearly', 'Yearly')])
    service_date = fields.Datetime(string='Service Date',
                                   tracking=True)
    service_ids = fields.One2many('machine.service',
                                  inverse_name='machine_name_id')
    transfer_ids = fields.One2many('machine.transfer',
                                   inverse_name='machine_name_id')




    @api.depends('sale_ids', 'purchase_ids')
    def _compute_combine_ids(self):
        for rec in self:
            if rec.sale_ids and rec.purchase_ids:
                sale_prod_id=rec.sale_ids.order_line.product_id
                purchase_prod_id=rec.purchase_ids.order_line.product_id
                print(sale_prod_id)
                print(purchase_prod_id)
                for sale in sale_prod_id:
                    if sale in purchase_prod_id:
                        print(sale)
                        self.update(
                            {'combine_ids': [(fields.Command.link(sale.id))]})
                    elif sale not in purchase_prod_id:
                        self.update(
                            {'combine_ids': [(fields.Command.unlink(sale.id))]})
                    else:
                        self.write({'combine_ids' : False})
            else:
                self.update({'combine_ids': [(fields.Command.clear())]})
                    # prod=rec.search([(sale,'in',purchase_prod_id)])

                # for sale in sale_prod_id:
                # if sale in purchase_prod_id:
                #     prod=sale
                #     print(prod)
                #     self.update({'combine_ids': [(fields.Command.link(prod.id))]})
                # else:
                #     self.write({'combine_ids' : False})
                #     for purchase in purchase_prod_id:
                #         if sale==purchase:
                #             prod=sale
                #             self.update({'combine_ids':[(fields.Command.set(prod.id))]})

                    # if sale_prod_id == purchase_prod_id:
                    #     prod=sale_prod_id
                    #     self.update({'combine_ids':[(fields.Command.set(prod.ids))]})

                    # self.update({'combine_ids':[(fields.Command.set(purchase_prod_id.ids))]})

                # purchase_prod_id=r.purchase_ids.order_line.product_id
                # print(sale_prod_id)
                    # print(purchase_prod_id)
                    # if sale_prod_id == purchase_prod_id:
                    #     prod=sale_prod_id
                    #     self.update({'combine_ids':[(fields.Command.set(prod.ids))]})


    @api.model_create_multi
    def create(self, vals_l):
        """Creating sequence number"""
        for vals in vals_l:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'machine.management') or 'New'
        return super(MachineManagement, self).create(vals_l)


    @api.constrains('purchase_value')
    def _check_purchase_value(self):
        """Validating purchase value"""
        for rec in self:
            if rec.purchase_value<=0:
                raise ValidationError("Purchase Value must be greater than 0")


    @api.constrains('serial_number')
    def _check_serial_number(self):
        """Checking serial number whether unique or not"""
        for rec in self:
            domain = [('serial_number', '=', rec.serial_number)]
            count = rec.search_count(domain)
        if count > 1:
            raise ValidationError(("The Serial Number should be unique"))


    def action_view_machine_transfer(self):
        """Smart button for transfer history"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "machine.transfer",
            "name": "Machine Transfers",
            "view_mode": "list,form",
            "domain": [('machine_name_id', '=', self.id)],
            'context': "{'create': False}"
        }


    def compute_machine_transfer_count(self):
        """Counting transfers"""
        for transfer in self:
            transfer.machine_transfer_count = self.env[
                'machine.transfer'].search_count([
                ('machine_name_id', '=', self.id)])


    def action_machine_transfer_form_view(self):
        """Action for button in machine management form"""
        return {
            "type": "ir.actions.act_window",
            "res_model": "machine.transfer",
            "view_mode": "form",
            "context": {'default_machine_name_id': self.id,
                        'default_transfer_type':'install'}

        }

    @api.depends('date_of_purchase')
    def _compute_machine_age(self):
        """Calculate machine age from purchase date"""
        for record in self:
            if record.date_of_purchase:
                today = fields.Date.today()
                purchase = record.date_of_purchase
                record.machine_age = today.year - purchase.year - (
                        (today.month, today.day) < (purchase.month,
                                                    purchase.day))
            else:
                record.machine_age = 0

    def action_service_form_view(self):
        """To redirect to the machine service form"""
        return {
                "type": "ir.actions.act_window",
                "res_model": "machine.service",
                "view_mode": "form",
                "context": {'default_machine_name_id': self.id}
        }

    def action_view_machine_service(self):
        """Smart button for machine services"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "machine.service",
            "name": "Machine Services",
            "view_mode": "list,form",
            "domain": [('machine_name_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def _compute_machine_service_count(self):
        """Counting machine services"""
        for service in self:
            service.machine_service_count = self.env[
                'machine.service'].search_count([
                ('machine_name_id', '=', self.id)])

    def unlink(self):
        """Restricting the deletion of machine if the machine has any transfer"""
        for machine in self:
            if machine.state == 'in_service':
                raise UserError("You cannot delete this machine because it is"
                                " already transferred")
        return super().unlink()

    def action_archive(self):
        """Archiving machines and also archiving all transfers and services
         associated with that machine"""
        if not self.env.user.has_group('machine_management.group_machine_manager'):
            raise UserError("You are not allowed to archive this service")
        for machine in self:
            if machine.state == 'active':
                transfers = machine.transfer_ids
                transfers.action_archive()
                services=machine.service_ids.filtered(lambda s:
                                                       s.service_state == 'open')
                other_services=machine.service_ids.filtered(lambda s
                                                            :s.service_state !=
                                                             'open')
                print(services)
                res = super().action_archive()
                if services:
                    services.action_cancel_service()
                    services.action_archive()

                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'type': 'danger',
                            'sticky': False,
                            'message': "Open services of this machines will be "
                                       "changed to cancelled state",
                            'next': {'type': 'ir.actions.act_window_close'},
                        }
                    }
                if other_services:
                    other_services.action_archive()


            else:
                raise UserError("You cannot delete the machine "
                            "which is in service state")
            return res







    # @api.depends('name', 'machine_name')
    # def _compute_display_name(self):
    #     for record in self:
    #         name = record.name or ''
    #         if record.machine_name:
    #             name = f'[{record.machine_name}] {name}'
    #         record.display_name = name
    #

    @api.model
    def recurring_maintenance(self):
        """Creating recurring maintenance for machines"""
        machines=self.search([('state','=','in_service')])
        for record in machines:
            print(record)
            if record.service_frequency == 'weekly':
                print('weekly')
                last_service_date=record.service_date+relativedelta(weeks=1)
            elif record.service_frequency == 'monthly':
                print('monthly')
                last_service_date=record.service_date+relativedelta(months=1)
            elif record.service_frequency == 'yearly':
                last_service_date=record.service_date+relativedelta(years=1)


            if record.service_ids:
                record.update({
                    'service_date': last_service_date})
            else:
                record.env['machine.service'].create({
                    'machine_name_id': record.id,
                    'customer_id': record.customer_id.id,
                })
                record.update({
                    'service_date': last_service_date})

    def action_unarchive(self):
        """Unarchiving machines and also unarchiving all transfers and services
         associated with that machine"""
        for machine in self:
            transfers = self.env[
                    'machine.transfer'].search([
                    ('active', '=', False),
                    ('machine_name_id', 'in', machine.ids)])
            transfers.action_unarchive()
            services = self.env['machine.service'].search([
                    ('active', '=', False),
                    ('machine_name_id', 'in', machine.ids)])
            services.action_unarchive()
        return super().action_unarchive()



    # @api.depends('customer_id')
    # def _compute_is_customer(self):
    #     print(self.customer_id)






            # if record.serial_number not in serial_numbers:
            #     record.env['machine.service'].create({
            #             'machine_name_id': record.id,
            #             'customer_id': record.customer_id.id,
            #             })
            #     record.update({
            #         'service_date':last_service_date})
            # else:
            #     record.update({
            #         'service_date': last_service_date})











