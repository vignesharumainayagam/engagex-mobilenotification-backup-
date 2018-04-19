# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
import frappe.utils
from frappe.utils.oauth import get_oauth2_authorize_url, get_oauth_keys, login_via_oauth2, login_via_oauth2_id_token, login_oauth_user as _login_oauth_user, redirect_post_login
import json
from frappe import _
from frappe.auth import LoginManager
from frappe.integrations.doctype.ldap_settings.ldap_settings import get_ldap_settings
from frappe.utils.password import get_decrypted_password
from frappe.utils.html_utils import get_icon_html

no_cache = True

def get_context(context):
	if frappe.session.user != "Guest" and frappe.session.data.user_type=="System User":
		frappe.local.flags.redirect_location = "/adsdasd"
		raise frappe.Redirect

	# get settings from site config
	context.no_header = True
	context.for_test = 'login.html'
	context["title"] = "Login"
	context["provider_logins"] = []
	context["disable_signup"] = frappe.utils.cint(frappe.db.get_value("Website Settings", "Website Settings", "disable_signup"))
	providers = [i.name for i in frappe.get_all("Social Login Key", filters={"enable_social_login":1})]
	for provider in providers:
		client_id, base_url = frappe.get_value("Social Login Key", provider, ["client_id", "base_url"])
		client_secret = get_decrypted_password("Social Login Key", provider, "client_secret")
		icon = get_icon_html(frappe.get_value("Social Login Key", provider, "icon"), small=True)
		if (get_oauth_keys(provider) and client_secret and client_id and base_url):
			context.provider_logins.append({
				"name": provider,
				"provider_name": frappe.get_value("Social Login Key", provider, "provider_name"),
				"auth_url": get_oauth2_authorize_url(provider),
				"icon": icon
			})
			context["social_login"] = True

	ldap_settings = get_ldap_settings()
	context["ldap_settings"] = ldap_settings

	login_name_placeholder = [_("Email address")]

	if frappe.utils.cint(frappe.get_system_settings("allow_login_using_mobile_number")):
		login_name_placeholder.append(_("Mobile number"))

	if frappe.utils.cint(frappe.get_system_settings("allow_login_using_user_name")):
		login_name_placeholder.append(_("Username"))

	context['login_name_placeholder'] = ' {0} '.format(_('or')).join(login_name_placeholder)

	return context
