# -*- coding: utf-8 -*-
from odoo import api, fields, models
from ast import literal_eval

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"


    def _get_company(self):
        domain = [('company_id', '=', self.env.user.company_id.id)]
        return domain
    
    purchase_order_approvers = fields.Many2many('res.users', string='Purchase Order Approvers',domain=_get_company)
    
    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('purchase_approval.purchase_order_approvers', self.purchase_order_approvers.ids)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        purchase_order_approvers = self.env['ir.config_parameter'].sudo().get_param('purchase_approval.purchase_order_approvers')
        if purchase_order_approvers:
            res.update(
                purchase_order_approvers=[(6, 0, literal_eval(purchase_order_approvers))],
            )
        return res
