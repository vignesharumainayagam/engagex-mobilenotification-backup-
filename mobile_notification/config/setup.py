from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Mobile App Notification"),
			"items": [
				{
					"type": "doctype",
					"name": "App Notification Center"
				},
				{
					"type": "doctype",
					"name": "App Notification Settings"
				},			
			]
		},		
	] 

	



