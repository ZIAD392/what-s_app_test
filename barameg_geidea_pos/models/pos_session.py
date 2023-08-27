# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_pos_payment_method(self):
        print('_loader_params_pos_payment_method')
        result = super(PosSession, self)._loader_params_pos_payment_method()
        result['search_params']['fields'].append('EnableGeidea')
        result['search_params']['fields'].append('GeideaPort')
        result['search_params']['fields'].append('GeideaTerminal')
        return result

    def _loader_params_pos_payment(self):
        print("_loader_params_pos_payment")
        result = super(PosSession, self)._loader_params_pos_payment()
        result['search_params']['fields'].append('PrimaryAccountNumber')
        result['search_params']['fields'].append('RetrievalReferenceNumber')
        result['search_params']['fields'].append('TransactionAuthCode')
        return result

    def _loader_params_geidea_terminals(self):
        return {'search_params': {'domain': [], 'fields': ['name']}}

    def _get_pos_ui_geidea_terminals(self, params):
        return self.env['geidea.terminals'].search_read(**params['search_params'])

    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        result.append('geidea.terminals')
        return result

    def _pos_data_process(self, loaded_data):
        loaded_data['geidea_terminals'] = self.env['geidea.terminals'].search_read([],[])
        super()._pos_data_process(loaded_data)
