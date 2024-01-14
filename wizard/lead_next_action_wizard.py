from odoo import models, fields, api,_

from odoo.exceptions import UserError

class NextActionWizard(models.TransientModel):
    
    _name = 'next.action.wizard'
    _description = 'Next Action Wizard'
    
    
    
    activity_type_id = fields.Many2one('mail.activity.type', string="Action") #Activty type:mail,call,meeting
    date_deadline = fields.Date(string="Due date", default=lambda self: self.env.context.get('reminder_date'), readonly=True) # date deadline of action
   
   
    # add schedule action button 
    def schedule_action(self):
        act_obj = self.env['mail.activity']
        lead_id = self.env.context.get('lead_id')
        lead = self.env['crm.lead'].browse(lead_id)
        res_model_id = self.env['ir.model'].search([('model','=',lead._name)],limit=1)
        # raise UserError([res_model_id,lead._name])
        data_to_create = {'activity_type_id':self.activity_type_id.id,
                          'date_deadline':self.date_deadline,'res_model_id':res_model_id.id,
                          'user_id':self.env.user.id,'res_id':lead.id
                          } 
        
        #create new activity with given data
        act_obj.create(data_to_create)
        
        return {'type': 'ir.actions.act_window_close'}
        
       
    

    

    
    