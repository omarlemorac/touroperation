# -*- coding: utf-8 -*_
"""
@author: Accioma
"""
from openerp.osv import osv, fields

class TourPackage(osv.Model):
    """
    @description: Tour Package that stores tour products with info regarding to a particular package
    """
    _name="tour.package"
    _columns={
        'name':fields.char('Name', size=256, required=True),
        'notes':fields.text('Notes', readonly=True),
        'adults':fields.integer('Adults',
                                help='Number of adults in tour'),
        'children':fields.integer('Children',
                                  help='Number of children in tour'),
        'infants':fields.integer('Infants',
                                 help='Number of infants in tour'),
        'start_date':fields.date('Start',
                                 help='Start date for tour'),
        'end_date':fields.date('End',
                               help='End date for tour'),
        'sale_price':fields.float('Sale Price', digits=(8,2),
                                  help='Price of package for sale to the customer'),
        'sales_person_id':fields.many2one('res.users',string="Sales Person", ondelete='set null')

        }
