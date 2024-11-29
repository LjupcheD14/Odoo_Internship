from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_urgent = fields.Boolean(string="Urgent", default=False)

    def action_mark_as_urgent(self):
        # Mark the order as urgent
        self.write({"is_urgent": True})

        # Send an email using the custom email template
        for order in self:
            # Ensure the order is confirmed before sending the confirmation email
            if order.state == "sale":  # Order must be in 'Sale' state (confirmed)
                template = self.env.ref(
                    "sale.email_template_edi_sale"
                )  # Default order confirmation template
                template.send_mail(order.id, force_send=True)

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
