import {Component, useState} from "../../../../addons/web/static/lib/hoot/tests/hoot-owl-module";

export class Counter extends Component {
    static template = "my_module.Counter";

    setup() {
        this.state = useState({value: 0});
    }

    increment() {
        this.state.value++;
    }
}