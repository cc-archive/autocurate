import urllib2
import os
import codecs
import datetime

#def unicode2filename(u):
#    return urllib.quote(u.encode('utf-8'))

class Autocurated:
    def __str__(self):
        assert '\t' not in self.attribution_string + self.url + self.license_uri # would violate format
        return '\t'.join( (self.url, self.license_uri, self.attribution_string))
    def __init__(self, url = None, attribution_string = '', license_uri = None):
        self.url = url
        self.attribution_string = attribution_string
        self.license_uri = license_uri

def int_log_10(n):
    # This sucks, but math.log(1000, 3) returns 2.something not 3.0
    ret = 0
    while n > (10 ** ret):
        ret += 1
    return ret

def save_url_to_filename(url, filename):
    # Byte stream - uses raw open()
    out_fd = open(filename, 'w')
    in_fd = urllib2.urlopen(url)
    s = in_fd.read()
    out_fd.write(s)
    out_fd.close()

def data2numberformat(data):
    length = len(data)
    length_log_10 = int_log_10(length)
    return '%0' + str(length_log_10) + 'd'

def thing2filename(thing, num_format, num):
    formatted_num = num_format % num

    base = thing.url.split('/')[-1]
    parts = base.rsplit('.', 1)
    parts[1:1] = [formatted_num]
    return '.'.join(parts)

def write_metadata_file(thing, filename):
    fd = codecs.open(filename, 'w', 'utf-8') # text file - uses codecs
    print >> fd, 'License:', thing.license_uri
    print >> fd, 'Author:', thing.attribution_string
    fd.close()

def autocurateds2directory(data, directory):
    if os.path.exists(directory):
        os.rename(directory, directory + '.old.' + datetime.datetime.now().strftime('%s'))
    os.makedirs(directory, mode=0755)
    os.makedirs(directory + '/credits', mode=0755)
    os.chdir(directory)

    num_format = data2numberformat(data)
    
    for num, thing in enumerate(data):
        filename = thing2filename(thing, num_format, num)
        # save it
        save_url_to_filename(thing.url, filename)
        # write metadata file
        write_metadata_file(thing, 'credits/' + filename)
