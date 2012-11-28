import fileinput
import re

KEY_VAL_RE = re.compile(r'(?P<key>.*?):( (?P<value>.*))?')

class Changes(dict):
    def __init__(self, path):
        super(Changes, self).__init__()

        self.path = path

        self.parse_changes(self.path)

        self._files = None

    @property
    def files(self):
        if self._files:
            return self._files

        self._files = []
        for item in self['Files']:
          md5, size, section, priority, filename = item.strip().split()
          changes_file = ChangesFile(md5=md5, size=size, priority=priority, filename=filename)

          self._files.append(changes_file)

        return self._files

    def parse_changes(self, path):
        info = None

        for line in fileinput.input(path):
            line = line.rstrip()

            # ignore PGP header
            if line in ('', '-----BEGIN PGP SIGNED MESSAGE-----'):
                continue

            # skip the signature altogether
            if line == '-----BEGIN PGP SIGNATURE-----':
                break

            if line.startswith(' ') and info:
                info['value'].append(line.strip())

            matches = KEY_VAL_RE.match(line)
            if matches:
                if info:
                    self.finalize_item(info)

                info = matches.groupdict()
                if info['value'] is None:
                    info['value'] = []
        fileinput.close()

        if info:
          self.finalize_item(info)

    def finalize_item(self, info):
        self[info['key']] = info['value']

class ChangesFile(object):
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)

    def __str__(self):
        return self.filename
    def __unicode__(self):
        return self.filename
