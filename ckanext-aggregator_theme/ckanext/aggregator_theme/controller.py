from pylons import config

import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.lib.app_globals as app_globals
import ckan.model as model
import ckan.logic as logic
import ckan.new_authz
import json
c = base.c
request = base.request
_ = base._

LICENSE_FILE = "/usr/lib/ckan/default/src/ckanext-aggregator_theme/ckanext/aggregator_theme/data/licenses.json"
FEATURED_FILE = "/usr/lib/ckan/default/src/ckanext-aggregator_theme/ckanext/aggregator_theme/data/featured.json"

class LicenseController(base.BaseController):


    #This restricts view of this page to sysadmins   
    def __before__(self, action, **params):
        super(LicenseController, self).__before__(action, **params)
        context = {'model': model,
                   'user': c.user, 'auth_user_obj': c.userobj}
        try:
            logic.check_access('sysadmin', context, {})
        except logic.NotAuthorized:
            base.abort(401, _('Need to be system administrator to administer'))
        c.revision_change_state_allowed = True

 
    def _get_form_items(self):
        
	# This is a list of items for the form. Pass these items into the form generator.
	# This is also used to iterate through the items in the form while building the license
	items = [
        	{'name': 'title', 'control': 'input', 'label': _('Title'), 'placeholder' : 'My License', 'is_required': 'is_required'},
      		{'name': 'maintainer', 'control': 'input', 'label': _('Maintainer'), 'placeholder' : 'My Licensing Body'},
      		{'name': 'url', 'control': 'input', 'label': _('URL'), 'placeholder' : 'http://www.mylicenseinfo.com'},
	      	{'name': 'family', 'control': 'input', 'label': _('Family')},
		{'name': 'status', 'control': 'checkbox', 'label': _('Active')},
      		{'name': 'is_okd_compliant', 'control': 'checkbox', 'value' : True, 'label': _('ODK Complaint')},
      		{'name': 'is_osi_compliant', 'control': 'checkbox', 'value' : True, 'label': _('OSI Compliant')},
      		{'name': 'is_generic', 'control': 'checkbox', 'value' : True, 'label': _('Generic')},
      		{'name': 'domain_data', 'control': 'checkbox', 'value' : True, 'label': _('Domain Data')},
      		{'name': 'domain_content', 'control': 'checkbox', 'value' : True, 'label': _('Domain Content')},
      		{'name': 'domain_software', 'control': 'checkbox', 'value' : True, 'label': _('Domain Software')},
		]
        return items


    def _get_delete_form(self, data):
	
	items = [ {'name': 'license', 'control' : 'select', 'options' : self._get_license_titles(), 'selected' : data.get('license'), 'label' : _('License')},
                ]
	return items


    def add(self):
	data = request.POST
	items = self._get_form_items() # get form items
	delete_items = self._get_delete_form(data)
	if 'delete' in data:
	    self._delete_license(data['license'])

	elif 'edit' in data:
	    license_data = self._get_license(data['license'])
	    license_data['license'] = data['license']
	    
	    vars = {'data': license_data, 'errors': {}, 'form_items': items, 'delete_form_items': delete_items}
            return base.render('admin/licenses.html',
                           extra_vars = vars)
	
	elif 'save' in data:
	    license = {}
            # iterate through each item in the form and match it with corresponding form data
	    
	    # redirect if title is empty
	    if data['title'] is u'':
		vars = {'data': data, 'errors': {'title': ['Required']}, 'form_items': items, 'delete_form_items': delete_items}
                return base.render('admin/licenses.html',
                           extra_vars = vars)

            for item in items:
		name = item['name']
        
	        if name not in data: # if checkbox not checked data will not have the form item
		    license[name] = False # set the checkbox to false for not checked
		elif data[name] is u'' and item['control'] is 'checkbox':
		    license[name] = True	
		else:
		    license[name] = data[name] # match the item key to the data value
		
	
   	    license['id'] =  license['title'].replace (" ", "-") # change the title into database loadable ID
	    self._add_license(license)
	delete_items = self._get_delete_form(data)

	vars = {'data': {}, 'errors': {}, 'form_items': items, 'delete_form_items': delete_items}
	return base.render('admin/licenses.html',
                           extra_vars = vars)


    def _get_license(self, target_license):
	with open(LICENSE_FILE, 'r') as read:
            licenses = json.load(read)
        
	license_dict = {}
        for license in licenses:
	    if str(license['id']) == target_license:
                license_dict = license
   	return license_dict

 
    def _add_license(self, target_license):
	with open(LICENSE_FILE, 'r') as read:
            licenses = json.load(read)

	#if the license is already in the file update the license
	for license in licenses:
           if license['id'] == target_license['id']:
		license.update(target_license)
		with open(LICENSE_FILE, 'w') as outfile:
            	    json.dump(licenses, outfile)
		return True
    	
	# add the new license if the license is not in the file
	licenses.append(target_license)
    	# write to file
	with open(LICENSE_FILE, 'w') as outfile:
            json.dump(licenses, outfile)


    def _delete_license(self, target_license):
	with open(LICENSE_FILE, 'r') as read:
            licenses = json.load(read)
        # remove the target license
	for license in licenses:
	    if str(license['id']) == target_license: 
        	licenses.remove(license)
        # write to file
	with open(LICENSE_FILE, 'w') as outfile:
            json.dump(licenses, outfile)

	
    # reload the license file
    def _load_licenses(self):
	license_register = model.Package.get_license_register()
        group_url = config.get('licenses_group_url', None)
        if group_url:
            license_register.load_licenses(group_url)
    
 
    # this returns a dict of licenses that the dropdown can read
    def _get_license_titles(self):

        self._load_licenses()
	context = {'user' :'civic_info'}
    	data_dict = {}
    	licenses = logic.get_action('license_list')(context, data_dict)
    	titles = []
	for license in licenses:
            license_dict = {}
            license_dict['text'] = license['title']
            license_dict['value'] = license['id']
            titles.append(license_dict)
    	# the format goes ('text' : 'licence_title', 'value' : 'licence_id'}
    	return titles


