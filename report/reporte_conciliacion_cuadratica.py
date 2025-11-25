# -*- encoding: utf-8 -*-

from odoo import api, models
import logging

class ReporteConciliacionCuadratica(models.AbstractModel):
    _name = 'report.conciliacion_cuadratica.reporte_conciliacion'
    _description = 'Reporte de Conciliación Cuadrática'

    def saldo_inicial_por_mes(self, datos):
        cuenta_id = datos['cuenta_id'].id
        year = int(datos['year'])
        year_inicio = f"{year}-01-01"
        next_year_inicio = f"{year+1}-01-01"

        self.env.cr.execute("""
            SELECT
                CASE
                    WHEN date < %s THEN 0
                    ELSE EXTRACT(MONTH FROM date)::int
                END AS mes_index,
                COALESCE(SUM(debit) - SUM(credit), 0) AS monto
            FROM account_move_line
            WHERE account_id = %s
            AND parent_state = 'posted'
            AND date < %s
            GROUP BY mes_index
            ORDER BY mes_index
        """, (year_inicio, cuenta_id, next_year_inicio))
        meses_data = self.env.cr.dictfetchall()
        montos_por_mes = {int(md['mes_index']): float(md['monto']) for md in meses_data}
        balance_acumulado = montos_por_mes.get(0, 0.0)
        
        saldo_incial_mensual = []
        for mes in range(1, 13):
            saldo_incial_mensual.append(balance_acumulado)
            balance_acumulado += montos_por_mes.get(mes, 0.0)

        saldo_final_mensual = []
        for mes in range(1, 13):
            balance_acumulado += montos_por_mes.get(mes, 0.0)
            saldo_final_mensual.append(balance_acumulado)
        resultados = [saldo_incial_mensual, saldo_final_mensual]
        return resultados

    def filtrar_datos(self, pagos, tipo_pago, tipo_conciliacion=None, pago_conciliacion=None):
        if tipo_pago == 'inbound':
            pagos = pagos.filtered(lambda p: p.payment_type == 'inbound')
        else:
            pagos = pagos.filtered(lambda p: p.payment_type == 'outbound')

        #filtros de ingresos
        if tipo_conciliacion == 'cxc_local':
            pagos = pagos.filtered(
                lambda p: not p.tipo_conciliacion_cuadratica and 
                        (p.partner_id.country_id.code == 'GT' or not p.partner_id.country_id))
        elif tipo_conciliacion == 'cxc_exterior':
            pagos = pagos.filtered(
                lambda p: not p.tipo_conciliacion_cuadratica and 
                        (p.partner_id.country_id and p.partner_id.country_id.code != 'GT'))
        elif tipo_conciliacion == 'cxc_interempresa':
            pagos = pagos.filtered(lambda p: p.tipo_conciliacion_cuadratica == 'CXC Interempresa')
        elif tipo_conciliacion == 'cxc_socios':
            pagos = pagos.filtered(lambda p: p.tipo_conciliacion_cuadratica == 'CXC Socios')
        elif tipo_conciliacion == 'cxc_empleados':
            pagos = pagos.filtered(lambda p: p.tipo_conciliacion_cuadratica == 'CXC Empleados')
        elif tipo_conciliacion == 'anticipo_clientes':
            pagos = pagos.filtered(lambda p: p.tipo_conciliacion_cuadratica == 'Anticipo a Clientes')
        elif tipo_conciliacion == 'intereses_ganados':
            pagos = pagos.filtered(lambda p: p.tipo_conciliacion_cuadratica == 'Intereses Ganados')
        elif tipo_conciliacion == 'transfer_interempresa':
            pagos = pagos.filtered(lambda p: p.tipo_conciliacion_cuadratica == 'Transferencias Interempresa')
        elif tipo_conciliacion == 'otros_ingresos':
            pagos = pagos.filtered(lambda p: p.tipo_conciliacion_cuadratica == 'Otros Ingresos')

        #filtros de egresos
        if pago_conciliacion == 'gastos_operativos':
            pagos = pagos.filtered(lambda p: p.pago_conciliacion_cuadratica == 'Gastos Operativos')
        elif pago_conciliacion == 'anticipos':
            pagos = pagos.filtered(lambda p: p.pago_conciliacion_cuadratica == 'Anticipos')
        elif pago_conciliacion == 'prestamos':
            pagos = pagos.filtered(lambda p: p.pago_conciliacion_cuadratica == 'Prestamos')
        elif pago_conciliacion == 'dividendos':
            pagos = pagos.filtered(lambda p: p.pago_conciliacion_cuadratica == 'Dividendos')
        elif pago_conciliacion == 'cxp_socios':
            pagos = pagos.filtered(lambda p: p.pago_conciliacion_cuadratica == 'CXP Socios')
        elif pago_conciliacion == 'cxp_relacionadas_locales':
            pagos = pagos.filtered(lambda p: p.pago_conciliacion_cuadratica == 'CXP Relacionadas Locales')
        elif pago_conciliacion == 'cxp_relacionadas_exterior':
            pagos = pagos.filtered(
                lambda p: not p.pago_conciliacion_cuadratica and 
                        (p.partner_id.country_id and p.partner_id.country_id.code != 'GT')) 
        elif pago_conciliacion == 'transfer_interempresa':
            pagos = pagos.filtered(lambda p: p.pago_conciliacion_cuadratica == 'Transferencias Interempresa')
        elif pago_conciliacion == 'otros_egresos':
            pagos = pagos.filtered(lambda p: p.pago_conciliacion_cuadratica == 'Otros Egresos')       
        return pagos

    def obtener_montos_mensuales(self, datos):
        totales = [0.0] * 12
        for d in datos:
            mes = d.date.month
            totales[mes-1] += d.amount
        return totales
    
    def obtener_totales_mensuales(self, datos):
        totales = [0.0] * 12
        for mes in range(0, 12):
            for d in datos:
                totales[mes] += d[mes]
        return totales
