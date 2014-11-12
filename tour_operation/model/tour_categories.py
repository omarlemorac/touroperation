# -*- coding: utf-8 -*_
"""
@author: Accioma
"""
from openerp.osv import osv, fields

class PackageClass(osv.Model):
    """
    @description: Package class

    """
    _name="tour.package.class"
    _columns={
        'name':fields.char('Name', size=100, required=True, translate=True),
        'description':fields.text('Description'),
        }


class LodgeClass(osv.Model):
    """
    @description: Lodge Class

    """
    _name="tour.lodge.class"
    _columns={
        'name':fields.char('Name', size=100, required=True, translate=True),
        'description':fields.text('Description'),
        }

class LodgeRoomType(osv.Model):
    """
    @description: Lodge Room Type

    """
    _name="tour.lodge.room.type"
    _columns={
        'name':fields.char('Name', size=100, required=True, translate=True),
        'description':fields.text('Description'),
        'product_id':fields.many2one('product.product', 'Product')
        }

class CruiseCabin(osv.Model):
    """
    @description: Cruise cabin tag

    """
    _name="tour.cruise.cabin"
    _columns={
        'name':fields.char('Name', size=100, required=True, translate=True),
        'description':fields.text('Description'),
        'product_id':fields.many2one('product.product', 'Product')
        }

class CruiseClass(osv.Model):
    """
    @description: Cruise class tag

    """
    _name="tour.cruise.class"
    _columns={
        'name':fields.char('Name', size=100, required=True, translate=True),
        'description':fields.text('Description')

        }

class CruiseStyle(osv.Model):
    """
    @description: Cruise style category tag

    """
    _name="tour.cruise.style"
    _columns={
        'name':fields.char('Name', size=100, required=True, translate=True),
        'description':fields.text('Description')

        }

class CruiseBedType(osv.Model):
    """
    @description: Bed type tag

    """
    _name="tour.cruise.bed.type"
    _columns={
        'name':fields.char('Name', size=100, required=True, translate=True),
        'description':fields.text('Description'),
        'product_id':fields.many2one('product.product', 'Product')
        }


class AccommodationStyle(osv.Model):
    """
    @description: Accommodation style category tag

    """
    _name="tour.accommodation.style"
    _columns={
        'name':fields.char('Name', size=100, required=True, translate=True),
        'description':fields.text('Description')
        }

class Cruise(osv.Model):
    """
    @description: Cruise class category tag

    """
    _name="tour.cruise.class"
    _columns={
        'name':fields.char('Name', size=100, required=True, translate=True),
        'description':fields.text('Description')
        }

class CabinType(osv.Model):
    """
    @description: Cabin type tag
    @note: Posibly unused class

    """
    _name="tour.cabin.type"
    _columns={
        'name':fields.char('Name', size=100, required=True, translate=True),
        'description':fields.text('Description'),
        'product_id':fields.many2one('product.product', 'Product')
        }

class BedType(osv.Model):
    """
    @description: Bed type tag

    """
    _name="tour.bed.type"
    _columns={
        'name':fields.char('Name', size=100, required=True, translate=True),
        'description':fields.text('Description'),
        'product_id':fields.many2one('product.product', 'Product')
        }

class Language(osv.Model):
    """
    @description: Language tag

    """
    _name="tour.language"
    _columns={
        'name':fields.char('Name', size=100, required=True, translate=True),
        'language_id':fields.char('Language', size=5, requiered=True),
        'description':fields.text('Description'),
        'product_id':fields.many2one('product.product', 'Product')
        }

class Transportation(osv.Model):
    """
    @description: Transportation tag

    """
    _name="tour.transportation"
    _columns={
        'name':fields.char('Name', size=100, required=True, translate=True),
        'description':fields.text('Description')
        }



class AccommodationRoomType(osv.Model):
    """
    @description: Accommodation room type: single, twin, double, etc.

    """
    _name="tour.accommodation.room.type"
    _columns={
        'name':fields.char('Name', size=100, required=True, translate=True),
        'description':fields.text('Description'),
        'product_id':fields.many2one('product.product', 'Product')
        }
