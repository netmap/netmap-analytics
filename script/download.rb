#!/usr/bin/env ruby

# Downloads the readings from the NetMap server into raw/readings.jsonn"

require 'json'
require 'open-uri'

Dir.mkdir('raw') unless File.exist?('raw')

File.open 'raw/readings.jsonn', 'wb' do |f|
  last_serial = 0
  loop do
    uri = "http://netmap-data.pwnb.us/readings/above/#{last_serial}"
    readings = open(uri) { |u| JSON.parse u.read }
    break if readings.empty?
    readings.each do |reading|
      last_serial = reading['serial']
      f.puts JSON.dump(reading)
    end
  end
end
