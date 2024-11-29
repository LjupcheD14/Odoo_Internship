from odoo import models, fields, api

import random
import string


class JobQueue(models.Model):
    _inherit = "queue.job"

    model_name = fields.Char(string="Model Name", store=True)
    name = fields.Char(string="Job Name", store=True)

    @api.model
    def create(self, vals):
        # Get the product name from context
        order_name = self.env.context.get("order_name", "Default Order Name")

        # Use the product_name in the job creation logic
        vals["name"] = f"Job for: {order_name}"  # Dynamic value
        vals["model_name"] = "Sale Order Template"  # Static value

        return super(JobQueue, self).create(vals)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_urgent = fields.Boolean(string="Urgent", default=False)

    def action_enqueue_job(self):
        print("I am clicked")

        self = self.with_context(order_name=self.name)

        self.with_delay().update_order_job()

    def update_order_job(self):
        pass
