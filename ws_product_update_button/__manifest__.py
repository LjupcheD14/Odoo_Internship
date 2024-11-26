# Copyright (C) 2024 WeSolved BV <https://wesolved.com>
# @author X X <xx@wesolved.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Product Update Button',
    'version': '18.0',
    'author': 'WeSolved BV',
    'category': 'Sales',
    'website': 'https://www.wesolved.com',
    'license': 'AGPL-3',
    'summary': 'Individual project: Added a button to update product in product template',
    'depends': ['base', 'sale', 'queue_job'],
    'data': [
        'views/product_update_view.xml',
    ],
    'installable': True,
    'application': False,
}
