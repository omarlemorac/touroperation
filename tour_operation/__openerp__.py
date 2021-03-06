# -*- coding: utf-8 -*-
{
    "name":"Tour Operation",
    "description":"""\
Tour Operation functionality
_____________________________________________

- Manage tour products:
  Cruises, accommodations, flight tickets, lodges, transfers, miscellaneous.
- Tour and Travel categories for products
- Travel Voucher of Service. TODO:
- Manage pax (passengers).
- Invoice creation.
- Account invoice integration.
    """,
    "category":"Tour & Travel Operation",
    "author":"Accioma",
    "data":["security/res_groups.xml",
            "security/ir.model.access.csv",
            "views/tour_operation_view.xml",
           ],
    "demo" : [
        #"demo/product_demo.xml",
        ],

    "depends":["base", "sale", "l10n_ec_advances"],
    "installable":True
}
