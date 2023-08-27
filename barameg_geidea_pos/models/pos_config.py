# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class PosConfig(models.Model):
    _inherit = 'pos.config'

    terminals = fields.One2many()