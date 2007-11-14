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
    b.open(u)
    if b.geturl() != u:
        return True
    return False

def main_returns():
    top = myflickr.flickr.interestingness_getList(api_key=myflickr.api_key,per_page='500')
    
    # top
    top_photos = top.photos[0].photo
    top_ids = [photo.attrib['id'] for photo in top_photos]
    top_flickrphotos = [ myflickr.photoid2flickrphoto(id) for id in top_ids]

    top_non_arr_flickrphotos  = [p for p in top_flickrphotos if p.attrib['license'] != '0' ]
    top_non_arr_flickr_urls = [biggest_possible_url(p) for p in top_non_arr_flickrphotos]
    return top_non_arr_flickr_urls # I have thrown away the license metadata

def main():
    print '\n'.join(main_returns())

if __name__ == '__main__':
    main()
