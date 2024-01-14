from odoo import models, fields, api,_

from odoo.exceptions import UserError

class LeadDefineDateWizard(models.TransientModel):
    
    _name = 'lead.define.date'
    _description = ' Lead date action Wizard'
    
    
    
    date = fields.Date(string="Date", required=True) # next action date of lead
  
    # next action date  button action
    def define_next_date(self):
        
        lead_id = self.env.context.get('lead_id')
        
        lead = self.env['crm.lead'].browse(lead_id)
        
        lead.write({'reminder_date':self.date})

        return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'crm.lead',
                'view_id': self.env.ref('crm.crm_case_tree_view_leads').id,
                'res_id': lead.id,
       }

    

    

    
    