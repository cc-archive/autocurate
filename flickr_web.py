import web

import autocurate_flickr

urls = (
    '/make_zip', 'MakeZip',
    '/grab_zip', 'GrabZip'
)

class MakeZip(object):
    def GET(self):
        return autocurate_flickr.main()

class GrabZip(object):
    def GET(self):
        print autocurate_flickr.return_tar()

if __name__ == "__main__":
    web.run(urls, globals())
