from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'


    machine_count = fields.Integer(
        string="Machine Count",
        compute='_compute_machine_count'
    )
    product_ids = fields.Many2many(
        'product.product',string="Products")
    # test_count = fields.Integer(string="Count",
    # compute='_compute_product_count',store=True)
    # active = fields.Boolean(default=True)
    is_customer = fields.Boolean(string="Is customer",
                                 compute="_compute_is_customer",
                                 search="_search_is_customer"
                                 )
    machine_ids = fields.One2many('machine.management',
                                  'customer_id')





    # @api.depends('product_ids')
    # def _compute_product_count(self):
    #     print("working")
    #     for machine in self:
    #         # print(machine.product_ids.supplier_taxes_id)
    #             # print(machine.product_ids.supplier_taxes_id.name)
    #         machine.test_count=len(machine.product_ids)


    def action_view_machines(self):
        """Smart button for transfer history"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "machine.management",
            "name": ("Machines"),
            "view_mode": "list,form",
            "domain": [('customer_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def _compute_machine_count(self):
        """Counting machines"""
        for machine in self:
            machine.machine_count = self.env[
                'machine.management'].search_count([
                ('customer_id', '=', self.id)])

    # def write(self,vals):
    #     if 'active' in vals and not vals['active']:
    #         self.env['machine.management'].search(
    #             [('customer_id', 'in', self.ids)]).active = False
    #     res = super(ResPartner, self).write(vals)
    #     return res




    def action_archive(self):
        """Archiving machines associated with a customer"""
        machines = self.env[
            'machine.management'].search([('customer_id', 'in', self.ids)])
        machines.action_archive()
        return super().action_archive()

    def _compute_is_customer(self):
        """Setting true or false for customer"""
        print("working")
        print(self)
        machines=self.env['machine.management'].search([
            ('customer_id', '=', self.id)])
        print(machines)
        if machines:
            self.is_customer = True
        else:
            self.is_customer = False

    def _search_is_customer(self, operator, value):
        """Returning customers who have a machine"""
        machines=self.env['machine.management'].search([('customer_id',
                                                         '!=', False)])
        print(machines)
        return [('id', 'in', machines.customer_id.ids)]
















        # self.machine_count = 0
        #
        # all_partners = self.with_context(active_test=False).search_fetch(
        #     [('id', 'child_of', self.ids)],
        #     ['parent_id'],
        # )
        # machine_groups = self.env['machine.management']._read_group(
        #     domain=[('partner_id', 'in', all_partners.ids)],
        #     groupby=['partner_id'], aggregates=['__count'],
        # )
        # self_ids = set(self._ids)
        #
        # for partner, count in machine_groups:
        #     while partner:
        #         if partner.id in self_ids:
        #             partner.purchase_order_count += count
        #         partner = partner.parent_id


