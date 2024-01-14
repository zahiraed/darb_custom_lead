from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
import datetime

#inherit from customer portal controller in order to add leads in menu
class CustomerPortalInherit(CustomerPortal):

    def _prepare_portal_layout_values(self):
        # override Prepare portal layout values function
        values = super(CustomerPortalInherit,
                       self)._prepare_portal_layout_values()
        # get overdue actions
        action_ids = request.env['mail.activity'].search(
            [('date_deadline', '<', datetime.date.today())])
        res_ids = [action.res_id for action in action_ids]
        # get count of leads that have overdue actions
        domain = [('type', '=', 'lead'), ('id', 'in', res_ids)]
        values['lead_count'] = request.env['crm.lead'].search_count(domain)

        return values

    def _lead_get_page_view_values(self, lead, access_token, **kwargs):
        values = {
            'page_name': 'lead',
            'lead': lead,
        }

        return self._get_page_view_values(lead, access_token, values, 'my_leads_history', False, **kwargs)

    # Add route to access to leads list
    @http.route(['/my/leads', '/my/leads/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_leads(self, page=1, sortby=None, **kw):

        values = self._prepare_portal_layout_values()
        CrmLead = request.env['crm.lead']
        # get overdue actions
        action_ids = request.env['mail.activity'].search(
            [('date_deadline', '<', datetime.date.today())])
        res_ids = [action.res_id for action in action_ids]
        domain = [('type', '=', 'lead'), ('id', 'in', res_ids)]

        # searchbar sorting
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }
        # default sortby order
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        archive_groups = self._get_archive_groups('crm.lead', domain)

        # leads count
        lead_count = CrmLead.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/leads",
            url_args={'sortby': sortby},
            total=lead_count,
            page=page,
            step=self._items_per_page
        )

        leads = CrmLead.search(
            domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_leads_history'] = leads.ids[:100]

        values.update({
            'leads': leads,
            'page_name': 'lead',
            'archive_groups': archive_groups,
            'default_url': '/my/leads',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })

        return request.render("darb_custom_lead.portal_my_leads", values)
