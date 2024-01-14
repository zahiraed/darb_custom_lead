from odoo import models, fields, api,_

from odoo.exceptions import UserError

class CrmLeadWizard(models.TransientModel):
    
    _name = 'crm.lead.wizard'
    _description = 'CRM Lead Wizard'
    
    
    
    name = fields.Char(string="Name", required=True) # name of the lead
    partner_id = fields.Many2one('res.partner',string="Customer") #Customer
    contact_name = fields.Char(string="Contact name") # contact of selected customer
    company_name = fields.Char(string="Company name") # company name of customer
    email = fields.Char(string="Email") # email
    phone = fields.Char(string="Phone") # phone
    title_id = fields.Many2one('res.partner.title',string="Title") #title of contact
    user_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user) # salesperson
    team_id = fields.Many2one('crm.team', string="Sales Team") # team of salesperson
    
    
    # create onchange function that when customer is identfied, it fill contact company and title
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            contact_name = self.partner_id.child_ids[0]['name'] if self.partner_id.is_company else self.partner_id.name
            title_id = self.partner_id.child_ids[0].title.id if self.partner_id.is_company else self.partner_id.title.id
            company_name = self.partner_id.name
            self.update({
                        'contact_name':contact_name,
                        'title_id':title_id,
                        'company_name':company_name,
                        })
 
 
    # create new lead button action
    def create_new_lead(self):
        crm_obj = self.env['crm.lead']
        
        data_to_create = {'name':self.name, 'partner_id':self.partner_id.id,
                          'contact_name':self.contact_name,'title_id':self.title_id.id,
                          'company_name':self.company_name, 'email_from':self.email,
                          'phone':self.phone,'user_id':self.user_id.id,
                          'team_id':self.team_id.id,'type':'lead'
                          } 
        
        #create new lead with given data
        lead_id = crm_obj.create(data_to_create)
        
        if lead_id:
            return {
                'name': _('Next action date'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'lead.define.date',
                'view_id': self.env.ref('darb_custom_lead.lead_define_date_form_wizard').id,
                'type': 'ir.actions.act_window',
                'context': {'lead_id':lead_id.id},
                'target': 'new'
            } 
    

    

    
    