# Pre-seeder

![data mining](https://media.tenor.com/q5eSKo33o3wAAAAd/planting-linus-van-pelt.gif)

**Prepare**<br />
```
pyasn_util_download.py --latest && pyasn_util_convert.py --single rib.202* asn.dat
wget https://yammdb.serv.app/geo.mmdb
```

**Run**<br />
```
python3 seed.py
```