# -*- coding: utf-8 -*-



{
    'name': "Purchase Order Attachment",
    'version': '1.0',
    'application': False,
    'sequence' :-10,
    'depends': ['purchase'],
    'data' : ['views/purchase_order_views.xml',
        'views/res_config_settings_views.xml']

}