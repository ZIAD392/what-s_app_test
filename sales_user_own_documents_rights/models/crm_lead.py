from odoo import models, fields, _, api
from odoo.exceptions import ValidationError


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    is_sales_man = fields.Boolean(compute='_compute_is_sales_man')

    def _compute_is_sales_man(self):
        for rec in self:
            if self.env.user.has_group('sales_team.group_sale_salesman') and not self.env.user.has_group('sales_team.group_sale_salesman_all_leads'):
                rec.is_sales_man = True
            else:
                rec.is_sales_man = False

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        if self.env.user.has_group('sales_team.group_sale_salesman') and not self.env.user.has_group('sales_team.group_sale_salesman_all_leads'):
            raise ValidationError(_("You are not allowed to change stage"))

