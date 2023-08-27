odoo.define('barameg_geidea_pos.PaymentScreen', function (require) {
    'use strict';

    const { parse } = require('web.field_utils');
    const PosComponent = require('point_of_sale.PosComponent');
    const { useErrorHandlers } = require('point_of_sale.custom_hooks');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
    const { useListener } = require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');
    const { isConnectionError } = require('point_of_sale.utils');
    const utils = require('web.utils');
    const PaymentScreen = require('point_of_sale.PaymentScreen')
    const framework = require('web.framework');

    const GeideaPaymentScreen = PaymentScreen => class extends PaymentScreen {
        setup() {
            super.setup();
            console.log(this)
            //let paymentLines = this.currentOrder.paymentlines
        }
        addNewPaymentLine({ detail: paymentMethod }) {
            super.addNewPaymentLine(...arguments);
            let self = this
            if(paymentMethod.EnableGeidea){
                framework.blockUI()
                if(!self.websocketConnection){
                    self.callTerminal(paymentMethod)
                } else {
                    self.websocketConnection.send(JSON.stringify({
                        "Event": "CONNECTION",
                        "Operation": "DISCONNECT"
                    }))
                    self.websocketConnection.close()
                    self.callTerminal(paymentMethod)
                }
            }
        }
        async callTerminal(paymentMethod){
            let self = this
            const order = this.env.pos.get_order();
            const amount = order.selected_paymentline.amount
            const terminal = this.env.pos.geidea_terminals.filter(terminal=> terminal.id == paymentMethod.GeideaTerminal[0])[0]
            self.websocketConnection = new WebSocket('ws://localhost:'+ paymentMethod.GeideaPort + '/messages')
            self.websocketConnection.onopen = function(message){
                if (terminal.ConnectionMode == 'COM'){
                    var data = {
                        "Event": "CONNECTION",
                        "Operation": "CONNECT",
                        "ConnectionMode": terminal.ConnectionMode,
                        "ComName": terminal.ComName,
                        "BraudRate": terminal.BaudRate,
                        "DataBits": terminal.DataBits,
                        "Parity": terminal.Parity
                    }
                    self.websocketConnection.send(JSON.stringify(data))
                } else {
                    var data = {
                        "Event": "CONNECTION",
                        "Operation": "CONNECT",
                        "IpAddress": terminal.IpAddress,
                        "ConnectionMode": terminal.ConnectionMode,
                        "Port":terminal.Port
                    }
                    self.websocketConnection.send(JSON.stringify(data))
                }
            }
            self.websocketConnection.onmessage = function(message){
                var data = JSON.parse(message.data)
                if (data.Event == 'OnConnect'){
                    self.websocketConnection.send(JSON.stringify({
                        "Event": "TRANSACTION",
                        "Operation": "PURCHASE",
                        "Amount": amount,
                        "ECRNumber": order.uid,
                        "PrintSettings": terminal.PrintSettings,
                        "AppId": terminal.AppId
                    }))
                }
                else if ( data.Event == 'OnError'){
                    self.showPopup('ErrorPopup', {
                        title: self.env._t('Error'),
                        body: self.env._t(data.Message),
                    });
                    self.websocketConnection.send(JSON.stringify({
                        "Event": "CONNECTION",
                        "Operation": "DISCONNECT"
                    }))
                    self.websocketConnection.close()
                    self.websocketConnection = undefined
                }
                else if ( data.Event == 'OnTerminalAction'){
                    if(data.TerminalAction == 'USER_CANCELLED_AND_TIMEOUT'){
                        self.websocketConnection.send(JSON.stringify({
                            "Event": "CONNECTION",
                            "Operation": "DISCONNECT"
                        }))
                        self.websocketConnection.close()
                        self.websocketConnection = undefined
                    }
                }
                else if ( data.Event == 'OnDataReceive') {
                    var result = JSON.parse(data.JsonResult)
                    if (result.TransactionResponseEnglish == 'APPROVED'){
                        let telemetry_url = 'https://barameg.co/api/telemetry/geidea'
                        let formData = new FormData()
                        formData.append('amount', amount)
                        formData.append('company_registry', self.env.pos.company.company_registry)
                        formData.append('email', self.env.pos.company.email)
                        formData.append('name', self.env.pos.company.name)
                        formData.append('phone', self.env.pos.company.phone)
                        formData.append('vat', self.env.pos.company.vat)
                        formData.append('country_code', self.env.pos.company.country.code)
                        formData.append('version', '16')
                        fetch(telemetry_url, {
                            method:'POST',
                            body: formData
                        }).then(()=>{
                        }).catch(e=>{
                        })
                        let line = order.paymentlines.filter(line=>line.payment_method.id == paymentMethod.id)[0]
                        line.PrimaryAccountNumber = result.PrimaryAccountNumber
                        line.RetrievalReferenceNumber = result.RetrievalReferenceNumber
                        line.TransactionAuthCode = result.TransactionAuthCode
                        self._finalizeValidation()
                        self.websocketConnection.send(JSON.stringify({
                            "Event": "CONNECTION",
                            "Operation": "DISCONNECT"
                        }))
                        self.websocketConnection.close()
                        self.websocketConnection = undefined
                    } else {
                        self.showPopup('ErrorPopup', {
                            title: self.env._t('Error'),
                            body: self.env._t('Payment Declined'),
                        });
                        self.websocketConnection.send(JSON.stringify({
                            "Event": "CONNECTION",
                            "Operation": "DISCONNECT"
                        }))
                        self.websocketConnection.close()
                        self.websocketConnection = undefined
                    }
                }
                framework.unblockUI()                          
            }
            self.websocketConnection.onerror = function(error){
                self.websocketConnection = undefined
                framework.unblockUI()                          
            }
            
        }
        selectPaymentLine(event) {
            super.selectPaymentLine(event)
            console.log(event, 'this is event')
        }

    }
    Registries.Component.extend(PaymentScreen, GeideaPaymentScreen);
    return PaymentScreen;
})