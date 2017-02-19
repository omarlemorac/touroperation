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
{
    'name': 'Voucher of Service',
    'version': '8.0.1',
    'author': 'Accioma',
    'category': 'Tour Operation',
    'description': """
================================
Voucher of Service
================================
Voucher of Service functionality for folio y tour operation
It allows to fill the voucher of service that will be sended to
tour operator or passenger.

    """,
    'website': 'http://www.accioma.com',
    'images': [],
    'depends': [
        'base', 'tour_operation', "partner_firstname", "report_webkit",
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/voucher_of_service_view.xml',
        'report/voucher_of_service_report.xml'
    ],
    'js': [
    ],
    'qweb' : [
    ],
    'css':[
    ],
    'demo': [
 #       'demo/voucher_of_service.xml',
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
