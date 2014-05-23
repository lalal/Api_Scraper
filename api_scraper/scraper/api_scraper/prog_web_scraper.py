import BeautifulSoup as bs
import urllib2 as lib2
from optparse import OptionParser
from django.db.models import Q
from scraper.api_scraper.models import Details

def scraper(page=0):
    scraper_list = []
    api_url = "http://programmableweb.com/apis/directory"
    if page != 0:
        api_url = '%s?page=%s' % (api_url, page)
    try:
        response = lib2.urlopen(api_url)
        soup = bs.BeautifulSoup(response.read())
    except Exception, e:
        print "Caught an exception retrieving API Page: %s" % e

    table = soup.find('table')
    for i in table.findAll('tr'):
        query = Q()
        for s in i.findAll('a'):
            if 'api' in s.get('href') and 'directory?order' not in s.get('href'):
                entry_dict = {}
                print 'href = %s, text = %s' % (s.get('href'), s.text)
                entry_dict['API Company'] = s.text
                query &= Q(company=s.text)
                spec = 'http://programmableweb.com%s' % s.get('href')
                try:
                    spec_resp = lib2.urlopen(spec)
                except:
                    print "An issue occured trying to open %s" % spec
                    continue
                soup_rec = bs.BeautifulSoup(spec_resp.read())
                for div in soup_rec.findAll('div'):
                    if div.get('class') == 'field':
                        label = div.find('label')
                        if label.text == 'API Homepage':
                            entry_dict['API Homepage'] = div.find('a').text
                            query &= Q(homepage=entry_dict['API Homepage'])
                            print div.find('a').text
                        elif label.text == 'Primary Category':
                            entry_dict['Primary Category'] = div.find('a').text
                            query &= Q(category=entry_dict['Primary Category'])
                        elif label.text == 'API Provider':
                            entry_dict['API Provider Page'] = div.find('a').text
                            query &= Q(provider=entry_dict['API Provider Page'])
        print query
        created = False
        det = Details.objects.filter(query)
        if det.count() == 0:
            created = True
        if created:
            try:
                new_det = Details()
                new_det.company = entry_dict.get('API Company', None)
                new_det.provider = entry_dict.get('API Provider Page', None)
                new_det.category = entry_dict.get('Primary Category', None)
                new_det.homepage = entry_dict.get('API Homepage', None)
                new_det.save()
            except Exception, e:
                print "Caught an exception trying to save new detail: %s" % e
        else:
            print "Entry has already been created: %s" % det
        
    return scraper_list

if __name__ == '__main__':
    parser = OptionParser()

    parser.add_option("-p", "--page_num", dest="page",
                      default=-1,
                      help="Which page number of programmable web to target")

    (options, args) = parser.parse_args()
    page = options.page
    page = int(page)
    if page >= 0:
            try:
                scraper_list = scraper(page)
            except Exception, e:
                print "Caught an exception scraping: %s" % e        
    else:
        for i in range(0,100):
            try:
                scraper_list = scraper(i)
            except Exception, e:
                print "Caught an exception scraping: %s" % e