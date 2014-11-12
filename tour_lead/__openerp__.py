# -*- coding: utf-8 -*-
{
    "name":"Tour Lead",
    "description":"""\
Detailed leads for tour operation
_____________________________________________

- Manage leads including tour products:
  Cruises, accommodations, flight tickets, lodges, transfers, miscellaneous.
- Tour and Travel categories for products
- Travel itinerary. TODO:
- Manage pax (passengers). TODO:
- Sale order creation. TODO:
- Account invoice integration. TODO:
    """,
    "category":"Tour & Travel Operation",
    "author":"Accioma",
    "data":[
        'wizard/quot_advance_payment_inv.xml',
        'views/crm_lead_view.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
           ],

    "depends":["base", "sale", "crm","tour_operation"],
    "installable":True
}
