from django.conf import settings

def get_current_schema():
    options = settings.DATABASES['default'].get('OPTIONS', {})
    search_path = options.get('options', '')
    if search_path:
        # Extract schema name from search_path option
        search_path = search_path.split('=')[1].split(',')[0].strip()
        return search_path
    return 'public'  # Default to 'public' schema if not specified