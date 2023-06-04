import subprocess, geoip2.database, netaddr, pyasn

def networkToSubs(subnet):
    sub, prefix = subnet.split("/")
    if int(prefix) > 22: return [subnet]
    network = netaddr.IPNetwork(subnet)
    return [str(sn) for sn in network.subnet(23)]

print("Microsoft: 8075, AWS: 16509")
asns = input("Please input asn numbers, eg. 3000,4000: ")
asns = asns.split(",")

countries = input("Please enter target continents, e.g AS, EU, NA: ")
countries = countries.split(",")

ips = []
print("Building list")
reader = geoip2.database.Reader("geo.mmdb")
with open('asn.dat') as file:
    for line in file:
        if ";" in line: continue
        line = line.rstrip()
        subnet, asn = line.split("\t")
        if asn in asns:
            subs = networkToSubs(subnet)
            for sub in subs:
                ip, prefix = sub.split("/")
                ip = ip[:-1]
                ip = f"{ip}1"
                try:
                    response = reader.city(ip)
                    if response.continent.code in countries:
                        ips.append(ip)
                except:
                    pass

print("Seeding...")
batchSize,count,pings = 1000,0,1
while count <= len(ips):
    print(f"fping {count} of {len(ips)}")
    batch = ' '.join(ips[count:count+batchSize])
    if not batch: break
    p = subprocess.run(f"fping -c {pings} {batch}", stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if not p.stdout.decode('utf-8'):
        print("Please install fping (apt-get install fping / yum install fping)")
        exit()
    count += batchSize