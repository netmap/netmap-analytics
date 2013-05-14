#!/usr/bin/env ruby

# Computes map plots out of the raw data.

require 'json'

Dir.mkdir('source/json') unless File.exist?('source/json')

grid = {}
File.open 'raw/readings.jsonn', 'rb' do |f|
  f.each_line do |line|
    reading = JSON.parse(line)['data']

    location = reading['location']
    ndt = reading['ndt']
    next unless location && ndt && ndt['avgrtt'] && ndt['bw']

    lat = location['latitude']
    long = location['longitude']
    key = [lat.round(3), long.round(3)]
    grid[key] ||= []
    grid[key] << reading
  end
end

class Array
  def avg
    sum.to_f / length
  end
  def sum
    s = 0
    0.upto(length - 1) { |i| s += self[i] }
    s
  end
end

summary = grid.map do |key, readings|
  avg_rtt = readings.map { |r| r['ndt']['avgrtt'].to_f }.avg
  avg_bw = readings.map { |r| r['ndt']['bw'].to_f }.avg
  {
    pos: { lat: key[0], long: key[1] },
    rtt: avg_rtt, bw: avg_bw, count: readings.length
  }
end

File.open 'json/netmap.jsonp', 'wb' do |f|
  f.write "onMapData(#{JSON.dump(summary)});\n"
end
