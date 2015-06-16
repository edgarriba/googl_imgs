from os import sys
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

  # if its a list, parse as 'string1+string2+..+stringN'
  # Example: ['hello','world'] --> hello+world
  searchTerm = '+'.join(searchTerm)

  for i in range(0, nSearches/4):

    # construct the query url
    url_query = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=' + searchTerm + '&start='+str(i*4)+ '&as_filetype=jpg'
    
    #request = urllib2.Request(url, None, {'Referer': /* Enter the URL of your site here */})
    request = urllib2.Request(url_query, None)
    response = urllib2.urlopen(request)

    # Process the JSON string.
    results = simplejson.load(response)

    # read the results
    for image_info in results['responseData']['results']:
      
      # wrap image url
      url = image_info['unescapedUrl']

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

  # run the searching algorithm
  search( sys.argv[1:] )