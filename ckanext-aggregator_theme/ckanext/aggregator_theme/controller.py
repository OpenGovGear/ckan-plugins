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

class LicenceController(base.BaseController):
    
    def _get_form_items(self):
        
	# This is a list of items for the form. Pass these items into the form generator.
	# This is also used to iterate through the items in the form while building the license
	
	items = [
        	{'name': 'title', 'control': 'input', 'label': _('Title')},
   	   	{'name': 'family', 'control': 'input', 'label': _('Family')},
      		{'name': 'maintainer', 'control': 'input', 'label': _('Maintainer')},
      		{'name': 'url', 'control': 'index', 'prepend': 'http://', 'label': _('URL')},
	      	{'name': 'status', 'control': 'checkbox', 'label': _('Active')},
      		{'name': 'odk_compliant', 'control': 'checkbox', 'value' :'True', 'label': _('ODK Complaint')},
      		{'name': 'osi_compliant', 'control': 'checkbox', 'label': _('OSI Compliant')},
      		{'name': 'generic', 'control': 'checkbox', 'label': _('Generic')},
      		{'name': 'domain_data', 'control': 'checkbox', 'label': _('Domain Data')},
      		{'name': 'domain_content', 'control': 'checkbox', 'label': _('Domain Content')},
      		{'name': 'domain_software', 'control': 'checkbox', 'label': _('Domain Software')},
		]
        return items

    def add(self):
        items = self._get_form_items() # get form items
	data = request.POST # get data from form
	licence = {}
        if 'save' in data:
            # iterate through each item in the form and match it with corresponding form data
            for item in items:
		name = item['name']
                if name not in data: # if checkbox not checked data will not have the form item
		    licence[name] = 'false' # set the checkbox to false for not checked
		elif data[name] is u'': # if checkbox is checked it will be recorded as empty unicode string
		    licence[name] = 'true' # set the checkbox to to true for checked
		else:
		    licence[name] = data[name] # match the item key to the data value

	    licence['id'] =  licence['title'].lower().replace (" ", "-") # change the title into database loadable ID
	    self._add_licence(licence)
            h.redirect_to(controller='ckanext.aggregator_theme.controller:LicenceController', action='add')

        data = {}
	vars = {'data': data, 'errors': {}, 'form_items': items}
        return base.render('admin/licences.html',
                           extra_vars = vars)

    def _add_licence(self, licence):
    	# load the license file
	with open('/usr/lib/ckan/default/src/ckanext-aggregator_theme/ckanext/aggregator_theme/data.json', 'r') as read:
            licences = json.load(read)
    	# add the new license
	licences.append(licence)
    	# write to file
	with open('/usr/lib/ckan/default/src/ckanext-aggregator_theme/ckanext/aggregator_theme/data.json', 'w') as outfile:
            json.dump(licences, outfile)

class ConfigurationController(base.BaseController):

     def _get_form_items(self):

        # This is a list of items for the form. Pass these items into the form generator.
        # This is also used to iterate through the items in the form while building the license

        items = [
                {'name': 'groups', 'control': 'input', 'label': _('Featured Subjects')},
                {'name': 'organizations', 'control': 'input', 'label': _('Featured Contributors')},
                ]
        return items

