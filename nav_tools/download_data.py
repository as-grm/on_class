import wget

url_01 = 'http://maia.usno.navy.mil/ser7/finals2000A.all'
url_02 = 'http://toshi.nofs.navy.mil/ser7/finals2000A.all'
url_03 = 'ftp://cddis.gsfc.nasa.gov/pub/products/iers/finals2000A.all'
url_04 = 'https://datacenter.iers.org/data/9/finals2000A.all'

wget.download(url_04)