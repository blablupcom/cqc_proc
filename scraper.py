# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import scraperwiki
import urllib2
from datetime import datetime
import csv
from lxml import etree
import requests

def connect(url):
    #print url
    report_tree = ''
    try:
        report_html = requests.get(url)
        report_tree = etree.HTML(report_html.text)
    except:
        print url
        connect(url)
    if not report_tree:
        connect(url)
    else:
        return report_tree

directoryUrl = "http://www.cqc.org.uk/content/how-get-and-re-use-cqc-information-and-data#directory"

soup = connect(directoryUrl)

csvUrl = soup.xpath('//div[@id="directory"]//a/@href')[0]
# csvA = block.find('a',href=True)
# csvUrl = csvA['href']
print csvUrl
response = urllib2.urlopen(csvUrl)
csv_file = csv.reader(response)
p = 0
for row in csv_file:
    if 'http' not in row[12]:
        continue
    print p
    location_url = row[12].replace('https://admin.cqc.org.uk', 'http://www.cqc.org.uk')
    name = row[0]
    add1 = ' '.join(row[2].split(',')[:-1])
    add2 = row[2].split(',')[-1]
    add3 = row[10]
    add4 = row[11]
    postal_code = row[3]
    telephone = row[4]
    type_of_service = row[6]
    services = row[8]
    local_authority = row[11]
    cqc_id = row[14]

    report_soup = connect(location_url)
    latest_report_url = location_url+'/reports'
    latest_report_soup = connect(latest_report_url)

    latest_report = ''
    try:
        latest_report = latest_report_soup.xpath('//span[@class="visit-date"]/text()')[0].strip() + ' '+ latest_report_soup.xpath('//div[@class=""]//p/text()')[0].strip()
    except:
        pass
    reports_url = ''
    try:
        reports_url = report_soup.xpath('//div[@class="overview-inner latest-report"]//li/following-sibling::li//a/@href')[0]
    except:
        pass
    if 'pdf' not in reports_url:
        reports_url = ''
        try:
            if 'http' not in report_soup.xpath('//a[text()="Read CQC inspection report online"]/@href')[0]:
                reports_url = 'http://www.cqc.org.uk'+report_soup.xpath('//a[text()="Read CQC inspection report online"]/@href')[0]
            else:
                reports_url = report_soup.xpath('//a[text()="Read CQC inspection report online"]/@href')[0]
        except:
            pass
    report_date = ''
    try:
        report_date = report_soup.find('div', 'overview-inner latest-report').find('h3').text.strip()
    except:
        pass
    overview = ''
    try:
        overview = report_soup.find('div', 'overview-inspections').find('h3').find('strong').text.strip()
    except:
        try:
            overview = report_soup.find('div', 'header-wrapper').find('h2').text.strip()
        except:
            pass
    overview_description = ''
    try:
        overview_description = report_soup.find('h3', 'accordion-title').find_next('div', 'accordion-wrapper').text.strip()
    except:
        pass
    overview_safe = ''
    try:
        overview_safe = report_soup.xpath('//ul[@class="inspection-results new-inspection"]//a[text()="Safe"]/following-sibling::span/text()')[0]
    except:
        pass
    overview_effective = ''
    try:
        overview_effective = report_soup.xpath('//ul[@class="inspection-results new-inspection"]//a[text()="Effective"]/following-sibling::span/text()')[0]
    except:
        pass
    overview_caring = ''
    try:
         overview_caring = report_soup.xpath('//ul[@class="inspection-results new-inspection"]//a[text()="Caring"]/following-sibling::span/text()')[0]
    except:
        pass
    overview_responsive = ''
    try:
        overview_responsive = report_soup.xpath('//ul[@class="inspection-results new-inspection"]//a[text()="Responsive"]/following-sibling::span/text()')[0]
    except:
        pass
    overview_well_led = ''
    try:
        overview_well_led = report_soup.xpath('//ul[@class="inspection-results new-inspection"]//a[text()="Well-led"]/following-sibling::span/text()')[0]
    except:
        pass
    run_by = ''
    try:
        run_by = report_soup.xpath('//h3[text()="Who runs this service"]/following-sibling::p/a/text()')[0]
    except:
        pass
    run_by_url = ''
    try:
        if 'http' not in report_soup.xpath('//h3[text()="Who runs this service"]/following-sibling::p/a/@href')[0]:
            run_by_url = 'http://www.cqc.org.uk'+report_soup.xpath('//h3[text()="Who runs this service"]/following-sibling::p/a/@href')[0]
        else:
            run_by_url = report_soup.xpath('//h3[text()="Who runs this service"]/following-sibling::p/a/@href')[0]
    except:
        pass
    overview_summary_url = ''
    try:
        if 'http' not in report_soup.xpath('//a[text()="Read overall summary"]/@href')[0]:
            overview_summary_url = 'http://www.cqc.org.uk'+report_soup.xpath('//a[text()="Read overall summary"]/@href')[0]
        else:
            overview_summary_url = report_soup.xpath('//a[text()="Read overall summary"]/@href')[0]
    except:
        pass
    overview_summary = summary_safe = summary_effective = summary_caring = summary_responsive = summary_well_led = ''
    if overview_summary_url:
        # overview_summary_page = urllib2.urlopen(overview_summary_url)
        # overview_summary_soup = BeautifulSoup(overview_summary_page, 'lxml')
        overview_summary_soup = connect(overview_summary_url)
        overview_summary = ' '.join(overview_summary_soup.xpath('//div[@id="overall"]//text()'))
    # summary_safe_url = ''
    # try:
    #     if 'http' not in report_soup.find('a', text=re.compile('\\bSafe\\b'))['href']:
    #         summary_safe_url = 'http://www.cqc.org.uk'+report_soup.find('a', text=re.compile('\\bSafe\\b'))['href']
    #     else:
    #         summary_safe_url = report_soup.find('a', text=re.compile('\\bSafe\\b'))['href']
    # except:
    #     pass
    # summary_safe = ''
    # if summary_safe_url and '#safe' in summary_safe_url:
    #     # summary_safe_page = urllib2.urlopen(summary_safe_url)
    #     # summary_safe_soup = BeautifulSoup(summary_safe_page, 'lxml')
    #     summary_safe_soup = connect(summary_safe_url)
        try:
            summary_safe = ' '.join(overview_summary_soup.xpath('//div[@id="safe"]//text()'))
        except:
            summary_safe = ''
    # summary_effective_url = ''
    # try:
    #     if 'http' not in report_soup.find('a', text=re.compile('\\bEffective\\b'))['href']:
    #         summary_effective_url = 'http://www.cqc.org.uk'+report_soup.find('a', text=re.compile('\\bEffective\\b'))['href']
    #     else:
    #         summary_effective_url = report_soup.find('a', text=re.compile('\\bEffective\\b'))['href']
    # except:
    #     pass
    # # print summary_effective_url
    # summary_effective = ''
    # if summary_effective_url:
    #     # summary_effective_page = urllib2.urlopen(summary_effective_url)
    #     # summary_effective_soup = BeautifulSoup(summary_effective_page, 'lxml')
    #     summary_effective_soup =connect(summary_effective_url)
        try:
            summary_effective = ' '.join(overview_summary_soup.xpath('//div[@id="effective"]//text()'))
        except:
            summary_effective = ''
    # summary_caring_url = ''
    # try:
    #     caring_url_check = report_soup.find('a', text=re.compile('\\bCaring\\b'))['href']
    #     if '#caring' in caring_url_check:
    #         if 'http' not in report_soup.find('a', text=re.compile('\\bCaring\\b'))['href']:
    #             summary_caring_url = 'http://www.cqc.org.uk'+report_soup.find('a', text=re.compile('\\bCaring\\b'))['href']
    #         else:
    #             summary_caring_url = report_soup.find('a', text=re.compile('\\bCaring\\b'))['href']
    # except:
    #     pass
    # summary_caring = ''
    # if summary_caring_url:
        # summary_caring_page = urllib2.urlopen(summary_caring_url)
        # summary_caring_soup = BeautifulSoup(summary_caring_page, 'lxml')
        # summary_caring_soup = connect(summary_caring_url)
        try:
            summary_caring = ' '.join(overview_summary_soup.xpath('//div[@id="caring"]//text()'))
        except:
            summary_caring = ''
    # summary_responsive_url = ''
    # try:
    #     if 'http' not in report_soup.find('a', text=re.compile('Responsive'))['href']:
    #         summary_responsive_url = 'http://www.cqc.org.uk'+report_soup.find('a', text=re.compile('Responsive'))['href']
    #     else:
    #         summary_responsive_url = report_soup.find('a', text=re.compile('Responsive'))['href']
    # except:
    #     pass
    # summary_responsive = ''
    # if summary_responsive_url:
    #     # summary_responsive_page = urllib2.urlopen(summary_responsive_url)
    #     # summary_responsive_soup = BeautifulSoup(summary_responsive_page, 'lxml')
    #     summary_responsive_soup = connect(summary_responsive_url)
        try:
            summary_responsive = ' '.join(overview_summary_soup.xpath('//div[@id="responsive"]//text()'))
        except:
            summary_responsive = ''
    # summary_well_led_url = ''
    # try:
    #     if 'http' not in report_soup.find('a', text=re.compile('Well-led'))['href']:
    #         summary_well_led_url = 'http://www.cqc.org.uk'+report_soup.find('a', text=re.compile('Well-led'))['href']
    #     else:
    #         summary_well_led_url = report_soup.find('a', text=re.compile('Well-led'))['href']
    # except:
    #     pass
    # summary_well_led = ''
    # if summary_well_led_url:
    #     summary_well_led_soup = connect(summary_well_led_url)
        try:
            summary_well_led = ' '.join(overview_summary_soup.xpath('//div[@id="wellled"]//text()'))
        except:
            summary_well_led = ''
    scraperwiki.sqlite.save(unique_keys=['location_url'], data={"location_url": location_url, "name": unicode(name), "add1": unicode(add1), "add2": unicode(add2), "add3": unicode(add3), "add4": unicode(add4), "postal_code": unicode(postal_code), "telephone": unicode(telephone),
                                                     "CQC_ID": cqc_id, "type_of_service": unicode(type_of_service), "services": unicode(services), "local_authority": unicode(local_authority), "latest_report": unicode(latest_report), "reports_url": unicode(reports_url),
                                                     "report_date": unicode(report_date), "overview": unicode(overview), "overview_description": unicode(overview_description), "overview_safe": unicode(overview_safe), "overview_effective": unicode(overview_effective),
                                                     "overview_caring": unicode(overview_caring), "overview_responsive": unicode(overview_responsive), "overview_well_led": unicode(overview_well_led), "run_by": unicode(run_by), "run_by_url": unicode(run_by_url),
                                                     "overview_summary": unicode(overview_summary), "summary_safe": unicode(summary_safe), "summary_effective": unicode(summary_effective), "summary_caring": unicode(summary_caring), "summary_responsive": unicode(summary_responsive),
                                                     "summary_well_led": unicode(summary_well_led)
                                                     })
    p+=1
