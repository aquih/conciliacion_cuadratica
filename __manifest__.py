{
    'name': "Conciliación Cuadrática",
    'summary': """ Conciliación Cuadrática """,
    'description': """
        Conciliación Cuadrática
    """,
    'author': "aquíH",
    'website': "http://www.aquih.com",
    'category': 'Uncategorized',
    'version': '1.1',
    'depends': ['l10n_gt_extra'],
    'license': 'Other OSI approved licence',
    'data': [
        'security/ir.model.access.csv',
        'wizard/reporte_conciliacion_cuadratica_wizard_views.xml',
        'views/res_partner_bank_view.xml',
        'views/account_payment_view.xml',
        'views/account_bank_statement_line_views.xml',
    ],
    'demo': [
    ],
}
