#!/usr/bin/python

import urllib2, json, sys, string, csv

def main(query):
    baseUrl = 'http://beta.ginetwork.org/GINetworkAPI/search?query=' + query
    baseUrl += '&providers-per-page=100'
    with open('csv/GINetwork_' + query + '.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'Provider',
            'Email',
            'Name',
            'Phone',
            'Title',
            'Website',
            'Street',
            'City',
            'Postal Code',
            'Associated with',
            'Description',
            'Latitude',
            'Longitude',
            'EIN',
            'State',
            'EIN ID'
        ])
        for index in range(100000):
            url = baseUrl + '&start-at-page=' + str(index)
            data = json.loads(urllib2.urlopen(url, timeout=60).read())
            result = data['giNetworkProvider']
            if len(result) == 0:
                break
            for item in result:
                contact = item['contactInformation']
                person = contact['contactPerson']
                address = contact['physicalAddress']
                if address['state'] != query:
                    continue
                writer.writerow([
                    item['name'],
                    contact['webAddresses']['email'],
                    person['firstName'] + ' ' + person['lastName'],
                    contact['phoneNumbers']['phone1'],
                    person['title'],
                    contact['webAddresses']['url'],
                    address['addressLine1'] + ' ' + address['addressLine2'],
                    address['city'],
                    address['zipCode'],
                    '',
                    item['description'],
                    address['latitude'],
                    address['longitude'],
                    item['ein'],
                    address['state'],
                    item['ein'].replace('-', '')
                ])

if __name__ == '__main__':
    query = 'TX'
    if len(sys.argv) > 1:
        query = sys.argv[1]
    main(query)
