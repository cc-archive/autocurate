class Autocurated:
    def __str__(self):
        assert '\t' not in self.attribution_string + self.url + self.license_uri # would violate format
        return '\t'.join( (self.url, self.license_uri, self.attribution_string))
    def __init__(self, url = None, attribution_string = '', license_uri = None):
        self.url = url
        self.attribution_string = attribution_string
        self.license_uri = license_uri

