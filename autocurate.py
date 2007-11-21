class Autocurated:
    url = None
    attribution_string = None
    license_uri = None
    def __str__(self):
        assert '\t' not in self.attribution_string # would violate format
        return '\t'.join( (self.url, self.license_uri, self.attribution_string))
    def __init__(self, url = None, attribution_string = None, license_uri = None):
        if url is not None:
            self.url = url
        if attribution_string is not None:
            self.attribution_string
        if license_uri is not None:
            self.license_uri = license_uri

