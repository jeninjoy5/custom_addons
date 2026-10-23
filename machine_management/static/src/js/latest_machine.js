/** @odoo-module */
import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
console.log("yes");
publicWidget.registry.get_product_tab = publicWidget.Widget.extend({
    selector : '.machine_section',
    async willStart() {
        const result = await rpc('/get_machines', {});
        console.log(result);
        if(result){
            this.$target.empty().html(renderToElement('machine_management.machine_data', {result: result}))
        }
    },
});
