# Copyright (C) 2024 WeSolved BV <https://wesolved.com>
# @author X X <xx@wesolved.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Urgent Custom Module",
    "version": "18.0",
    "author": "WeSolved BV",
    "category": "Sales",
    "website": "https://www.wesolved.com",
    "license": "AGPL-3",
    "summary": "Individual project: Added a button to update product in product template",
    "depends": ["base", "sale", "mail"],
    "data": [
        "views/urgent_view.xml",
        "views/urgent_list_view.xml",
        "views/urgent_kanban_view.xml",
        "views/urgent_filter_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "ws_urgent/static/src/js/urgent_filter.js",  # Include JS file here
        ],
    },
    "installable": True,
    "application": False,
}
