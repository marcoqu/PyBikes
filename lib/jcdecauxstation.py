# -*- coding: utf-8 -*-

from station import Station
from BeautifulSoup import BeautifulStoneSoup
import urllib,urllib2
from datetime import datetime

LIST_URL = '/service/carto'
STATION_URL = '/service/stationdetails/%s/'

class JCDecauxStation(Station):
  
  prefix = ""
  main_url = ""
  station_url = ""
    
  def update(self, prefix = ""):
      #print "Updating "+str(self.number)
      if self.station_url == "":
	self.station_url = STATION_URL % self.city
      usock = urllib.urlopen(prefix+self.main_url + self.station_url + str(self.number))
      xml_data = usock.read()
      usock.close()
      soup = BeautifulStoneSoup(xml_data)
      self.bikes = int(soup.find('available').contents[0])
      self.free = int(soup.find('free').contents[0])
      self.timestamp = datetime.now()     
      return self
    
  def from_xml(self, xml_data):
    
    # xml marker object as in
    # <marker name="20011 - PYRÉNÉES-DAGORNO" number="20011" address="103 RUE DES PYRENNEES -" 
    # fullAddress="103 RUE DES PYRENNEES - 75020 PARIS" 
    # lat="48.8556029461854" lng="2.405108726356833" 
    # open="1" bonus="0"/>

    soup = BeautifulStoneSoup(xml_data)
    self.number = int(soup.contents[0].get("number"))
    self.name = unicode(BeautifulStoneSoup(soup.contents[0].get("name"),convertEntities=BeautifulStoneSoup.HTML_ENTITIES )).replace('\n','')
    if (self.name == ""):
      self.name = unicode(BeautifulStoneSoup(soup.contents[0].get("address"),convertEntities=BeautifulStoneSoup.HTML_ENTITIES )).replace('\n','')
    if (self.name == ""):
      self.name = "??"
    self.lat = int(float(soup.contents[0].get("lat"))*1E6)
    self.lng = int(float(soup.contents[0].get("lng"))*1E6)
    

def get_all(spec, prefix = ""):
  usock = urllib2.urlopen(prefix+spec.main_url+LIST_URL)
  xml_data = usock.read()
  usock.close()
  soup = BeautifulStoneSoup(xml_data)
  markers = soup.findAll('marker')
  stations = []
  for index, marker in enumerate(markers):
    station = spec(index)
    station.from_xml(marker.prettify())
    stations.append(station)
  return stations
    
