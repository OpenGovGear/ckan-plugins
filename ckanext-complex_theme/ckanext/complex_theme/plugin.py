import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

def most_popular_groups():
    '''Return a sorted list of groups with the most datasets. '''

    # get a list of all sites groups from ckan sorted by # of datasets
    groups = toolkit.get_action('group_list')(
        data_dict={'sort': 'packages desc', 'all_fields': True})

    # Trunc the list to 10
    groups = groups[:10]

    return groups

class ComplexThemePlugin(plugins.SingletonPlugin):
    '''An example theme plugin.

    '''
    # Declare that this class implements IConfigurer.
    plugins.implements(plugins.IConfigurer)

    # Declare that this plugin will implement ITemplateHelpers.
    plugins.implements(plugins.ITemplateHelpers)

    def update_config(self, config):

        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        # 'templates' is the path to the templates dir, relative to this
        # plugin.py file.
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')
        toolkit.add_resource('fanstatic', 'complex_theme')

    def get_helpers(self):
        '''Register most_popular_groups() function aboive as a template
        helper function.'''

        return {'complex_theme_most_popular_groups': most_popular_groups}
