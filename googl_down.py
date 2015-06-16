from os import sys
import time
import numpy as np
import urllib2
import simplejson
import cv2

# open an image from a given valid url
def url_to_image(url):
  # download the image, convert it to a NumPy array, and then read
  # it into OpenCV format
  resp = urllib2.urlopen(url)
  arr = np.asarray(bytearray(resp.read()), dtype="uint8")
  img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
 
  # return the image
  return img

# search images in Google Images given a set of words
# searchTerm The set of words to search
# nSearches The number of images, must be multiple of 4
def search(searchTerm, nSearches=8):

  # parse as 'string1+string2+..+stringN'
  if ' ' in searchTerm:
    searchTerm = searchTerm.replace(' ', '+')

  hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

  # construct the query url
  url_query = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=' + searchTerm + '&start=0&as_filetype=jpg'
  print url_query

  # generate the request to ggl
  request = urllib2.Request(url_query, headers=hdr)

  # the the request response from ggl
  response = urllib2.urlopen(request)

  # process the JSON string
  results = simplejson.load(response)

  # read the results
  for image_info in results['responseData']['results']:
    
    # wrap image url
    url = image_info['unescapedUrl']
    print url

    # parse the url and construct an opencv Mat
    img = url_to_image(url)

    try:
      # show the image
      cv2.namedWindow('vis', 0)
      cv2.imshow('vis', img)
      cv2.waitKey(1000)
      cv2.destroyAllWindows()
    except cv2.error as e:
      # Throw away some gifs...blegh.
      print 'ERROR: %s with url: %s ' % (e, url)
      continue

# Example
if __name__ == "__main__":

  if len(sys.argv) < 2:
    print '[ERROR] Need at least one argument'
    sys.exit()

  # parse the list input as string
  searchTerm = ' '.join(sys.argv[1:])

  # run the searching algorithm
  search( searchTerm )