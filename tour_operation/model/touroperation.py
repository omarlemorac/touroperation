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


from openerp import api, exceptions, fields, models
import openerp.addons.decimal_precision as dp
import datetime

class airport(models.Model):
    _name='touroperation.airport'
    _description='Airport'

    name = fields.Char('Name', size=100, required=True, select=True)
    description = fields.Char('Description', size=255, required=True)
    country_id = fields.Many2one('res.country', string='Country')

class airline(models.Model):
    _name='touroperation.airline'
    _description='Airline'
    name = fields.Char('Name', size=100, required=True, select=True)
    description = fields.Char('Description', size=255)


