import json
import inspect
from copy import deepcopy

from faker import Faker
from faker_israel import Provider as IsraelProvider

from . import pdf_multi_config_constants
from .faker_var_value import FakerVarValue


def process_var_value(key, value, vars_, fake, with_cache=True):
    try:
        if not isinstance(value, FakerVarValue):
            if isinstance(value, (tuple, list)):
                value = FakerVarValue(value[0], *value[1:])
            else:
                value = FakerVarValue(value)
        if not key:
            key = value.method
        if key in vars_ and with_cache:
            return vars_[key]
        elif len(value.args) > 0 or hasattr(fake, value.method):
            args = [process_var_value(arg, arg, vars_, fake) for arg in value.args]
            vars_[key] = value.get(fake, args)
            return vars_[key]
        else:
            return value.method
    except Exception as e:
        raise Exception(f'Error processing var value "{key}" "{value}": {e}') from e


def generate(type_config):
    fake = Faker('he_IL')
    fake.add_provider(IsraelProvider)
    out = deepcopy(type_config)
    out.pop('_key_prefix')
    vars_ = out.pop('_vars', None) or {}
    replacements = out.pop('replacements')
    out['_fake_vars'] = {}
    for k, v in vars_.items():
        if callable(v) and not isinstance(v, FakerVarValue):
            vars_[k] = v(vars_)
            out['_fake_vars'][k] = [inspect.getsource(v)]
        else:
            out['_fake_vars'][k] = v.as_tuple() if isinstance(v, FakerVarValue) else v
            process_var_value(k, v, vars_, fake, with_cache=False)
    out['replacements'] = {}
    for repl_key, repl_config in replacements.items():
        repl_config['_fake'] = repl_config['new'].as_tuple() if isinstance(repl_config['new'], FakerVarValue) else repl_config['new']
        repl_config['new'] = process_var_value(None, repl_config['new'], vars_, fake)
        out['replacements'][repl_key] = repl_config
    return out


def main(config_type, num=1, key_prefix=None, doc_name=None):
    type_config = pdf_multi_config_constants.TYPES[config_type]
    if key_prefix:
        type_config['_key_prefix'] = key_prefix
    if doc_name:
        type_config['doc_name'] = doc_name
    output = {
        (type_config['_key_prefix'] + str(i + 1)): generate(type_config)
        for i in range(num)
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))
