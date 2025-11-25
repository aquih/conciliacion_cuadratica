# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    account_type = fields.Selection(
        [
            ('Ahorro', 'Ahorro'),
            ('Monetaria', 'Monetaria'),
            ('Cuenta Corriente', 'Cuenta Corriente'),
            ('Otro', 'Otro'),
        ],
        string="Tipo de cuenta",
    )