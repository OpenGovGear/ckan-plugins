'''plugin.py

'''
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.logic as logic
def get_orgs():
    '''Return a sorted list of the groups with the most dataset'''
    context = {'user':'civic_info'}
    data_dict = {'available_only': True, 'am_member': "false"}
    return logic.get_action('group_list_authz')(context, data_dict)

def url_for_display_image(group_id):
        # Call organization_show to get url of uploaded image
    data_dict ={"id":group_id}
    group_dict = logic.get_action('organization_show')({}, data_dict)
    return group_dict["image_display_url"]

class AggregatorThemeClass(plugins.SingletonPlugin):
    '''The Aggregator theme plugin.

    '''
    # Declare that this class implements IConfigurer.
    plugins.implements(plugins.IConfigurer)

    plugins.implements(plugins.ITemplateHelpers)

    def update_config(self, config):

        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        # 'templates' is the path to the templates dir, relative to this
        # plugin.py file.
	toolkit.add_public_directory(config, 'public')
        toolkit.add_template_directory(config, 'templates')
	toolkit.add_resource('fantastic', 'agg_theme')
    
    def get_helpers(self):
        '''Register helper functions.

        '''
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {'get_orgs': get_orgs, 'url_for_display_image': url_for_display_image}

