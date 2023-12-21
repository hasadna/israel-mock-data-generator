import inspect


class FakerVarValue:

    def __init__(self, method, *args, max_length=None, chars_reverse=False, prevent_apostrophe=False, prevent_chars=None,
                 min_words=None, post_get_callback=None, **kwargs):
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.max_length = max_length
        self.chars_reverse = chars_reverse
        self.prevent_apostrophe = prevent_apostrophe
        self.prevent_chars = prevent_chars
        self.min_words = min_words
        self.post_get_callback = post_get_callback
        self._log = [f"init: {method} {args}"]

    def as_tuple(self):
        res = [self.method, *self.args]
        if self.kwargs:
            for k, v in self.kwargs.items():
                res.append(f'{k}={v}')
        for attr in dir(self):
            if attr.startswith('_') or attr in ('method', 'args', 'kwargs'):
                continue
            val = getattr(self, attr)
            if val and not callable(val):
                res.append(f'{attr}={val}')
        if self.post_get_callback:
            res.append(inspect.getsource(self.post_get_callback).strip())
        return *res,

    def is_valid(self, val):
        if isinstance(val, str):
            if self.prevent_apostrophe and ("'" in val or '"' in val or '׳' in val):
                self._log.append(f'got invalid value "{val}" with apostrophe')
                return False
            elif self.max_length and len(val) > self.max_length:
                self._log.append(f'got invalid value "{val}" with length {len(val)}')
                return False
            elif self.prevent_chars and any(c in val for c in self.prevent_chars):
                self._log.append(f'got invalid value "{val}" with chars {self.prevent_chars}')
                return False
            elif self.min_words and len(val.split()) < self.min_words:
                self._log.append(f'got invalid value "{val}" with less than {self.min_words} words')
                return False
            else:
                return True
        elif self.prevent_apostrophe or self.max_length or self.prevent_chars or self.min_words:
            assert hasattr(val, 'faker_var_value_is_valid')
            return val.faker_var_value_is_valid(self)
        else:
            return True

    def get(self, fake, args):
        for i in range(500):
            val = getattr(fake, self.method)(*args, **self.kwargs)
            if self.is_valid(val):
                return self.post_get(val)
        raise Exception(f'Could not generate valid value within 50 random tries\n' + "\n".join(self._log))

    def post_get(self, val):
        if self.chars_reverse:
            assert isinstance(val, str)
            val = val[::-1]
        if self.post_get_callback:
            val = self.post_get_callback(val)
        return val