class ConfigurationController(base.BaseController):


    # restrict access to sysadmins
    def __before__(self, action, **params):
        super(ConfigurationController, self).__before__(action, **params)
        context = {'model': model,
                   'user': c.user, 'auth_user_obj': c.userobj}
        try:
            logic.check_access('sysadmin', context, {})
        except logic.NotAuthorized:
            base.abort(401, _('Need to be system administrator to administer'))
        c.revision_change_state_allowed = True

    def _get_form_items(self):

        # This is a list of items for the form. Pass these items into the form generator.
        # This is also used to iterate through the items in the form while building the license
	options = self._get_dropdown_options()
	featured = self._get_featured()
	items = [
                {'name': 'left_side', 'control': 'select', 'options' : options, 'selected' : featured[0], 'label' : _('Spot One')},
                {'name': 'right_side', 'control': 'select', 'options' : options, 'selected' : featured[1], 'label' : _('Spot Two')},
                ]
        return items

    def index(self):
	data = request.POST
	featured = []
	items = self._get_form_items()
	if 'save' in data:
	    for item in items:
		name = item['name']
	    	featured.append(data[name])
	    self._set_featured(featured)
	items = self._get_form_items()
	vars = { 'errors': {}, 'form_items': items}
        return base.render('admin/advanced_configuration.html',
                          extra_vars = vars)
    # get options in format that can be used by dropdown
    def _get_dropdown_options(self):
	context = {'user' :'civic_info'}
        data_dict = {'all_fields' : True}
        
	groups = logic.get_action('group_list')(context, data_dict)
        titles = []
	titles.append({'text' : 'None', 'value' : 'none'}) # Add option for no featured
        for group in groups:
            group_dict = {}
            group_dict['text'] = group['title']
            group_dict['value'] = group['id']
            titles.append(group_dict)
	
	orgs = logic.get_action('organization_list')(context, data_dict)
        for org in orgs:
            org_dict = {}
            org_dict['text'] = org['title']
            org_dict['value'] = org['id']
            titles.append(org_dict)

        return titles

    def _set_featured(self, new_featured):
	with open(FEATURED_FILE, 'w') as outfile:
            json.dump(new_featured, outfile)

    def _get_featured(self):
        with open(FEATURED_FILE, 'r') as infile:
            featured = json.load(infile)
	    return featured
