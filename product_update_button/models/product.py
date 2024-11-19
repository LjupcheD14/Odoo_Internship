from odoo import models, fields, api
from datetime import datetime
from addons.queue_job.job import Job


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Add any custom fields if needed
    is_storable = fields.Boolean(string="Is Storable?", default=True)

    # def action_enqueue_job(self):
    #     """
    #     Method to enqueue a background task to update product details.
    #     """
    #     for product in self:
    #         # Enqueue a background job to perform the update
    #         self.env['queue.job'].sudo().with_context(
    #             product_id=product.id
    #         ).requeue(self._update_product_job, product.id)
    #
    #     return True

    def action_enqueue_job(self):
        for product in self:
            product.with_delay().update_product_job()

    def update_product_job(self):
        self.write({'name': self.name + ' (Updated)'})

    # def action_update_product(self):
    #     """
    #     Method to update the product template with the required fields.
    #     This method is triggered by the button on the product form.
    #     """
    #     # Define the tax: create it if it doesn't exist
    #     tax = self.env.ref('account.tax_19', raise_if_not_found=False)
    #     if not tax:
    #         tax = self.env['account.tax'].create({
    #             'name': '19% VAT',
    #             'amount': 19.0,
    #             'type_tax_use': 'sale',  # It will apply to sales
    #             'amount_type': 'percent',
    #             'active': True,
    #             'company_id': self.env.company.id,
    #         })
    #
    #     # Loop through selected products and update them
    #     for product in self:
    #         # Set the current time and format it as a string
    #         current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #
    #         # Update the product fields
    #         product.write({
    #             'name': f"Product 1 {current_time}",
    #             'sale_description': f"This is the description after job run {current_time}",
    #             'list_price': 10.1,  # Sales price
    #         })
    #
    #         # Update the tax (if necessary, adjust your product's tax_ids field)
    #         if tax not in product.taxes_id:
    #             product.write({
    #                 'taxes_id': [(4, tax.id)],  # Add tax to product
    #             })
    #
    #     return True
