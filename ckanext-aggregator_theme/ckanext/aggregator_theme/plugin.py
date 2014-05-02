'''
plugin.py for the aggregator theme

'''
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.logic as logic
import ckan.lib.helpers as h
import json
FEATURED_FILE = "data/featured.json"


def get_orgs():
    '''Return a sorted list of the groups with the most dataset'''
    context = {'user':'hayden'}
    data_dict = {'all_fields': True, 'am_member': "false"}
    return logic.get_action('organization_list')(context, data_dict)

def get_groups():
    '''Return a sorted list of the groups with the most dataset'''
    context = {'user':'hayden'}
    data_dict = {'all_fields': True, 'am_member': "false"}
    return logic.get_action('group_list')(context, data_dict)

def url_for_display_image(group_id):
    # Call organization_show to get url of uploaded image
    data_dict ={"id":group_id}
    group_dict = logic.get_action('organization_show')({}, data_dict)
    return group_dict["image_display_url"]

def get_featured():
    with open(FEATURED_FILE, 'r') as infile:
    	featured = json.load(infile)
    featured_items = []
    for feature in featured:
	context = {'user':'civic_info'}
	data_dict = {'id' : feature}
	try:
		featured_item = logic.get_action('group_show')(context, data_dict)
	except:
		featured_item = logic.get_action('organization_show')(context, data_dict)
	featured_items.append(featured_item)
    return featured_items

class AggregatorThemeClass(plugins.SingletonPlugin):
    '''The Aggregator theme plugin.

    '''
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)

    def update_config(self, config):

        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        # 'templates' is the path to the templates dir, relative to this
        # plugin.py file.
	toolkit.add_public_directory(config, 'public')
        toolkit.add_template_directory(config, 'templates')
	toolkit.add_resource('fanstatic', 'agg_theme')
    
    def get_helpers(self):
        '''Register helper functions.

        '''
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {'get_orgs': get_orgs, 'url_for_display_image': url_for_display_image, 'get_featured' : get_featured, 'get_groups' : get_groups } 
    
    def before_map(self, m):
        
	# This sets up a route for the license plugin. The format goes as follows
	#'
	# m.connect('route_alias', 'url', controller='path.to.controller:ProperController',
	# action='function_to_call', ckan_icon='relevant_icon')
	m.connect('ckanadmin_licenses', '/ckan-admin/licenses',
                    controller='ckanext.aggregator_theme.controller:LicenseController',
                    action='add', ckan_icon='edit')
	m.connect('ckanadmin_advanced', '/ckan-admin/advanced_configuration',
		    controller='ckanext.aggregator_theme.controller:ConfigurationController',
                    action='index', ckan_icon='edit')
	return m
