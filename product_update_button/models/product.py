from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Add any custom fields if needed
    is_storable = fields.Boolean(string="Is Storable?", default=True)

    @api.model
    def action_update_quantity_on_hand(self):
        # Implement logic for updating product quantities
        # This is just an example placeholder for the logic
        pass

    @api.model
    def action_enqueue_job(self):
        # Add the logic you want for the action
        # For example, you can schedule a background job or update something
        # This could be a mockup implementation for testing
        print("Enqueuing job for product template")
        return True
