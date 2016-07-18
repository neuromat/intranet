SUIT_CONFIG = {
    'ADMIN_NAME': 'NIRA',
    'MENU_OPEN_FIRST_CHILD': False,
    'HEADER_DATE_FORMAT': 'l, d F Y',
    'MENU': (
        {'app': 'activity', 'icon': 'icon-calendar'},
        {'app': 'dissemination', 'icon': 'icon-facetime-video'},
        {'app': 'person', 'icon': 'icon-user'},
        {'app': 'research', 'icon': 'icon-book'},
        {'app': 'scientific_mission', 'icon': 'icon-plane'},
        {'label': _('Reports'), 'icon': 'icon-th', 'permissions': 'custom_auth.view_reports', 'models': (
            {'label': _('Academic works'), 'url': '/research/academic_works'},
            {'label': _('Articles'), 'url': '/research/articles'},
            {'label': _('Disseminations'), 'url': '/dissemination/dissemination_report'},
            {'label': _('Meetings'), 'url': '/activity/meetings'},
            {'label': _('Scientific missions'), 'url': '/scientific_mission/report'},
            {'label': _('Seminars'), 'url': '/activity/seminars'},
            {'label': _('Training programs'), 'url': '/activity/training_programs'},
        )},
        {'label': _('Add content'), 'icon': 'icon-upload', 'permissions': 'custom_auth.add_content', 'models': (
            {'label': _('Create/Update citation name'), 'url': '/person/citation_names'},
            {'label': _('Import papers'), 'url': '/research/import_papers'},
        )},
        {'label': _('Documents'), 'icon': 'icon-list-alt', 'permissions': 'custom_auth.create_documents', 'models': (
            {'label': _('FAPESP - appendix 5'), 'url': '/scientific_mission/anexo5/'},
            {'label': _('Seminar poster'), 'url': '/activity/seminar_poster'},
        )},
        '-',
        {'app': 'cities_light', 'icon': 'icon-globe', 'label': _('Cities')},
        {'app': 'custom_auth', 'icon': 'icon-lock', 'label': _('Users')},
        {'app': 'auth', 'icon': 'icon-lock', 'label': _('Groups')},
    ),
}