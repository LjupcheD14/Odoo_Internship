from odoo import models

import xlsxwriter
import csv
import io
import base64
import json


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_print_custom_report(self):
        """Button action to trigger the PDF report"""
        return self.env.ref(
            "ws_custom_sales_report.custom_sales_report_action"
        ).report_action(self)

    def action_export_custom_excel(self):
        """Button action to trigger the Excel export"""
        # Create an in-memory file
        output = io.BytesIO()

        # Create an Excel workbook and a worksheet
        workbook = xlsxwriter.Workbook(output)
        sheet = workbook.add_worksheet("Sale Orders")

        # Define a bold format for headers
        bold = workbook.add_format({"bold": True})

        # Write headers to the Excel file
        sheet.write(0, 0, "Order Name", bold)
        sheet.write(0, 1, "Customer", bold)
        sheet.write(0, 2, "Order Date", bold)
        sheet.write(0, 3, "Total Amount", bold)

        # Fetch the sale order data (you can adjust the domain or fields as needed)
        orders = self.search([("id", "=", self.id)])

        # Write data to Excel for each sale order
        row = 1
        for order in orders:
            sheet.write(row, 0, order.name)
            sheet.write(row, 1, order.partner_id.name)
            sheet.write(
                row,
                2,
                order.date_order.strftime("%Y-%m-%d") if order.date_order else "",
            )
            sheet.write(row, 3, order.amount_total)
            row += 1

        # Close the workbook (this saves the file in memory)
        workbook.close()

        # Move the cursor to the beginning of the file so it can be read
        output.seek(0)

        # Base64 encode the binary data of the Excel file
        file_data = base64.b64encode(output.getvalue()).decode("utf-8")

        # Create the attachment
        attachment = self.env["ir.attachment"].create(
            {
                "name": "sale_order_excel_report.xlsx",
                "type": "binary",
                "datas": file_data,
                "res_model": "sale.order",
                "res_id": self.id,
                "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            }
        )

        # Return the URL to the attachment
        return {
            "type": "ir.actions.act_url",
            "url": "/web/content/%d?download=true" % attachment.id,
            "target": "new",
        }

    def action_export_custom_csv(self):
        """Button action to trigger the CSV export"""
        # Create an in-memory file for CSV
        output = io.StringIO()

        # Create a CSV writer
        writer = csv.writer(output)

        # Write the header row
        writer.writerow(["Order Name", "Customer", "Order Date", "Total Amount"])

        # Fetch the sale order data (you can adjust the domain or fields as needed)
        orders = self.search([("id", "=", self.id)])

        # Write data rows for each sale order
        for order in orders:
            writer.writerow(
                [
                    order.name,
                    order.partner_id.name,
                    order.date_order.strftime("%Y-%m-%d") if order.date_order else "",
                    order.amount_total,
                ]
            )

        # Get the CSV content as string
        file_data = output.getvalue()

        # Base64 encode the CSV data
        file_data_base64 = base64.b64encode(file_data.encode("utf-8")).decode("utf-8")

        # Create the attachment
        attachment = self.env["ir.attachment"].create(
            {
                "name": "sale_order_csv_report.csv",
                "type": "binary",
                "datas": file_data_base64,
                "res_model": "sale.order",
                "res_id": self.id,
                "mimetype": "text/csv",
            }
        )

        # Return the URL to the attachment
        return {
            "type": "ir.actions.act_url",
            "url": "/web/content/%d?download=true" % attachment.id,
            "target": "new",
        }

    def action_export_custom_json(self):
        """Button action to trigger the JSON export"""
        # Fetch sale order data
        orders = self.search([("id", "=", self.id)])

        # Prepare data to be serialized into JSON
        order_data = []
        for order in orders:
            data = {
                "order_name": order.name,
                "customer": order.partner_id.name,
                "order_date": (
                    order.date_order.strftime("%Y-%m-%d") if order.date_order else ""
                ),
                "total_amount": order.amount_total,
                "order_lines": [],
            }
            # Add line items
            for line in order.order_line:
                data["order_lines"].append(
                    {
                        "product_name": line.product_id.name,
                        "quantity": line.product_uom_qty,
                        "unit_price": line.price_unit,
                        "line_total": line.price_subtotal,
                    }
                )
            order_data.append(data)

        # Convert Python dictionary to JSON string
        json_content = json.dumps(order_data, indent=4)

        # Create an in-memory file (StringIO)
        file_data = io.BytesIO(json_content.encode("utf-8"))

        # Base64 encode the file content
        file_data_base64 = base64.b64encode(file_data.getvalue()).decode("utf-8")

        # Create an attachment for the JSON file
        attachment = self.env["ir.attachment"].create(
            {
                "name": "sale_order_json_report.json",
                "type": "binary",
                "datas": file_data_base64,
                "res_model": "sale.order",
                "res_id": self.id,
                "mimetype": "application/json",
            }
        )

        # Return the URL for the file to be downloaded
        return {
            "type": "ir.actions.act_url",
            "url": "/web/content/%d?download=true" % attachment.id,
            "target": "new",
        }
