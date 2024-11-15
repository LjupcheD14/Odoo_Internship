odoo.define("wb_pos.WBSampleButton", function (require) {
    const PosComponent = require("point_of_sale.PosComponent");  // Corrected 'PosComponent'
    const ProductScreen = require("point_of_sale.ProductScreen");  // Corrected 'ProductScreen'
    const Registries = require("point_of_sale.Registries");

    const {useListener} = require("@web/core/utils/hooks");

    class WBSampleButton extends PosComponent {
        // Define functionality, e.g., a button click handler

        setup() {
            super.setup();
            useListener("click", this.wb_sample_button_click);
        }

        wb_sample_button_click() {
            console.log("WB Sample Button clicked!");
        }

        // handleClick() {
        //     console.log("WB Sample Button clicked!");
        // }
    }

    WBSampleButton.template = "WBSampleButton";  // Associate the template

    // Add the button to the ProductScreen
    ProductScreen.addControlButton({
        component: WBSampleButton,
        position: ["before", "OrderlineCustomerNotaButton"],  // Ensure this button exists in the product screen
    });

    // Register the component
    Registries.Component.add(WBSampleButton);

    return WBSampleButton;
});


// odoo.define('pos_custom_button.CustomButton', function (require) {
//     "use strict";
//     const PosComponent = require('point_of_sale.PosComponent');
//     const Registries = require('point_of_sale.Registries');
//
//     class CustomButton extends PosComponent {
//         async onClick() {
//             // Action triggered when button is clicked
//             alert('Custom Button Clicked!');
//         }
//     }
//
//     CustomButton.template = 'CustomButton';
//     Registries.Component.add(CustomButton);
//     return CustomButton;
// });

// odoo.define('your_module.pos_custom_button', function (require) {
//     const PosComponent = require('point_of_sale.PosComponent');
//     const ProductScreen = require('point_of_sale.ProductScreen');
//     const Registries = require('point_of_sale.Registries');
//
//     // Custom Button Component
//     class CustomButton extends PosComponent {
//         // Function triggered when button is clicked
//         handleClick() {
//             alert('Custom POS Button Clicked!');
//             // You can add your custom logic here
//         }
//     }
//
//     // Associate the button with a template
//     CustomButton.template = 'CustomButtonTemplate';
//
//     // Add the button to the Product Screen (or any other screen)
//     ProductScreen.addControlButton({
//         component: CustomButton,
//         position: ['before', 'OrderlineCustomerNotaButton'],  // Position relative to an existing button
//     });
//
//     // Register the button so it is available in the POS system
//     Registries.Component.add(CustomButton);
//
//     return CustomButton;
// });
