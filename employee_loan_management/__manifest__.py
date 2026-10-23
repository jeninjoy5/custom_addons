# -*- coding: utf-8 -*-


{
    'name': "Employee Loan Management",
    'version': '1.0',
    'application': True,
    'sequence': -10,
    'depends': ['hr','mail'],
    'data': ['data/sequence_data.xml',

            'security/ir.model.access.csv',

            'views/employee_loan_line_views.xml',
            'views/employee_loan_views.xml',
            'views/employee_loan_menu.xml']

}