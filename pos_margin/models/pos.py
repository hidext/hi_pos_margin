# -*- coding: utf-8 -*-
##############################################################################
#    Hidext
#    Copyright (C) 2018-TODAY Hidext (<http://www.hidext.com>).
#    Author: Hidext(<http://www.hidext.com>)
##############################################################################

from odoo import fields, models,api
import odoo.addons.decimal_precision as dp

class PosOrder(models.Model):
    _inherit ='pos.order'
    profit = fields.Float(compute='_product_profit',digits=dp.get_precision('Product Price'), string="Profit")

    @api.depends('lines.profit')
    def _product_profit(self):
        for order in self:
            order.profit = sum(order.lines.mapped('profit'))
            
class PosOrderLine(models.Model):
    _inherit ='pos.order.line'   
        
    purchase_price = fields.Float(string='Cost', compute='product_id_change_profit', digits=dp.get_precision('Product Price'), store=True)
    profit = fields.Float(compute='_product_profit', digits=dp.get_precision('Product Price'), store=True)

    @api.depends('product_id')
    def product_id_change_profit(self):
        for line in self:
            line.purchase_price = line.product_id.standard_price
        return

    @api.depends('product_id', 'purchase_price', 'price_unit')
    def _product_profit(self):
        for line in self:
            # print("lineeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",line)
            line.profit = line.price_subtotal_incl - ((line.purchase_price or line.product_id.standard_price) * line.qty)

