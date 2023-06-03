import urllib.request

for i in range(2013, 2019):
    for j in range(1, 13):
        url = f'http://naq.cicidata.top:10443/chinavis/opendata/download/daily/CN-Reanalysis{i}{j:02d}.zip'
        urllib.request.urlretrieve(url, f'CN-Reanalysis{i}{j:02d}.zip')

for i in range(2013, 2019):
        url = f'http://naq.cicidata.top:10443/chinavis/opendata/download/hourly/CN-Reanalysis-hourly{i}01.zip'
        urllib.request.urlretrieve(url, f'CN-Reanalysis-hourly{i}01.zip')
