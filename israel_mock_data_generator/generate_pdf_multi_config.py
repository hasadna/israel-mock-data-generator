import json
from copy import deepcopy

from faker import Faker
from faker_israel import Provider as IsraelProvider

from . import pdf_multi_config_constants


def process_var_value(key, value, vars_, fake):
    if isinstance(value, (tuple, list)):
        method = value[0]
        args = value[1:]
    else:
        method = value
        args = []
    if not key:
        key = method
    if key in vars_:
        return vars_[key]
    elif len(args) > 0 or hasattr(fake, method):
        args = [process_var_value(arg, arg, vars_, fake) for arg in args]
        vars_[key] = getattr(fake, method)(*args)
        return vars_[key]
    else:
        return value


def generate(type_config):
    fake = Faker('he_IL')
    fake.add_provider(IsraelProvider)
    out = deepcopy(type_config)
    out.pop('_key_prefix')
    vars_ = out.pop('_vars')
    for k, v in vars_.items():
        process_var_value(k, v, vars_, fake)
    for repl_key, repl_config in out['replacements'].items():
        repl_config['_fake'] = repl_config['new']
        repl_config['new'] = process_var_value(None, repl_config['new'], vars_, fake)
    return out


def main(config_type, num=1):
    type_config = pdf_multi_config_constants.TYPES[config_type]
    output = {
        (type_config['_key_prefix'] + str(i + 1)): generate(type_config)
        for i in range(num)
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))
