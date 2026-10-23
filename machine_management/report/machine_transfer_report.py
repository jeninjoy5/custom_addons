from odoo import models,api,fields

class MachineTransferReport(models.AbstractModel):
    _name = 'report.machine_management.form_machine_transfer_report'

    @api.model
    def _get_report_values(self,docids,data=None):
        docs=data.get('report')
        customer=data.get('customer')
        machine=data.get('machine')
        transfer_install = []
        transfer_remove = []
        print(docs)
        for types in docs:
            print(types)
            if types['transfer_type'] == 'install':
                transfer_install.append("install")
            if types['transfer_type'] == 'remove':
                transfer_remove.append("remove")
        print(transfer_install)
        print(transfer_remove)
        print(docids)
        print(data)
        print(customer)
        return {
            'doc_ids': docids,
            'doc_model': 'transfer.report.wizard',
            'docs': docs,
            'customer': customer,
            'machine': machine,
            'transfer_install': transfer_install,
            'transfer_remove': transfer_remove

        }
