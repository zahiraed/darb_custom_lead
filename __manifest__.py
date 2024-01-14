# -*- coding: utf-8 -*-
{
    'name': "darb_custom_lead",

    'summary': """
        Qualify leads,
        Link lead to existing customer""",

    'description': """
            Add information for which the customer must be contacted , but without crezting an opportunity
    """,

    'author': "ED-DENDANE ZAHIRA",
    'website': "",
    'category': 'CRM',
    'version': '12.0.7.4',

    'depends': ['crm', 'mail', 'base', 'portal'],

    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_views_inherit.xml',
        'views/res_partner_views_inherit.xml',
        'wizard/lead_define_date_wizard_view.xml',
        'wizard/crm_lead_wizard_view.xml',
        'wizard/lead_next_action_wizard_view.xml',
        'views/crm_menuitems.xml',
        'report/overdue_action_template.xml',
        'report/overdue_actions_report.xml',
        'views/lead_portal_templates.xml',
        'views/assets_backend_inherit.xml'
    ],

    'qweb': ['static/src/xml/systray_lead.xml'],

    'installable': True,
    'application': False

}
