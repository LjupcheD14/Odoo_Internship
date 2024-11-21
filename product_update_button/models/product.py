from odoo import models, fields, api
from addons.queue_job.job import Job
import random
import string


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Add any custom fields if needed
    is_storable = fields.Boolean(string="Is Storable?", default=True)

    barcode_value = fields.Char("Barcode", help="The barcode value for the product")

    def action_enqueue_job(self):
        print("I am clicked")

        now = fields.Datetime.now()

        # Get or create the '19%' tax
        tax_19 = self._get_or_create_tax_19()
        tax_15 = self._get_or_create_tax_15()

        barcode_value = self.generate_barcode_value()

        # Prepare the supplier taxes values
        # supplier_taxes_values = [(6, 0, [tax_19.id])]

        taxes_values = (4, tax_19.id)
        supplier_taxes_values = (4, tax_15.id)

        # Define the values dictionary for the product
        values = self._prepare_product_values(now, taxes_values, supplier_taxes_values, barcode_value)

        print("Values being passed:", values)

        # Call the method to update the product job
        self.with_delay().update_product_job(values)

    def _get_or_create_tax_19(self):
        """
        Search for the '19%' tax, and create it if not found.
        Returns the tax record.
        """
        # Search for the tax record with the name '19%'
        tax_19 = self.env['account.tax'].search([('name', '=', '19%')], limit=1)

        if not tax_19:
            # If the tax is not found, create it

            # Find or create the tax group (adjust the name or ID based on your setup)
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
                'type_tax_use': 'sale',  # Or 'sale' depending on the use case
                'tax_group_id': tax_group.id,  # Assign the created or existing tax group
                'amount_type': 'percent',
            })
            print("Tax '19%' created.")

        return tax_19

    def _get_or_create_tax_15(self):
        tax_15 = self.env['account.tax'].search([('name', '=', '15%')], limit=1)

        if not tax_15:
            tax_group = self.env['account.tax.group'].search([('name', '=', 'General Sales Taxes')], limit=1)

            if not tax_group:

                tax_group = self.env['account.tax.group'].create({
                    'name': 'General Sales Taxes',
                })

            tax_15 = self.env['account.tax'].create({
                'name': '15%',
                'amount': 15.0,  # Adjust the tax rate
                'type_tax_use': 'purchase',  # Or 'sale' depending on the use case
                'tax_group_id': tax_group.id,  # Assign the created or existing tax group
                'amount_type': 'percent',
            })
            print("Tax '15%' created.")

        return tax_15

    def _prepare_product_values(self, now, taxes_values, supplier_taxes_values, barcode_value):
        """
        Prepare the values dictionary for creating/updating a product.
        """
        return {
            "name": "Product 1 " + str(now),
            "description_sale": "This is the description after the job run + exact timedate of clicking " + str(now),
            "list_price": 10.1,
            "barcode": barcode_value,
            "is_storable": True,
            "taxes_id": taxes_values,
            "supplier_taxes_id": supplier_taxes_values
        }

    def update_product_job(self, values):
        if not isinstance(values, dict):
            raise ValueError("Values must be dictionaries")
        print(f"I am updating the product {self.name}")

        self.write(values)
        print(f"I am updated the product with new name:  {self.name}")
        return

    def generate_barcode_value(self):
        barcode_value = ''.join(random.choices(string.digits, k=12))  # EAN-13 is 12 digits long
        self.barcode_value = barcode_value
        return barcode_value

    # def action_enqueue_job(self):
    #     print("I am clicked")
    #
    #     now = fields.Datetime.now()
    #
    #     # Search for the tax record with the name '19%'
    #     tax_19 = self.env['account.tax'].search([('name', '=', '19%')], limit=1)
    #
    #     if not tax_19:
    #         # If the tax is not found, create it
    #
    #         # Find or create the tax group (you may want to change the name or ID based on your setup)
    #         tax_group = self.env['account.tax.group'].search([('name', '=', 'General Sales Taxes')], limit=1)
    #
    #         if not tax_group:
    #             # If the tax group doesn't exist, create a default one
    #             tax_group = self.env['account.tax.group'].create({
    #                 'name': 'General Sales Taxes',
    #             })
    #
    #         # Create the tax '19%'
    #         tax_19 = self.env['account.tax'].create({
    #             'name': '19%',
    #             'amount': 19.0,  # Adjust the tax rate
    #             'type_tax_use': 'purchase',  # Or 'sale' depending on the use case
    #             'tax_group_id': tax_group.id,  # Assign the created or existing tax group
    #             'amount_type': 'percent',
    #         })
    #         print("Tax '19%' created.")
    #
    #     # Assign the tax to the 'supplier_taxes_id' field (many2many relation)
    #     supplier_taxes_values = [(6, 0, [tax_19.id])]
    #
    #     # Define the values dictionary
    #     values = {
    #         "name": "Product 1 " + str(now),
    #         "description_sale": "This is the description after the job run + exact timedate of clicking " + str(now),
    #         "list_price": 10.1,
    #         "barcode": "BarCodeTEST123" + str(now),
    #         "is_storable": True,
    #         "supplier_taxes_id": supplier_taxes_values,  # Overwriting the supplier_taxes_id
    #     }
    #
    #     print("Values being passed:", values)
    #
    #     # Call the method to update the product job
    #     self.with_delay().update_product_job(values)
