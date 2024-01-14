odoo.define('darb_custom_lead.leadsMenu', function (require) {
    "use strict";
    
    var core = require('web.core');
    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    
    var LeadMenu = Widget.extend({
        name: 'lead_menu',
        template:'darb_custom_lead.leadMenu',
        events: {
            'show.bs.dropdown': '_onLeadMenuShow',
        },
        willStart: function () {
            return $.when(this.call('mail_service', 'isReady'));
        },
        start: function () {
            this._$leadsPreview = this.$('.o_mail_systray_dropdown_items');
            this._updateLeadPreview();
            return this._super();
        },
    
        /**
         * Make RPC and get current user's leads details
         * @private
         */
        _getLeadData: function () {
            var self = this;
    
            return self._rpc({
                model: 'res.users',
                method: 'systray_get_user_leads',
                args: [],
            }).then(function (data) {
           
                self._leads = data;
                self.leadCounter = data.total_count || 0;
                self.$('.o_notification_counter').text(self.leadCounter);
                self.$el.toggleClass('o_no_notification', !self.leadCounter);
            });
        },
        /**
         * @private
         */
        _updateLeadPreview: function () {
            var self = this;
            self._getLeadData().then(function (){
                self._$leadsPreview.html(QWeb.render('darb_custom_lead.systray.LeadMenu.Previews', {
                    leads : self._leads
                }));
            });
        },

        /**
         * @private
         */
        _onLeadMenuShow: function () {
             this._updateLeadPreview();
        },
    });
    
    SystrayMenu.Items.push(LeadMenu);
    
    return LeadMenu;
    
    });