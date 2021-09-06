# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError,ValidationError

class purchase_approval(models.Model):
    _inherit = "purchase.order"


    @api.multi
    def request_approval_(self):
        # to resend the notification for approval
        for order in self:
            order.send_notification()
            
    @api.multi
    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()
            if order.required_approval() and self.env.user not in order.approvers():
                order.write({'state':'to approve'})
                order.send_notification()
            else:
                order.write({'state':'purchase'})
        return True
    
    def approvers(self):
        # this function returns list of valid approvers 
        temp = self.env['ir.config_parameter'].sudo().get_param('purchase_approval.purchase_order_approvers') or False
        record = temp.strip('[').strip(']').split(',')
        users=self.env['res.users'].browse([int(x) for x in record])
        return users
    
    def send_notification(self):
        # post message in chatter + create notification
        for user in self.approvers():
            notification_ids = [(0,0,{
                'res_partner_id': user.partner_id.id,
                'notification_type': 'inbox'
            })]
            self.message_post(
                body = 'Dear Purchase Order <a href="#id='+str(self.id)+'&model=purchase.order">' + self.name + '</a> is waiting for approval',
                message_type = "notification",
                subtype="mail.mt_comment",
                author_id = self.env.user.partner_id.id,
                notification_ids=notification_ids)

            
    @api.one
    def button_approve(self):
        if self.env.user in self.approvers():
            self.write({'state': 'purchase'})
        else:
            raise ValidationError("Unauthorised to approve order,please request Approval")
            
    def required_approval(self):
        # simpler implimentation of approval requirement
        order = self
        if order.amount_total > self.env.user.company_id.currency_id._convert(
                            order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()):  
            return True
        return False