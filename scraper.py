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
from multiprocessing.dummy import Pool as ThreadPool
import urllib
from concurrent.futures import ThreadPoolExecutor
from fork import fork


def parse_data(row):
    results = {}
    location_url = row[12].replace('https://admin.cqc.org.uk', 'http://www.cqc.org.uk')
    # print location_url
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
        report_date = report_soup.xpath('//div[@class="overview-inner latest-report"]/h3/text()')[0]
    except:
        pass
    overview = ''
    try:
        overview = report_soup.xpath('//div[@class="overview-inspections"]//h3/strong/text()')[0]
    except:
        try:
            overview = report_soup.xpath('//div[@class="header-wrapper"]//h2/text()')[0]
        except:
            pass
    overview_description = ''
    try:
        overview_description = report_soup.xpath('//h3[@class="accordion-title"]/following-sibling::div//text()')[0]
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
        overview_summary_url = report_soup.xpath('//a[text()="Read overall summary"]/@href')[0]
    except:
        pass
    overview_summary = summary_safe = summary_effective = summary_caring = summary_responsive = summary_well_led = summary_treating_people_with_respect = summary_providing_care = summary_caring_for_people_safely = summary_staffing = summary_quality_and_suitability_of_management = ''
    if overview_summary_url:
        overview_summary_url = location_url+'/inspection-summary'
        overview_summary_soup = connect(overview_summary_url)
        overview_summary = overview_summary_soup.xpath('//div[@id="overall"]//text()')
        try:
            summary_safe = overview_summary_soup.xpath('//div[@id="safe"]//text()')
        except:
            pass
        try:
            summary_effective = overview_summary_soup.xpath('//div[@id="effective"]//text()')
        except:
            pass
        try:
            summary_caring = overview_summary_soup.xpath('//div[@id="caring"]//text()')
        except:
            pass
        try:
            summary_responsive = overview_summary_soup.xpath('//div[@id="responsive"]//text()')
        except:
            pass
        try:
            summary_well_led = overview_summary_soup.xpath('//div[@id="wellled"]//text()')
        except:
            pass

    else:
        overview_summary_url = location_url+'/inspection-summary'
        overview_summary_soup = connect(overview_summary_url)

        try:
            summary_treating_people_with_respect = overview_summary_soup.xpath('//div[@id="CH1"]/ol//text()')
        except:
            pass

        try:
            summary_providing_care = overview_summary_soup.xpath('//div[@id="CH2"]/ol//text()')
        except:
            pass

        try:
            summary_caring_for_people_safely = overview_summary_soup.xpath('//div[@id="CH3"]/ol//text()')
        except:
            pass

        try:
            summary_staffing = overview_summary_soup.xpath('//div[@id="CH4"]/ol//text()')
        except:
            pass
        try:
            summary_quality_and_suitability_of_management = overview_summary_soup.xpath('//div[@id="CH5"]/ol//text()')
        except:
            pass
    l = [location_url, name, add1, add2, add3, add4,  postal_code, telephone, cqc_id, type_of_service, services, local_authority, latest_report, reports_url, report_date, overview, overview_description, overview_safe, overview_effective,
                                                                 overview_caring, overview_responsive, overview_well_led, run_by, run_by_url, overview_summary, summary_safe, summary_effective, summary_caring, summary_responsive,
                                                                 summary_well_led, summary_treating_people_with_respect, summary_providing_care, summary_caring_for_people_safely, summary_staffing, summary_quality_and_suitability_of_management]
    print name
    results.setdefault(location_url,[]).append(l)
    return results

    # return location_url, name, add1, add2, add3, add4,  postal_code, telephone, cqc_id, type_of_service, services, local_authority, latest_report, reports_url, report_date, overview, overview_description, overview_safe, overview_effective,\
    #                                                  overview_caring, overview_responsive, overview_well_led, run_by, run_by_url, overview_summary, summary_safe, summary_effective, summary_caring, summary_responsive,\
    #                                                  summary_well_led, summary_treating_people_with_respect, summary_providing_care, summary_caring_for_people_safely, summary_staffing, summary_quality_and_suitability_of_management



def connect(url):
    report_tree = ''
    try:
        report_html = requests.get(url, timeout = 90)
        report_tree = etree.HTML(report_html.text)
    except:
        print url
        return connect(url)
    if not report_tree:
        return connect(url)
    else:
        return report_tree

directoryUrl = "http://www.cqc.org.uk/content/how-get-and-re-use-cqc-information-and-data#directory"

soup = connect(directoryUrl)

csvUrl = soup.xpath('//div[@id="directory"]//a/@href')[0]

response = urllib.urlretrieve(csvUrl)

with open(response[0], 'rb') as csvfile:
    csv_file = csv.reader(csvfile, delimiter=',')
    next(csv_file)
    next(csv_file)
    next(csv_file)
    next(csv_file)
    next(csv_file)
    for res in csv_file:
        results = fork(parse_data, res)
        # print results
        for result in results:
            print result[0]
        #     scraperwiki.sqlite.save(unique_keys=['location_url'], data={"location_url": result[0], "name": unicode(result[1]), "add1": unicode(result[2]), "add2": unicode(result[3]), "add3": unicode(result[4]), "add4": unicode(result[5]),
        #                                                                 "postal_code": unicode(result[6]), "telephone": unicode(result[7]), "CQC_ID": result[8], "type_of_service": unicode(result[9]), "services": unicode(result[10]), "local_authority": unicode(result[11]), "latest_report": unicode(result[12]), "reports_url": unicode(result[13]),
        #                                                  "report_date": unicode(result[14]), "overview": unicode(result[15]), "overview_description": unicode(result[16]), "overview_safe": unicode(result[17]), "overview_effective": unicode(result[18]),
        #                                                  "overview_caring": unicode(result[19]), "overview_responsive": unicode(result[20]), "overview_well_led": unicode(result[21]), "run_by": unicode(result[22]), "run_by_url": unicode([23]),
        #                                                  "overview_summary": unicode(result[24]), "summary_safe": unicode(result[25]), "summary_effective": unicode(result[26]), "summary_caring": unicode(result[27]), "summary_responsive": unicode(result[28]),
        #                                                  "summary_well_led": unicode(result[29]), 'summary_treating_people_with_respect': unicode(result[30]), 'summary_providing_care': unicode(result[31]), 'summary_caring_for_people_safely': unicode(result[32]), 'summary_staffing': unicode(result[33]), 'summary_quality_and_suitability_of_management': unicode(result[34])
        #                                                  })
