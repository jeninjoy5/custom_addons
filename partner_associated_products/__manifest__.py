# -*- coding: utf-8 -*-



{
    'name': "Partner Associated Products",
    'version': '1.0',
    'application': False,
    'sequence' :-10,
    'depends': ['product','sale'],
    'data' : ['views/sale_order_views.xml',
              'views/res_partner_views.xml'
              ]

}