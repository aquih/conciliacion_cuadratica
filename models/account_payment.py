# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    tipo_conciliacion_cuadratica = fields.Selection([
            ('CXC Interempresa', 'CXC Interempresa'), 
            ('CXC Socios', 'CXC Socios'),
            ('CXC Empleados', 'CXC Empleados'),
            ('Anticipo a Clientes', 'Anticipo a Clientes'),
            ('Intereses Ganados', 'Intereses Ganados'),
            ('Transferencias Interempresa', 'Transferencias Interempresa'),
            ('Otros Ingresos', 'Otros Ingresos'),
        ],string="Tipo de conciliación cuadrática")
    pago_conciliacion_cuadratica = fields.Selection([
            ('Gastos Operativos', 'Gastos Operativos'),
            ('Anticipos', 'Anticipos'),
            ('Prestamos', 'Prestamos'),
            ('Dividendos', 'Dividendos'),
            ('CXP Socios', 'CXP Socio'),
            ('CXP Relacionadas Locales', 'CXP Relacionadas Locales'),
            ('Transferencias Interempresa', 'Transferencias Interempresa'),
            ('Otros Egresos', 'Otros Egresos'),
        ],string="Tipo de conciliación cuadrática de pago")
    
    cuenta_origen_conciliacion_cuadratica = fields.Many2one('res.partner.bank', string='Cuenta de origen')
    banco_origen_conciliacion_cuadratica = fields.Many2one('res.bank', string='Banco de origen', related='cuenta_origen_conciliacion_cuadratica.bank_id')

    @api.constrains('tipo_conciliacion_cuadratica', 'cuenta_origen_conciliacion_cuadratica', 'pago_conciliacion_cuadratica')
    def _check_interempresa_fields(self):
        for rec in self:
            if rec.tipo_conciliacion_cuadratica or rec.pago_conciliacion_cuadratica:
                if not rec.cuenta_origen_conciliacion_cuadratica:
                    raise ValidationError(_("Debe seleccionar una Cuenta de Origen para pagos Interempresa."))


