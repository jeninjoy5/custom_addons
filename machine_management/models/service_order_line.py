from odoo import models,fields,api



class ServiceOrderLine(models.Model):
    _name = 'service.order.line'

    order_id = fields.Many2one('machine.service',
                               string='Order',
                               required=True,
                               ondelete='cascade',
                               index=True,
                               copy=False)
    parts_id = fields.Many2one(string="Parts",
                               comodel_name='product.template',
                               required=True,
                               domain="[('id','in',allowed_parts_ids)]",)
    parts_qty = fields.Float(string="Quantity",
                             digits='Product Unit',
                             default=1.0,
                             required=True)
    price_unit = fields.Float(string="Unit Price",
                              related = "parts_id.list_price",
                              readonly=False)
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
    price_total = fields.Monetary(string="Total",
                                  readonly=False,
                                  compute="_compute_price_total")
    allowed_parts_ids = fields.Many2many(comodel_name='product.product',
                                         compute='_allowed_parts_ids')



    @api.depends('parts_id','parts_qty','price_unit')
    def _compute_price_total(self):
        """Calculating the total amount of price per product"""
        for line in self:
            line.price_total=line.parts_qty*float(line.price_unit)


    @api.depends('order_id.machine_name_id')
    def _allowed_parts_ids(self):
        """Calculating the list of allowed parts ids"""
        for record in self:
            if record.order_id.machine_name_id:
                parts=record.order_id.machine_name_id.order_line_ids.parts_id
                self.update({'allowed_parts_ids':[(fields.Command.set(
                    parts.ids))]})


