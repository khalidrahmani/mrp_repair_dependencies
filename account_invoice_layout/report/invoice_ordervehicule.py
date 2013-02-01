# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time

from report import report_sxw
from tools import amount_to_text
import pooler

class invoicevehicule(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(invoicevehicule, self).__init__(cr, uid, name, context=context)        
        self.localcontext.update({
            'time': time,
            'caracteristiques': self.caracteristiques,
            'amount_in_word': self.amount_in_word,
            'format_quantity': self.format_quantity,
            'saleorder': self.saleorder
        })
    
    def saleorder(self, order):
        pool = pooler.get_pool(self.cr.dbname)
        sale_order_obj = pool.get('sale.order')
        oid = sale_order_obj.search(self.cr, self.uid, [('name','=',order.origin)])[0]
        saleorder = sale_order_obj.browse(self.cr, self.uid, oid)     
        return saleorder
        
        
    def caracteristiques(self, order):
        pool = pooler.get_pool(self.cr.dbname)
        sale_order_obj = pool.get('sale.order')
        oid = sale_order_obj.search(self.cr, self.uid, [('name','=',order.origin)])[0]
        saleorder = sale_order_obj.browse(self.cr, self.uid, oid)          
        
        order_lines = saleorder.order_line       
        line = order_lines[0]
        voiture = line.product_id
        cars = []     
        for car in voiture.caracteristiques_ids:
            if car.visible : 
                cars.append(car)  
        return cars
    def format_quantity(self, qty):
        return "0"+ str(int(qty))
    def amount_in_word(self, amount):
        return amount_to_text(amount, 'fr', 'DH')
            
report_sxw.report_sxw('report.invoice.ordervehicule', 'account.invoice', 'addons/account_invoice_layout/report/invoice_ordervehicule.rml', parser=invoicevehicule, header="external")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

