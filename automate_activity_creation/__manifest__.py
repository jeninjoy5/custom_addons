# -*- coding: utf-8 -*-


{
    'name': "Automate Activity Creation",
    'version': '1.0',
    'application': False,
    'sequence': -10,
    'depends': ['purchase'],
    'data': [
        'data/activity_creation_data.xml',
        'data/mail_template.xml'
             ]

}