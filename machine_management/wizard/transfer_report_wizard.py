import io
import json

from odoo import models,fields,api
from odoo.exceptions import ValidationError
from odoo.tools import json_default

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

class TransferReportWizard(models.TransientModel):
    _name = 'transfer.report.wizard'


    from_date = fields.Datetime(string='From Date')
    to_date = fields.Datetime(string='To Date')
    customer_ids = fields.Many2many('res.partner', string='Customer')
    transfer_type = fields.Selection([('install','Install'),
                                      ('remove','Remove')],
                                     string="Transfer Type")
    machine_ids = fields.Many2many('machine.management', string='Machine')
    # allowed_machine_ids=fields.Many2many('machine.management','transfer_wizard_rel','wizard_id','machine_id')



    # @api.onchange('transfer_type')
    # def _onchange_transfer_type(self):
    #     if self.transfer_type == "install":
    #         machines=self.env['machine.management'].search([
    #             ('state', '=', 'active')])
    #         self.update({'allowed_machine_ids':[(fields.Command.set(
    #             machines.ids))]})
    #     elif self.transfer_type == "remove":
    #         machines=self.env['machine.management'].search([
    #             ('state', '=', 'in_service')])
    #         self.update({'allowed_machine_ids':[(fields.Command.set(
    #             machines.ids))]})



    def action_report_machine_transfer(self):
        print(self)
        records=self.env['machine.transfer'].search([])
        if not records:
            raise ValidationError("Records not Found")
        query = """select pr.name as customer,mm.machine_name as machine,mt.transfer_type 
                as transfer_type,mt.transfer_date as transfer_date from machine_transfer as mt
                inner join res_partner as pr on pr.id=mt.customer_id
                inner join machine_management as mm on mm.id=mt.machine_name_id"""
        customer = []
        machine = []
        if self.from_date and self.to_date:
            if self.from_date > self.to_date:
                raise ValidationError("Date are not valid")
            query += """ and mt.transfer_date >= '%s' and mt.transfer_date <= '%s'"""%(self.from_date,self.to_date)
        if self.from_date:
            query += """ and mt.transfer_date >= '%s'"""%self.from_date
        if self.to_date:
            query += """ and mt.transfer_date <= '%s'"""%self.to_date
        if self.customer_ids:
            print(self.customer_ids.ids)
            customer_ids = ",".join(map(str,self.customer_ids.ids))
            print(customer_ids)
            query += """ and mt.customer_id in (%s)"""%customer_ids
            if len(customer_ids)==1:
                customer.append(self.customer_ids.name)
        if self.transfer_type:
            query += """ and mt.transfer_type = '%s'"""%self.transfer_type
        if self.machine_ids:
            machine_ids = ",".join(map(str,self.machine_ids.ids))
            query += """ and mt.machine_name_id in (%s)"""%machine_ids
            if len(machine_ids)==1:
                machine.append(self.machine_ids.name)
        print(query)
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        print(report)
        data = {'report':report,
                'customer':customer,
                'machine':machine,
                }
        print(data)
        return self.env.ref('machine_management.action_report_machine_transfer_form').report_action(self, data=data)



    def action_xlsx_report_machine_transfer(self):
        records = self.env['machine.transfer'].search([])
        if not records:
            raise ValidationError("Records not Found")
        query = """select pr.name as customer,mm.machine_name as machine,mt.transfer_type 
                        as transfer_type,mt.transfer_date as transfer_date from machine_transfer as mt
                        inner join res_partner as pr on pr.id=mt.customer_id
                        inner join machine_management as mm on mm.id=mt.machine_name_id"""
        customer = []
        machine = []
        if self.from_date and self.to_date:
            if self.from_date > self.to_date:
                raise ValidationError("Date are not valid")
            query += """ and mt.transfer_date >= '%s' and mt.transfer_date <= '%s'""" % (
                self.from_date, self.to_date)
        if self.from_date:
            query += """ and mt.transfer_date >= '%s'""" % self.from_date
        if self.to_date:
            query += """ and mt.transfer_date <= '%s'""" % self.to_date
        if self.customer_ids:
            print(self.customer_ids.ids)
            customer_ids = ",".join(map(str, self.customer_ids.ids))
            print(customer_ids)
            query += """ and mt.customer_id in (%s)""" % customer_ids
            if len(customer_ids) == 1:
                customer.append(self.customer_ids.name)
        if self.transfer_type:
            query += """ and mt.transfer_type = '%s'""" % self.transfer_type
        if self.machine_ids:
            machine_ids = ",".join(map(str, self.machine_ids.ids))
            query += """ and mt.machine_name_id in (%s)""" % machine_ids
            if len(machine_ids) == 1:
                machine.append(self.machine_ids.name)
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        data={'report': report,
              'customer':customer,
              'machine':machine
              }
        print(data['report'])
        if not data['report']:
            raise ValidationError("No record found")
        return {
                'type': 'ir.actions.report',
                'data': {'model': 'transfer.report.wizard',
                         'options': json.dumps(data, default=json_default),
                         'output_format': 'xlsx',
                         'report_name': 'Machine Transfer Report',
                         },
                'report_type': 'xlsx'
        }

    def get_xlsx_report(self,data,response):
        print(data['customer'])
        print(data['machine'])
        print(data['report'])
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output,{'in_memory':True})
        sheet = workbook.add_worksheet('report')
        sheet.set_column(2, 2, 15)
        sheet.set_column(3, 3, 15)
        sheet.set_column(4, 4, 15)
        sheet.set_column(5, 5, 15)
        sheet.set_column(6, 6, 15)
        sheet.set_column(7, 7, 15)
        sheet.set_column(8, 8, 15)
        sheet.set_column(9, 9, 15)
        sheet.set_column(10, 10, 15)
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        cell_format = workbook.add_format({'font_size': '12px',
                                           'align':'center','bold':True})
        data_format = workbook.add_format({'align':'center'})
        sheet.merge_range('E3:I4','MACHINE TRANSFER REPORT',head)
        transfer_install=[]
        transfer_remove=[]
        for record in data['report']:
            if record['transfer_type'] == 'install':
                transfer_install.append("install")
            if record['transfer_type'] == 'remove':
                transfer_remove.append("remove")
        # col=2
        # if len(data['machine']) == 1:
        #     sheet.write(5, col, 'Machine:', cell_format)
        #     sheet.write(6, col, data['machine'][0])
        #     col+=1
        # if len(data['customer']) == 1:
        #     sheet.write(5, col, 'Customer:', cell_format)
        #     sheet.write(6, col, data['customer'][0])
        # col=2
        # if len(data['machine']) != 1:
        #     sheet.write(8, col, 'Machine', cell_format)
        #     col+=1
        # if len(data['customer']) != 1:
        #     sheet.write(8, col, 'Customer', cell_format)
        #     col+=1
        # sheet.write(8, col, 'Transfer Type', cell_format)
        # col+=1
        # sheet.write(8, col, 'Transfer Date', cell_format)
        if transfer_install:
            sheet.merge_range('C8:E8', 'Transfer Type : Install', cell_format)
            col = 2
            if len(data['machine']) == 1:
                sheet.write(4, col, 'Machine:', cell_format)
                sheet.write(5, col, data['machine'][0],data_format)
                col += 1
            if len(data['customer']) == 1:
                sheet.write(4, col, 'Customer:', cell_format)
                sheet.write(5, col, data['customer'][0],data_format)
            col = 2
            if len(data['machine']) != 1:
                sheet.write(9, col, 'Machine', cell_format)
                col += 1
            if len(data['customer']) != 1:
                sheet.write(9, col, 'Customer', cell_format)
                col += 1
            sheet.write(9, col, 'Transfer Type', cell_format)
            col += 1
            sheet.write(9, col, 'Transfer Date', cell_format)
            row = 9
            col = 2
            for record in data['report']:
                if record['transfer_type'] == 'install':
                    row += 1
                    if len(data['machine']) != 1:
                        sheet.write(row, col, record['machine'],data_format)
                        col+=1
                    if len(data['customer']) != 1:
                        sheet.write(row, col, record['customer'],data_format)
                        col+=1
                    sheet.write(row, col, record['transfer_type'],data_format)
                    col+=1
                    sheet.write(row, col, record['transfer_date'],data_format)
                    col=2

        if transfer_remove:
            sheet.merge_range('H8:J8', 'Transfer Type : Remove', cell_format)
            col = 7
            if len(data['machine']) == 1:
                sheet.write(4, col, 'Machine:', cell_format)
                sheet.write(5, col, data['machine'][0],data_format)
                col += 1
            if len(data['customer']) == 1:
                sheet.write(4, col, 'Customer:', cell_format)
                sheet.write(5, col, data['customer'][0],data_format)
            col = 7
            if len(data['machine']) != 1:
                sheet.write(9, col, 'Machine', cell_format)
                col += 1
            if len(data['customer']) != 1:
                sheet.write(9, col, 'Customer', cell_format)
                col += 1
            sheet.write(9, col, 'Transfer Type', cell_format)
            col += 1
            sheet.write(9, col, 'Transfer Date', cell_format)
            row = 9
            col = 7
            for record in data['report']:
                if record['transfer_type'] == 'remove':
                    row += 1
                    if len(data['machine']) != 1:
                        sheet.write(row, col, record['machine'],data_format)
                        col += 1
                    if len(data['customer']) != 1:
                        sheet.write(row, col, record['customer'],data_format)
                        col += 1
                    sheet.write(row, col, record['transfer_type'],data_format)
                    col += 1
                    sheet.write(row, col, record['transfer_date'],data_format)
                    col = 2
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()





