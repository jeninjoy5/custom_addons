# -*- coding: utf-8 -*-


{
    'name': "Purchase Order Automation",
    'version': '1.0',
    'application': False,
    'sequence':-10,
    'depends': ['product'],
    'data' : [
        'security/ir.model.access.csv',

        'wizard/purchase_order_confirm_views.xml',

        'views/product_template_views.xml']

}