TYPES = {
    'poalim_private': {
        '_key_prefix': 'poalim.private.heb.2-',
        'bank_name': 'poalim',
        'doc_name': 'private.heb.2',
        'replace_include_location': False,
        'replace_method': 1,
        '_vars': {
            'bank': ('bank', 'פועלים'),
            'bank_statement': ('bank_statement', 'bank'),
        },
        'replacements': {
            '-1': {
                'several': True,
                'new': ('bank_account_number', 'bank'),
                'old': 'ז1ז1ז1ז1'
            },
            '-2': {
                'new': 'teudat_zehut',
                'old': 'ו1ו1ו1ו1ו'
            },
            '-4': {
                'new': ('bank_branch_number', 'bank'),
                'old': 'ד4ד'
            },
            '-5': {
                'new': ('bank_statement_print_date', '%d/%m/%Y'),
                'old': 'א1' + '/' + 'ב1' + '/' + 'ש1ש1'
            },
            '-6': {
                'several': True,
                'new': 'name',
                'old': 'ןד ילארשי'
            },
            '-7': {
                'new': ('bank_account_creation_date', '%d/%m/%Y'),
                'old': 'א2' + '/' + 'ב2' + '/' + 'ש2ש2'
            },
            '-8': {
                'new': 'teudat_zehut',
                'old': 'ו2ו2ו2ו2ו'
            },
            '-9': {
                'new': 'name',
                'old': 'הנד ילארשי'
            },
        }
    }
}
