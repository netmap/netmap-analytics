import urllib, json, math
from decimal import Decimal
d = 0
dcount = 0
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
    #find first serial number which has 'location'
    dcount = 0
    stopval = 0
    while(stopval == 0 and dcount < len(data)):
      if ('location' in data[dcount]['data'] and 'ndt' in data[dcount]['data'] and 'bw' in data[dcount]['data']['ndt'] and 'avgrtt' in data[dcount]['data']['ndt']):
        dc = dcount
        stopval = 1
      dcount = dcount + 1 
    #add first key on first run
    if (pagecount == 0):
      floc = data[dc]['data']['location']
      fnew_key = str(round(floc['longitude'],2)) + "," + str(round(floc['latitude'],2))
      fdata[fnew_key] = []
      fdata[fnew_key].append(data[dc]['data'])
    pagecount = pagecount + 1
    for x in xrange(dc+1, len(data)):
      loc = data[x]['data']['location']
      for k in fdata:
	l = k.split(',')
        #lo is longitude for that reading, la is latitude for that reading (both in decimal)
	lo = Decimal(l[0])
	la = Decimal(l[1])
        #if lo and la are within 0.01 of previous entry, then combine with it. else make a new one
        if 'ndt' in data[x]['data'] and 'bw' in data[x]['data']['ndt'] and 'avgrtt' in data[x]['data']['ndt']: 
          #if (math.fabs((Decimal(round(loc['longitude'], 2)) - float(lo)) < 0.1) and (math.fabs(Decimal(round(loc['latitude'], 2)) - float(la)) < 0.1)):
          if (math.fabs(round(loc['longitude'],2) - float(lo)) < 0.01 and math.fabs(round(loc['latitude'],2) - float(la)) < 0.01):  
            fdata[k].append(data[x]['data'])
	  else:
	    new_key = str(round(loc['longitude'],2)) + "," + str(round(loc['latitude'],2))
	    fdata[new_key] = []
	    fdata[new_key].append(data[x]['data']) 
            #fdata[new_key] = [data[x]['data']] 
  #d now gets updated to last serial number of previous page to get the next data page (next data array)
    if(len(data) != 0):
      d1 =  data[len(data)-1]
      d = d1['serial']
# I now have dictionary where keys are long, lat strings and values for each are array of dictionaries (only the data part) for
# all entries that fit in the same location area. Now I must, for each key (location), average the necessary
# values from all dictionaries listed in that location and then create a final dictionary where keys are again 
# the locations, and the values are now the final dictionary of the averaged relevant values (key is value description and value is avg (eg. latency: 5))

senddata = {}
for lkey in fdata:
  #count = 0
  bwtotal = 0.0
  rtttotal = 0.0
  #fdata is dictionary where locations are keys and values are arrays of dictionaries of data for that location
  for inkey in xrange(0, len(fdata[lkey])): 
    #print float(fdata[lkey][inkey]['ndt']['bw'])
    bwtotal = bwtotal + float(fdata[lkey][inkey]['ndt']['bw'])
    rtttotal = rtttotal + float(fdata[lkey][inkey]['ndt']['avgrtt'])
    #CAN DO THIS FOR ANY METRIC (which is key of data)
    #count = count + 1  
  totdat = {}
  totdat['bw'] = bwtotal/len(fdata[lkey])
  totdat['rtt'] = rtttotal/len(fdata[lkey])
  senddata[lkey] = {}
  senddata[lkey] = totdat
jsenddata = json.dumps(senddata)
with open("onmapdata.json", "w") as f:
    f.write(jsenddata)
#senddata is the final dictionary with keys as long,lat and values as dictionaries (one per location) with keys as latency, rtt, etc. and values as the final values.
