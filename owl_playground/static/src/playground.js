/** @odoo-module **/

import { Component } from "@odoo/owl";

export class Playground extends Component {
    static template = "owl_playground.playground";
}
owl.Component.mount(Playground, document.body);
