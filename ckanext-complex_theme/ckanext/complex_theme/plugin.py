import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.model as model
import ckan.lib.search as search
import json
import ckan.lib.helpers as h
import ckan.logic as logic
NUM_MOST_VIEWED_DATASETS = 3

def get_most_viewed_datasets(num_datasets=NUM_MOST_VIEWED_DATASETS):
    try:
        data = {'rows': num_datasets,
                'sort': u'views_total desc',
                'facet': u'false',
                'fq': u'capacity: "public"',
                'fl': 'id, name, title'}
        # Ugly: going through ckan.lib.search directly
        # (instead of get_action('package_search').
        #
        # TODO: Can we return views_total using package_search for internal
        # use only (without outputting it during public API calls)?
	query = search.query_for(model.Package)
	result = query.run(data)
	return [r for r in result.get('results', [])]
    except search.SearchError, e:
        log.error('Error searching for most viewed datasets')
        log.error(e)

def get_tag_names():
    tags = h.get_facet_items_dict('tags', limit=20)
    tag_names = [tag['name'] for tag in tags]
    return json.dumps(tag_names)

def get_groups():
    '''Return a sorted list of the groups with the most dataset'''
    data_dict = {'all_fields': True, 'ignore_auth': "true"}
    return logic.get_action('group_list')({}, data_dict)

def get_orgs():
    '''Return a sorted list of the groups with the most dataset'''
    context = {'user':'hayden'}
    data_dict = {'all_fields': True, 'ignore_auth': "true"}
    return logic.get_action('organization_list')(context, data_dict)

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
        '''Register the most_popular_groups() function above as a template
        helper function.

        '''
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {'get_most_viewed_datasets': get_most_viewed_datasets,        
		'get_tag_names' : get_tag_names,
		'get_orgs': get_orgs,
		'get_groups' : get_groups
                }
