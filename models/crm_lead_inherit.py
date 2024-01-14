from odoo import models, fields, api,_


class CrmLeadInherit(models.Model):
    _inherit = 'crm.lead'

    reminder_date = fields.Date(string='Reminder date')  # next action date

   # create onchange partner name function that check if customer already exist and fill contact title automatically
    @api.onchange('partner_name')
    def onchange_partner_name(self):
        partner_obj = self.env['res.partner']
        if self.partner_name:
            partner_id = partner_obj.search(
                [('name', 'ilike', self.partner_name)], limit=1)

            if partner_id:
                child_id = partner_obj.search(
                    [('parent_id', '=', partner_id.id)], limit=1)
                if child_id:
                    self.update({'contact_name': child_id.name,
                                 'title': child_id.title.id if child_id.title.id else False})
                    
    
    # schedule next action based on reminder date               
    def schedule_next_action(self):
             return {
                'name': _('Next action'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'next.action.wizard',
                'view_id': self.env.ref('darb_custom_lead.lead_next_action_form_wizard').id,
                'type': 'ir.actions.act_window',
                'context': {'reminder_date':self.reminder_date,
                            'lead_id':self.id},
                'target': 'new'
            } 


    #call qweb report template in order to print  overdue actions 
    @api.multi
    def overdue_actions_print(self):
        
        return self.env.ref('darb_custom_lead.report_overdue_actions').report_action(self)