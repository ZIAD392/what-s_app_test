odoo.define('barameg_geidea_pos.models', function (require) {
    "use strict";

    const { PosGlobalState, Order, Orderline, Payment } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    const { uuidv4 } = require('point_of_sale.utils');
    const core = require('web.core');
    const Printer = require('point_of_sale.Printer').Printer;
    const { batched } = require('point_of_sale.utils')
    const QWeb = core.qweb;

    const TIMEOUT = 7500;

    const GeideaState = (PosGlobalState) => class GeideaState extends PosGlobalState {
        async _processData(loadedData) {
            await super._processData(...arguments);
            this.geidea_terminals = loadedData['geidea_terminals']
        }
    }
    Registries.Model.extend(PosGlobalState, GeideaState);

    const GeideaPayment = (Payment) => class GeideaPayment extends Payment {
        constructor(obj, options) {
            super(...arguments);
            this.PrimaryAccountNumber = this.PrimaryAccountNumber || null;
            this.RetrievalReferenceNumber = this.RetrievalReferenceNumber || null;
            this.TransactionAuthCode = this.TransactionAuthCode || null;
        }
        //@override
        export_as_JSON() {
            const json = super.export_as_JSON(...arguments);
            json.PrimaryAccountNumber = this.PrimaryAccountNumber;
            json.RetrievalReferenceNumber = this.RetrievalReferenceNumber;
            json.TransactionAuthCode = this.TransactionAuthCode;
            return json;
        }
        //@override
        init_from_JSON(json) {
            super.init_from_JSON(...arguments);
            this.PrimaryAccountNumber = json.PrimaryAccountNumber;
            this.RetrievalReferenceNumber = json.RetrievalReferenceNumber;
            this.TransactionAuthCode = json.TransactionAuthCode;
        }
    }
    Registries.Model.extend(Payment, GeideaPayment);

});
