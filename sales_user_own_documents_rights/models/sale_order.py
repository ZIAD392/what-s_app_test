from odoo import models, fields, _, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_sales_man = fields.Boolean(compute='_compute_is_sales_man')

    @api.onchange("order_line")
    def _compute_is_sales_man(self):
        for rec in self:
            if self.env.user.has_group('sales_team.group_sale_salesman') and not (
            self.env.user.has_group('sales_team.group_sale_salesman_all_leads')):
                rec.is_sales_man = False
            else:
                rec.is_sales_man = True


class CustomStockPicking(models.Model):
    _inherit = 'stock.picking'
    is_coordinator = fields.Boolean(compute='_compute_is_coordinator')

    @api.depends('user_id.groups_id')
    def _compute_is_coordinator(self):
        coordinator_group = self.env.ref('sales_user_own_documents_rights.group_stock_project_coordinator')
        for record in self:
            record.is_coordinator = coordinator_group in record.user_id.groups_id
