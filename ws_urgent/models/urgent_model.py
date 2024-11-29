from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_urgent = fields.Boolean(string="Urgent", default=False)

    def action_mark_as_urgent(self):
        self.write({"is_urgent": True})
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Success",
                "message": "This order has been marked as urgent!",
                "type": "success",
            },
        }

    def action_mark_as_not_urgent(self):
        self.write({"is_urgent": False})
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Success",
                "message": "This order is no longer urgent.",
                "type": "success",
            },
        }
