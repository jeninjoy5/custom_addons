# -*- coding: utf-8 -*-


{
    'name': "Product Fields",
    'version': '1.0',
    'application': False,
    'sequence':-10,
    'depends': ['product','sale','stock'],
    'data' : ['security/ir.model.access.csv',

              'data/product_brand_data.xml',
              'data/location_data.xml',

              'views/res_partner_views.xml',
              'views/sale_order_views.xml',
              'views/product_brand.xml',
              'views/product_template.xml',
    ]
}