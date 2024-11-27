# Copyright (C) 2024 WeSolved BV <https://wesolved.com>
# @author X X <xx@wesolved.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Custom Sales Report",
    "summary": "This module adds a custom PDF report for sales orders",
    "version": "18.0",
    "author": "WeSolved BV",
    "category": "Sales",
    "website": "https://www.wesolved.com",
    "license": "AGPL-3",
    "summary": "Individual project: Added a button to update product in product template",
    "depends": ["sale", "web"],
    "data": [
        "report/custom_sales_report.xml",
        "views/sale_order_view.xml",
    ],
    "assets": {
        "web.assets_qweb": [
            "ws_custom_sales_report/static/src/css/report_styles.css",  # Reference to your CSS file
        ],
    },
    "installable": True,
    "application": False,
}
