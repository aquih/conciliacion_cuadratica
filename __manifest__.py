# -*- coding: utf-8 -*-
{
    'name': "Conciliación Cuadrática",

    'summary': """ Conciliación Cuadrática """,

    'description': """
        Conciliación Cuadrática
    """,

    'author': "aquíH",
    'website': "http://www.aquih.com",

    'category': 'Uncategorized',
    'version': '0.2',

    'depends': ['l10n_gt_extra'],

    'data': [
        'security/ir.model.access.csv',
        'wizard/reporte_conciliacion_cuadratica_wizard_views.xml',
        'views/res_partner_bank_view.xml',
        'views/account_payment_view.xml',
    ],
    
    'demo': [
    ],
}
