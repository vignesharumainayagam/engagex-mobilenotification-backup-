// Copyright (c) 2018, Tridots Tech and contributors
// For license information, please see license.txt

frappe.ui.form.on('App Notification Center', {
	refresh: function(frm) {
		frappe.breadcrumbs.add("Setup");
	},
	create_receiver_list: function (frm) {


     },
     send_notification: function(frm) {

               console.log(frm.doc.receiver_list.split("\n"))
               var a = frm.doc.receiver_list.split("\n");
               var b = a.filter(function(v){return v!==''});
               console.log(b)
                    frappe.call({
                    "method": "frappe.client.get",
                    args: {
                         doctype: "App Notification Settings",
                    },
                    callback: function (r) {


                         var receiver = frm.doc.receiver_list.split("\n");     

                         var one_signal_userconfig = { 
                              headers: { 
                                   'Content-Type': 'application/json', 
                                   "Authorization": "Basic "+ r.message.secret_key 
                              } 
                         }; 
                         var info = {}; 

                         var user_notification_data = { 
                              "app_id": r.message.app_id, 
                              "contents": { "en": frm.doc.content_data }, 
                              "data": {"add_data":frm.doc.message},
                              "include_player_ids": b
                         } 
                         $.post(r.message.notification_gateway_url, user_notification_data, one_signal_userconfig).done(function(e) { console.log(e); });


                    }
               });

	},

     
});
