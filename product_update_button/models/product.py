from odoo import models, fields, api
from datetime import datetime
from addons.queue_job.job import Job


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Add any custom fields if needed
    is_storable = fields.Boolean(string="Is Storable?", default=True)

    def action_enqueue_job(self):
        print("I am clicked")

        now = fields.Datetime.now()

        # Search for the tax record with the name '19%'
        tax_19 = self.env['account.tax'].search([('name', '=', '19%')], limit=1)

        if not tax_19:
            # If the tax is not found, create it

            # Find or create the tax group (you may want to change the name or ID based on your setup)
            tax_group = self.env['account.tax.group'].search([('name', '=', 'General Sales Taxes')], limit=1)

            if not tax_group:
                # If the tax group doesn't exist, create a default one
                tax_group = self.env['account.tax.group'].create({
                    'name': 'General Sales Taxes',
                })

            # Create the tax '19%'
            tax_19 = self.env['account.tax'].create({
                'name': '19%',
                'amount': 19.0,  # Adjust the tax rate
                'type_tax_use': 'purchase',  # Or 'sale' depending on the use case
                'tax_group_id': tax_group.id,  # Assign the created or existing tax group
                'amount_type': 'percent',
            })
            print("Tax '19%' created.")

        # Assign the tax to the 'supplier_taxes_id' field (many2many relation)
        supplier_taxes_values = [(6, 0, [tax_19.id])]

        # Define the values dictionary
        values = {
            "name": "Product 1 " + str(now),
            "description_sale": "This is the description after the job run + exact timedate of clicking " + str(now),
            "list_price": 10.1,
            "barcode": "BarCodeTEST123" + str(now),
            "is_storable": True,
            "supplier_taxes_id": supplier_taxes_values,  # Overwriting the supplier_taxes_id
        }

        print("Values being passed:", values)

        # Call the method to update the product job
        self.with_delay().update_product_job(values)

    def update_product_job(self, values):
        if not isinstance(values, dict):
            raise ValueError("Values must be dictionaries")
        print(f"I am updating the product {self.name}")

        self.write(values)
        print(f"I am updated the product with new name:  {self.name}")
        return
