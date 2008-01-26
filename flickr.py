import autocurate
import sys
import rose.myflickr as myflickr
import string
import mechanize

def photo2url(photo, photo_size="original"):
    ''' Input: a Flickr Photo.  Output: a URL for a photo!'''
    d = photo.__dict__
    size = {'75x75': '_s', 'thumbnail': '_t', 'small': '_m', 'medium': '', 'large': '_b', 'original': '_o'}
    t =string.Template('http://farm${farm}.static.flickr.com/${server}/${id}_${secret}%s.jpg' % size[photo_size])
    return t.substitute(d['attrib'])

def biggest_possible_url(photo):
    for size in ['original', 'large', 'medium', 'small']:
        url = photo2url(photo, photo_size=size)
        if not url_is_unavailable(url):
            return url
    raise Exception

def url_is_unavailable(u):
    b = mechanize.Browser()
    try: # catch the 404
        b.open(u)
    except mechanize.HTTPError, e:
        return True

    if b.geturl() != u:
        return True
    return False

def flickr_photo2attribstring(photo):
    data = photo.owner[0].attrib
    order = ['realname', 'username']
    for key in order:
        if key in data:
            return data[key]
    return data['nsid'] + "on Flickr.com"

def main_returns():
    top = myflickr.flickr.interestingness_getList(api_key=myflickr.api_key,per_page='500')
    
    # top
    top_photos = top.photos[0].photo
    top_ids = [photo.attrib['id'] for photo in top_photos]
    top_flickrphotos = [ myflickr.photoid2flickrphoto(id) for id in top_ids]
    top_flickrphotos = [k for k in top_flickrphotos if k is not None]

    top_non_arr_flickrphotos  = [p for p in top_flickrphotos if p.attrib['license'] != '0' ]
    top_non_arr_flickr_urls_with_licenses = [(biggest_possible_url(p), myflickr.licensenum2licenseurl(p.attrib['license']), flickr_photo2attribstring(p)) for p in top_non_arr_flickrphotos]

    return [autocurate.Autocurated(url = thing[0], 
                                   license_uri = thing[1],
                                   attribution_string=thing[2])
            for thing in top_non_arr_flickr_urls_with_licenses]

def main():
    data = main_returns()
    autocurateds2directory('auto_flickr')
    print 'flickr.py: success!'

def failsafe(fn):
    def inner_fn(*args, **kwargs):
        try:
            fn(*args, **kwargs)
        except Exception, e:
            print >> sys.stderr, e
            return None # Sad
    return inner_fn

if __name__ == '__main__':
    main()
