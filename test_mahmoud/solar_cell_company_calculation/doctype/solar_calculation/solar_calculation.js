// Copyright (c) 2025, company to determine the Return on Investment (ROI) for clients switching to solar and contributors
// For license information, please see license.txt

frappe.ui.form.on("Solar Calculation", {
	refresh: function(frm) {
        frm.add_custom_button(__('Calculate'), function() {
            frm.call('calculate_averages').then(() => {
                frm.reload_doc()
            });
        });
        
        // Restrict edit access for accounting team
        if (frappe.user.has_role('Accounts User') && !frappe.user.has_role('Sales User')) {
            frm.set_read_only();
        }
    },
    before_save: function(frm) {
        // Validate consumption data
        if (frm.doc.consumption_data && frm.doc.consumption_data.length > 0) {
            frm.doc.consumption_data.forEach(row => {
                if (!row.timestamp || row.kw < 0 || row.kwh < 0) {
                    frappe.throw('Invalid consumption data: Ensure all timestamps are set and KW/KWH are non-negative');
                }
            });
        }
    },
});
