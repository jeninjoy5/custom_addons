# -*- coding: utf-8 -*-


{
    'name': "Machine Management",
    'version': '1.0',
    'application': True,
    'sequence':-10,
    'summary': 'Manage Machines',
    'depends': ['mail','product','account','sale','stock','website','website_sale'],
    'data': ['security/ir.model.access.csv',
             'security/machine_management_groups.xml',

             'data/recurring_maintenace_data.xml',
             'data/mail_template.xml',
             'data/service_product_demo.xml',
             'data/machine_type_demo.xml',
             'data/sequence_data.xml',

             'wizard/transfer_report_wizard_views.xml',

             'views/snippets/s_machine.xml',
             'views/machine_management_portal_templates.xml',
             'views/machine_service_request_templates.xml',
             'views/machine_service_request_menu.xml',
             'report/machine_transfer_templates.xml',
             'report/machine_transfer_reports.xml',
             'views/machine_service_views.xml',
             'views/res_partner_views.xml',
             'views/machine_tags_views.xml',
             'views/machine_transfer_views.xml',
             'views/machine_type_views.xml',
             'views/machine_management_views.xml',
             'views/machine_management_menu.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'machine_management/static/src/js/action_manager.js'
        ],
        'web.assets_frontend': ['machine_management/static/src/xml/machine_snippet_template.xml',
            'machine_management/static/src/js/latest_machine.js'],
    },
}