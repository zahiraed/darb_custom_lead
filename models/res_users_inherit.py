
from odoo import models, fields, api, modules

class ResUsersInherit(models.Model):
    _inherit = 'res.users'
    
    #add systray get user leads to add user leads using SQL query 
    @api.model
    def systray_get_user_leads(self):
        
        query = """SELECT cl.id, count(*), cl.reminder_date,
                    CASE
                        WHEN %(today)s::date - reminder_date::date = 0 Then 'lead_today'
                        WHEN %(today)s::date - reminder_date::date > 0 Then 'lead_overdue'
                        WHEN %(today)s::date - reminder_date::date < 0 Then 'lead_planned'
                    END AS states
                    FROM crm_lead AS cl
                    WHERE cl.reminder_date IS NOT NULL and cl.type='lead'  
                    GROUP BY cl.id, states;
                    """

        self.env.cr.execute(query, {
            'today': fields.Date.context_today(self),
            'user_id': self.env.uid
        })
        
        user_leads = self.env.cr.dictfetchall()
        leads = {'name': 'darb_custom_lead',
                 'icon': modules.module.get_module_icon(self.env['crm.lead']._original_module),
                 'model': 'crm.lead',
                 'total_count':0 ,
                 'lead_today_count': 0,
                 'lead_overdue_count':0,
                 'lead_planned_count': 0
                }
        for lead in user_leads:
              leads['%s_count' % lead['states']] += lead['count']
              if lead['states'] in ('lead_today','lead_overdue'):
                        leads['total_count'] += lead['count']
              

        return leads