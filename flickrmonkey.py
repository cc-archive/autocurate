# Do hilarious monkey patching to work around Flickr bad Unicode
import xml.dom.expatbuilder
import xml.parsers.expat
import BeautifulSoup

old_parseString = xml.dom.expatbuilder.ExpatBuilder.parseString

def new_parseString(self, string):
    print "FYI, Asheesh's parseString"
    soup = BeautifulSoup.BeautifulStoneSoup(string)
    soup_hacked_string = str(soup)

    # post soup, no need to fix unicode    
    
    return old_parseString(self, soup_hacked_string)
#    except xml.parsers.expat.ExpatError, e:
#        print "FYI, Asheesh's workaround"
#        lines = string.split('\n')
#        lines = [thing.strip() for thing in lines]

        # Have faith that <note>s are the problem
#        line = lines[e.lineno - 1].strip()
#        assert (line.startswith('<note') and line.endswith('</note>')) # screw it
#        non_note_lines = [line for line in thing if not (line.startswith('<note>') and line.endwith('</note>'))]
#        fixed_string = '\n'.join(non_note_lines)
        #fixed_string = unicode(string, 'utf-8', 'replace').encode('utf-8')
#        return old_parseString(self, fixed_string)

xml.dom.expatbuilder.ExpatBuilder.parseString = new_parseString

