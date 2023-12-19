from .faker_var_value import FakerVarValue


TYPES = {
    'poalim_private': {
        '_key_prefix': 'poalim.private.heb.2-',
        'bank_name': 'poalim',
        'doc_name': 'private.heb.2',
        'replace_include_location': False,
        'replace_method': 1,
        '_vars': {
            'bank': ('bank', 'poalim'),
            'bank_branch': ('bank_branch', 'bank'),
            'related_names': FakerVarValue('related_names', name_reverse=True, max_length=12, prevent_apostrophe=True),
            'name1': FakerVarValue('related_names_name', 'related_names', max_length=12, chars_reverse=True, prevent_apostrophe=True),
            'name2': FakerVarValue('related_names_name', 'related_names', max_length=12, chars_reverse=True, prevent_apostrophe=True),
            'tz1': 'teudat_zehut',
            'tz2': 'teudat_zehut',
        },
        'replacements': {
            '-1': {
                'several': True,
                'new': ('bank_account_number', 'bank'),
                'old': 'ז1ז1ז1ז1'
            },
            '-2': {
                'new': 'tz1',
                'old': 'ו1ו1ו1ו1ו'
            },
            '-4': {
                'new': ('bank_branch_number', 'bank_branch'),
                'old': 'ד4ד'
            },
            '-5': {
                'new': ('bank_statement_print_date', '%d/%m/%Y'),
                'old': 'א1' + '/' + 'ב1' + '/' + 'ש1ש1'
            },
            '-6': {
                'several': True,
                'new': 'name1',
                'old': 'ןד ילארשי'
            },
            '-7': {
                'new': ('bank_account_creation_date', '%d/%m/%Y'),
                'old': 'א2' + '/' + 'ב2' + '/' + 'ש2ש2'
            },
            '-8': {
                'new': 'tz2',
                'old': 'ו2ו2ו2ו2ו'
            },
            '-9': {
                'new': 'name2',
                'old': 'הנד ילארשי',
            },
        }
    },
    'leumi_amuta': {
        '_key_prefix': 'leumi.amota.heb.1-',
        "bank_name": "leumi",
        "doc_name": "amota.heb.1",
        "replace_include_location": False,
        "replace_method": 1,
        '_vars': {
            'bank': ('bank', 'leumi'),
            'bank_branch': ('bank_branch', 'bank'),
            'bank_account_number': ('bank_account_number', 'bank'),
        },
        "replacements": {
            "-1": {
                "several": True,
                "new": 'bank_account_number',
                "old": "ז1ז1ז1ז1"
            },
            "-2": {
                "new": "het_pey",
                "old": "ח1פ1ח1פ1ח"
            },
            "-4": {
                "new": ("bank_branch_number", "bank_branch"),
                "old": "ד4ד"
            },
            "-5": {
                "new": ("bank_statement_print_date", "%d/%m/%Y"),
                "old": "א1/ב1/ש1ש1"
            },
            "-6": {
                "new": FakerVarValue('company', chars_reverse=True),
                "old": "התומע המשש התומע"
            },
            "-8": {
                "new": ('bank_iban', 'bank_branch', 'bank_account_number'),
                "old": "ה1ה1ה1ה1ה1ה1ה1ה1ה1ה"
            },
        }
    }
}
