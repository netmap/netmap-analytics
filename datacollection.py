import urllib, json, math
from decimal import Decimal
d = 0
pagecount = 0
fdata = {}
while(d != -1):
  url = "http://netmap-data.pwnb.us/readings/above/" + str(d)
  response = urllib.urlopen(url);
  data = json.loads(response.read())
  #data is the array of data collected from url above
  if(data == []):
    d =-1
  else:
    #x iterates through serial numbers (each serial number is one set of measurements)
    #data[x] is a dictionary for that measurement set and ['data'] is relevant data dictionary and then [location] gives long and lat in dictionary
    
    #add first key on first run
    if (pagecount == 0):
      floc = data[0]['data']['location']
      fnew_key = str(round(floc['longitude'],2)) + "," + str(round(floc['latitude'],2))
      fdata[fnew_key] = []
      fdata[fnew_key].append(data[0]['data'])
    pagecount = pagecount + 1
    for x in xrange(1, len(data)-1):
      loc = data[x]['data']['location']
      for k in fdata:
	l = k.split(',')
        #lo is longitude for that reading, la is latitude for that reading (both in decimal)
	lo = Decimal(l[0])
	la = Decimal(l[1])
        print k
        #if lo and la are within 0.01 of previous entry, then combine with it. else make a new one
	if (math.fabs(round(loc['longitude'],2) - lo) < 0.01 and math.fabs(round(loc['latitude'],2) - la) < 0.01):
          fdata[k].append(data[x]['data'])
	else:
	  new_key = str(round(loc['longitude'],2)) + "," + str(round(loc['latitude'],2))
	  fdata[new_key] = []
	  fdata[new_key].append(data[x]['data']) 
          #fdata[new_key] = [data[x]['data']] 
  #d now gets updated to last serial number of previous page to get the next data page (next data array)
  d1 =  data[len(data)-1]
  d = d1['serial']

# I now have dictionary where keys are long, lat strings and values for each are array of dictionaries (only the data part) for
# all entries that fit in the same location area. Now I must, for each key (location), average the necessary
# values from all dictionaries listed in that location and then create a final dictionary where keys are again 
# the locations, and the values are now the final dictionary of the averaged relevant values (key is value description and value is avg (eg. latency: 5))

senddata = {}

for lkey in fdata:
  #count = 0
  latencytotal = 0.0
  rtttotal = 0.0
  #fdata is dictionary where locations are keys and values are arrays of dictionaries of data for that location
  #for inkey inffdata[lkey]:
  for inkey in xrange(0, len(fdata[lkey])-1): 
    #latencytotal = latencytotal + float(inkey['latency'])
    latencytotal = latencytotal + float(fdata[lkey][inkey]['latency'])
    #rtttotal = rtttotal + float(inkey['rtt'])
    rtttotal = rtttotal + float(fdata[lkey][inkey]['rtt'])
    #CAN DO THIS FOR ANY METRIC (which is key of data)
    #count = count + 1  
  #if len(fdata[lkey]) doesn't work, uncomment count above and replace with count
  totdat = {}
  totdat['latency'] = latencytotal/len(fdata[lkey])
  totdat['rtt'] = rtttotal/len(fdata[lkey])
  senddata[lkey] = {}
  senddata[lkey] = totdat


#senddata is the final dictionary with keys as long,lat and values as dictionaries (one per location) with keys as latency, rtt, etc. and values as the final values.
