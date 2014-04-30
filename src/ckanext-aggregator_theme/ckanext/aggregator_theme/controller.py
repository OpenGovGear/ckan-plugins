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

LICENCE_FILE = '/usr/lib/ckan/default/src/ckanext-aggregator_theme/ckanext/aggregator_theme/licences.json'
FEATURED_FILE = '/usr/lib/ckan/default/src/ckanext-aggregator_theme/ckanext/aggregator_theme/featured.json'

class LicenceController(base.BaseController):


    #This restricts view of this page to sysadmins   
    def __before__(self, action, **params):
        super(LicenceController, self).__before__(action, **params)
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
        	{'name': 'title', 'control': 'input', 'label': _('Title'), 'placeholder' : 'My Licence', 'is_required': 'is_required'},
      		{'name': 'maintainer', 'control': 'input', 'label': _('Maintainer'), 'placeholder' : 'My Licensing Body'},
      		{'name': 'url', 'control': 'input', 'label': _('URL'), 'placeholder' : 'http://www.mylicenceinfo.com'},
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
	
	items = [ {'name': 'licence', 'control' : 'select', 'options' : self._get_licence_titles(), 'selected' : data.get('licence'), 'label' : _('Licence')},
                ]
	return items


    def add(self):
	data = request.POST
	items = self._get_form_items() # get form items
	delete_items = self._get_delete_form(data)
	if 'delete' in data:
	    self._delete_licence(data['licence'])

	elif 'edit' in data:
	    licence_data = self._get_licence(data['licence'])
	    licence_data['licence'] = data['licence']
	    
	    vars = {'data': licence_data, 'errors': {}, 'form_items': items, 'delete_form_items': delete_items}
            return base.render('admin/licences.html',
                           extra_vars = vars)
	
	elif 'save' in data:
	    licence = {}
            # iterate through each item in the form and match it with corresponding form data
	    
	    # redirect if title is empty
	    if data['title'] is u'':
		vars = {'data': data, 'errors': {'title': ['Required']}, 'form_items': items, 'delete_form_items': delete_items}
                return base.render('admin/licences.html',
                           extra_vars = vars)

            for item in items:
		name = item['name']
        
	        if name not in data: # if checkbox not checked data will not have the form item
		    licence[name] = False # set the checkbox to false for not checked
		elif data[name] is u'' and item['control'] is 'checkbox':
		    licence[name] = True	
		else:
		    licence[name] = data[name] # match the item key to the data value
		
	
   	    licence['id'] =  licence['title'].replace (" ", "-") # change the title into database loadable ID
	    self._add_licence(licence)
	delete_items = self._get_delete_form(data)

	vars = {'data': {}, 'errors': {}, 'form_items': items, 'delete_form_items': delete_items}
	return base.render('admin/licences.html',
                           extra_vars = vars)


    def _get_licence(self, target_licence):
	with open(LICENCE_FILE, 'r') as read:
            licences = json.load(read)
        
	licence_dict = {}
        for licence in licences:
	    if str(licence['id']) == target_licence:
                licence_dict = licence
   	return licence_dict

 
    def _add_licence(self, target_licence):
	with open(LICENCE_FILE, 'r') as read:
            licences = json.load(read)

	#if the licence is already in the file update the licence
	for licence in licences:
           if licence['id'] == target_licence['id']:
		licence.update(target_licence)
		with open(LICENCE_FILE, 'w') as outfile:
            	    json.dump(licences, outfile)
		return True
    	
	# add the new license if the licence is not in the file
	licences.append(target_licence)
    	# write to file
	with open(LICENCE_FILE, 'w') as outfile:
            json.dump(licences, outfile)


    def _delete_licence(self, target_licence):
	with open(LICENCE_FILE, 'r') as read:
            licences = json.load(read)
        # remove the target license
	for licence in licences:
	    if str(licence['id']) == target_licence: 
        	licences.remove(licence)
        # write to file
	with open(LICENCE_FILE, 'w') as outfile:
            json.dump(licences, outfile)

	
    # reload the licence file
    def _load_licences(self):
	license_register = model.Package.get_license_register()
        group_url = config.get('licenses_group_url', None)
        if group_url:
            license_register.load_licenses(group_url)
    
 
    # this returns a dict of licences that the dropdown can read
    def _get_licence_titles(self):

        self._load_licences()
	context = {'user' :'civic_info'}
    	data_dict = {}
    	licences = logic.get_action('license_list')(context, data_dict)
    	titles = []
	for licence in licences:
            licence_dict = {}
            licence_dict['text'] = licence['title']
            licence_dict['value'] = licence['id']
            titles.append(licence_dict)
    	return titles


class ConfigurationController(base.BaseController):

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
