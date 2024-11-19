{
    'name': 'Product Update Button',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Add a button to update product in product template',
    'depends': ['sale', 'queue_job'],
    'data': [
        'views/product_template_view.xml',
    ],
    'installable': True,
    'application': False,
}
