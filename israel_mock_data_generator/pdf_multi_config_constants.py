from .faker_var_value import FakerVarValue


MIZRAHI_PREVENT_CHARS = list("9")
DISCOUNT_PREVENT_CHARS = list("'זךןעפףצץ")


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
    },
    'mizrahi_amuta': {
        '_key_prefix': 'tfachot.amota.heb.1-',
        "bank_name": "tfachot",
        "doc_name": "amota.heb.1",
        "replace_include_location": False,
        "replace_method": 1,
        '_vars': {
            'bank': ('bank', 'mizrahi'),
            'bank_branch': FakerVarValue(
                'bank_branch', 'bank', prevent_chars=MIZRAHI_PREVENT_CHARS,
                faker_var_value_bank_branch_is_valid_fields=['number']
            ),
            'bank_account_number': FakerVarValue('bank_account_number', 'bank', prevent_chars=MIZRAHI_PREVENT_CHARS),
            'company_name': FakerVarValue(
                'company', min_words=3, post_get_callback=lambda s: s.replace(',', ''), prevent_chars=MIZRAHI_PREVENT_CHARS
            ),
            'company_name_short': lambda vars_: vars_['company_name'].split()[0] + ' ' + vars_['company_name'].split()[2],
            'company_name_part1': lambda vars_: ' '.join(vars_['company_name'].split(' ')[0:1]),
            'company_name_part2': lambda vars_: ' '.join(vars_['company_name'].split(' ')[1:]),
        },
        "replacements": {
            "-1": {
                "new": "bank_account_number",
                "old": "ז1ז1ז1ז1"
            },
            "-2": {
                "new": ("bank_branch_number", "bank_branch"),
                "old": "ד4ד"
            },
            "-3": {
                "new": FakerVarValue('bank_iban', 'bank_branch', 'bank_account_number', prevent_chars=MIZRAHI_PREVENT_CHARS),
                "old": "ה1ה1ה1ה1ה1ה1ה1ה1ה1ה"
            },
            "-4": {
                "new": FakerVarValue("het_pey", prevent_chars=MIZRAHI_PREVENT_CHARS),
                "old": "ח1פ1ח1פ1ח"
            },
            "-5": {
                "several": True,
                "new": FakerVarValue("bank_statement_print_date", "%d/%m/%Y", prevent_chars=MIZRAHI_PREVENT_CHARS),
                "old": "א1/ב1/ש1ש1"
            },
            "-6": {
                "new": FakerVarValue('bank_account_creation_date', '%d/%m/%Y', prevent_chars=MIZRAHI_PREVENT_CHARS),
                "old": "א2/ב2/ש2ש2"
            },
            "-7": {
                "new": FakerVarValue('time', '%H:%M', prevent_chars=MIZRAHI_PREVENT_CHARS),
                "old": "ט1:ט2"
            },
            "-6a": {
                "reverseNew": True,
                "new": 'company_name_short',
                "old": "מ\"עב הרבח"
            },
            "-7a": {
                "reverseNew": True,
                "new": 'company_name',
                "old": "התומע המשש התומע"
            },
            "-8": {
                "pad": 10,
                "reverseNew": True,
                "new": 'company_name_part1',
                "old": "1-יצח-םש"
            },
            "-10": {
                "reverseNew": True,
                "new": 'company_name_part2',
                "old": "2-יצח-םש"
            }
        }
    },
    'discount_private': {
        '_key_prefix': 'discont.private.heb.1-',
        "bank_name": "discont",
        "doc_name": "private.heb.1",
        "replace_include_location": False,
        "replace_method": 1,
        '_vars': {
            'bank': ('bank', 'discount'),
            'bank_branch': FakerVarValue(
                'bank_branch', 'bank', prevent_chars=DISCOUNT_PREVENT_CHARS,
                faker_var_value_bank_branch_is_valid_fields=['name', 'number', 'address']
            ),
            'bank_account_number': FakerVarValue('bank_account_number', 'bank', prevent_chars=list('15')),
            'related_names': FakerVarValue('related_names', name_reverse=True, prevent_chars=DISCOUNT_PREVENT_CHARS),
            'name': FakerVarValue('related_names_name', 'related_names', prevent_chars=DISCOUNT_PREVENT_CHARS),
        },
        "replacements": {
            "-1": {
                "special_handling": "discont02",
                "new": "bank_account_number",
                "old": "י7י7י7י7י7"
            },
            "-2": {
                "new": "bank_account_number",
                "old": "י7י7י7י7י7"
            },
            "-3": {
                # old bank account number
                "new": ('numerify', '0-00-######'),
                "old": "י2י2י2י2י2י"
            },
            "-4": {
                "new": FakerVarValue('teudat_zehut', prevent_chars=(list('15'))),
                "old": "999999999"
            },
            "-5": {
                "special_handling": "discont01",
                "new": FakerVarValue("bank_statement_print_date", "%d/%m/%Y", prevent_chars=('4', '5', '6', '9')),
                "old": "88/88/8888"
            },
            "-6": {
                "special_handling": "discont03",
                "reverseNew": False,
                "new": "name",
                "old": "הנד יול"
            },
            "-7": {
                "reverseNew": True,
                "new": 'name',
                "old": "הנד יול"
            },
            "-8": {
                "reverseNew": True,
                "new": ('bank_branch_name', 'bank_branch'),
                "old": "פינסםש",
                "_fake": "snif name"
            },
            "-9": {
                "new": ('bank_branch_number', 'bank_branch'),
                "old": "ד4ד"
            },
            "-10": {
                "reverseNew": True,
                "new": ('bank_branch_address', 'bank_branch'),
                "old": "כ2כ2כ2כ"
            },
            "-11": {
                "reverseNew": True,
                "new": FakerVarValue(
                    'parse', "{{street_address}}, {{city}}", max_length=15, post_get_callback=lambda s: s.replace(',', ''),
                    prevent_chars=DISCOUNT_PREVENT_CHARS
                ),
                "old": "כ1כ1כ1כ1כ1כ1כ1כ1כ1כ1כ1כ"
            }
        }
    }
}
