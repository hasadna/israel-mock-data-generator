class FakerVarValue:

    def __init__(self, method, *args, max_length=None, chars_reverse=False, prevent_apostrophe=False, **kwargs):
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.max_length = max_length
        self.chars_reverse = chars_reverse
        self.prevent_apostrophe = prevent_apostrophe
        self._log = [f"init: {method} {args}"]

    def as_tuple(self):
        return self.method, *self.args

    def is_valid(self, val):
        if isinstance(val, str):
            if self.prevent_apostrophe and ("'" in val or '"' in val or '׳' in val):
                self._log.append(f'got invalid value "{val}" with apostrophe')
                return False
            elif self.max_length is not None and len(val) > self.max_length:
                self._log.append(f'got invalid value "{val}" with length {len(val)}')
                return False
            else:
                return True
        elif self.prevent_apostrophe or self.max_length is not None:
            assert hasattr(val, 'faker_var_value_is_valid')
            return val.faker_var_value_is_valid(self)
        else:
            return True

    def get(self, fake, args):
        for i in range(50):
            val = getattr(fake, self.method)(*args, **self.kwargs)
            if self.is_valid(val):
                return self.post_get(val)
        raise Exception(f'Could not generate valid value within 50 random tries\n' + "\n".join(self._log))

    def post_get(self, val):
        if self.chars_reverse:
            assert isinstance(val, str)
            val = val[::-1]
        return val
