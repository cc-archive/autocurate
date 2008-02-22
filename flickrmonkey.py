# Do hilarious monkey patching to work around Flickr bad Unicode
import xml.dom.expatbuilder
import xml.dom.minidom
import xml.parsers.expat
import BeautifulSoup

old_parseString = xml.dom.expatbuilder.ExpatBuilder.parseString

def is_valid_xml(maybe_valid):
    try:
        parsed = xml.dom.minidom.parseString(maybe_valid)
        return True
    except xml.parsers.expat.ExpatError:
        return False

def new_parseString(self, string):
    if is_valid_xml(string):
        return old_parseString(self, string)
    else:
        print "FYI, Asheesh's parseString"
        soup = BeautifulSoup.BeautifulStoneSoup(string)
        soup_hacked_string = str(soup)

        # post soup, no need to fix unicode    
        # But some attribs might have evil ampersand nonsense
        # Can't do this in a try-except because the parser object
        # maintains state, so you only get one shot.

        # Fix up attribs on photo elements
        if not is_valid_xml(soup_hacked_string):
            for photo in soup('photo'):
                for key in photo.attrMap:
                    if '&' in photo[key]:
                        cleaned = photo[key].replace('&', '&amp;')
                        photo[key] = cleaned
                        print 'FYI, Asheesh cleaned', key, 'in', photo['id']
            soup_hacked_string = str(soup)
        
    return old_parseString(self, soup_hacked_string)

xml.dom.expatbuilder.ExpatBuilder.parseString = new_parseString
