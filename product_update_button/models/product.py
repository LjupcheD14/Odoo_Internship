from odoo import models, fields, api

import random
import string


class JobQueue(models.Model):
    _inherit = 'queue.job'

    products = fields.One2many('product.template', 'job_id', string='Products')
    model_name = fields.Char(string='Model Name', store=True)
    name = fields.Char(string='Job Name', store=True)

    @api.model
    def create(self, vals):
        # Get the product name from context
        product_name = self.env.context.get('product_name', 'Default Product Name')

        # Use the product_name in the job creation logic
        vals['name'] = f"Job for: {product_name}"

        return super(JobQueue, self).create(vals)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Add any custom fields if needed
    is_storable = fields.Boolean(string="Is Storable?", default=True)

    barcode_value = fields.Char("Barcode", help="The barcode value for the product")

    job_id = fields.Many2one('queue.job', string='Job Queue', help="Job linked to this product")

    def action_enqueue_job(self):
        print("I am clicked")

        now = fields.Datetime.now()

        # To get or create tax 19%
        tax_19 = self._get_or_create_tax(19)

        # To get or create tax 15%
        tax_15 = self._get_or_create_tax(15)

        barcode_value = self.generate_barcode_value()

        taxes_values = (4, tax_19.id)
        supplier_taxes_values = (4, tax_15.id)

        # Define the values dictionary for the product
        values = self._prepare_product_values(now, taxes_values, supplier_taxes_values, barcode_value)

        print("Values being passed:", values)

        # Add product_name to the context
        self = self.with_context(product_name=self.name)

        # Call the method to update the product job
        self.with_delay().update_product_job(values)

    def _get_or_create_tax(self, tax_rate):
        """
        Search for the tax with the given rate, and create it if not found.
        Returns the tax record.
        """
        # Search for the tax record with the specified rate
        tax = self.env['account.tax'].search([('name', '=', f'{tax_rate}%')], limit=1)

        if not tax:
            # If the tax is not found, create it

            # Find or create the tax group (adjust the name or ID based on your setup)
            tax_group = self.env['account.tax.group'].search([('name', '=', 'General Sales Taxes')], limit=1)

            if not tax_group:
                # If the tax group doesn't exist, create a default one
                tax_group = self.env['account.tax.group'].create({
                    'name': 'General Sales Taxes',
                })

            # Create the tax with the given rate
            tax = self.env['account.tax'].create({
                'name': f'{tax_rate}%',  # Using the dynamic tax rate
                'amount': tax_rate,  # Using the dynamic tax rate
                'type_tax_use': 'sale',  # Adjust based on use case ('sale' or 'purchase')
                'tax_group_id': tax_group.id,  # Assign the created or existing tax group
                'amount_type': 'percent',
            })
            print(f"Tax '{tax_rate}%' created.")

        return tax

    def _prepare_product_values(self, now, taxes_values, supplier_taxes_values, barcode_value):
        """
        Prepare the values dictionary for creating/updating a product.
        You can include {self.name} dynamically here, but be aware that {self.name} may not be set yet.
        """
        product_name = self.name if self.name else "Product 1"  # Fallback in case self.name is not set

        product_values = {
            "name": f"{product_name} - {str(now)}",  # Using self.name with the timestamp
            "description_sale": f"This is the description after the job run + exact timedate of clicking {str(now)}",
            "list_price": 10.1,
            "barcode": barcode_value,
            "is_storable": True,
            "taxes_id": taxes_values,
            "supplier_taxes_id": supplier_taxes_values
        }

        return product_values

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
    #     # Get the current time
    #     now = fields.Datetime.now()
    #
    #     # Get or create the '19%' and '15%' tax
    #     tax_19 = self._get_or_create_tax_19()
    #     tax_15 = self._get_or_create_tax_15()
    #
    #     # Generate barcode value
    #     barcode_value = self.generate_barcode_value()
    #
    #     # Prepare the supplier taxes values
    #     taxes_values = (4, tax_19.id)
    #     supplier_taxes_values = (4, tax_15.id)
    #
    #     # Prepare product values
    #     values = self._prepare_product_values(now, taxes_values, supplier_taxes_values, barcode_value)
    #
    #     print("Values being passed:", values)
    #
    #     # Create or update a queue.job record
    #     queue_job = self.env['queue.job'].with_delay().create({
    #         'name': f'Job for {self.name}',  # Setting the name field in queue.job (You can customize this)
    #         'product_template_id': self.id,  # Linking the queue job to the current product template
    #         'custom_job_field': 'Custom job value',  # Setting a custom field for the job
    #         'state': 'pending',  # Set the job state (e.g., pending)
    #         'priority': 1,  # Set the priority of the job (Optional)
    #     })
    #
    #     print(f"Queue job created")
