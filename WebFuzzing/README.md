apt --purge remove python3-pycurl
apt install libcurl4-openssl-dev libssl-dev
pip3 install pycurl wfuzz

1st step we choose the URL
2nd step we choose the dictionary Attention we must put the full path ex /home/user/document/common.txt

Fuzzing a URL
Fuzzing a URL with wfuzz library is very simple. Firstly, import the wfuzz module:

Now, let’s try to fuzz a web page to look for hidden content, such as directories. For this example, let’s use Acunetix’s testphp (http://testphp.vulnweb.com/):

>>> import wfuzz
>>> for r in wfuzz.fuzz(url="http://testphp.vulnweb.com/FUZZ", hc=[404], payloads=[("file",dict(fn="wordlist/general/common.txt"))]):
...     print r
...
00060:  C=301      7 L        12 W          184 Ch        "admin"
00183:  C=403     10 L        29 W          263 Ch        "cgi-bin"
00429:  C=301      7 L        12 W          184 Ch        "images"
...
Now, we have a FuzzResult object called r. We can get all the information we need from this object.

FuzzSession object
A FuzzSession object has all the methods of the main wfuzz API.

The FuzzSession object allows you to persist certain parameters across fuzzing sessions:

>>> import wfuzz
>>> s = wfuzz.FuzzSession(url="http://testphp.vulnweb.com/FUZZ")
>>> for r in s.fuzz(hc=[404], payloads=[("file",dict(fn="wordlist/general/common.txt"))]):
...     print r
...
00060:  C=301      7 L        12 W          184 Ch        "admin"
00183:  C=403     10 L        29 W          263 Ch        "cgi-bin"
...
FuzzSession can also be used as context manager:

>>> with wfuzz.FuzzSession(url="http://testphp.vulnweb.com/FUZZ", hc=[404], payloads=[("file",dict(fn="wordlist/general/common.txt"))]) as s:
...     for r in s.fuzz():
...             print r
...
00295:  C=301      7 L        12 W          184 Ch        "admin"
00418:  C=403     10 L        29 W          263 Ch        "cgi-bin"
Get payload
The get_payload function generates a Wfuzz payload from a Python iterable. It is a quick and flexible way of getting a payload programmatically without using Wfuzz payloads plugins.

Generating a new payload and start fuzzing is really simple:

>>> import wfuzz
>>> s = wfuzz.get_payload(range(5))
>>> for r in s.fuzz(url="http://testphp.vulnweb.com/FUZZ"):
...     print r
...
00012:  C=404      7 L        12 W          168 Ch        "0"
00013:  C=404      7 L        12 W          168 Ch        "1"
00014:  C=404      7 L        12 W          168 Ch        "2"
00015:  C=404      7 L        12 W          168 Ch        "3"
00016:  C=404      7 L        12 W          168 Ch        "4"
The get_payloads method can be used when various payloads are needed:

>>> import wfuzz
>>> s = wfuzz.get_payloads([range(5), ["a","b"]])
>>> for r in s.fuzz(url="http://testphp.vulnweb.com/FUZZ/FUZ2Z"):
...     print r
...
00028:  C=404      7 L        12 W          168 Ch        "4 - b"
00027:  C=404      7 L        12 W          168 Ch        "4 - a"
00024:  C=404      7 L        12 W          168 Ch        "2 - b"
00026:  C=404      7 L        12 W          168 Ch        "3 - b"
00025:  C=404      7 L        12 W          168 Ch        "3 - a"
00022:  C=404      7 L        12 W          168 Ch        "1 - b"
00021:  C=404      7 L        12 W          168 Ch        "1 - a"
00020:  C=404      7 L        12 W          168 Ch        "0 - b"
00023:  C=404      7 L        12 W          168 Ch        "2 - a"
00019:  C=404      7 L        12 W          168 Ch        "0 - a"
Get session
The get_session function generates a Wfuzz session object from the specified command line. It is a quick way of getting a payload programmatically from a string representing CLI options:

$ python
>>> import wfuzz
>>> s = wfuzz.get_session("-z range,0-10 http://testphp.vulnweb.com/FUZZ")
>>> for r in s.fuzz():
...     print r
...
00002:  C=404      7 L        12 W          168 Ch        "1"
00011:  C=404      7 L        12 W          168 Ch        "10"
00008:  C=404      7 L        12 W          168 Ch        "7"
00001:  C=404      7 L        12 W          168 Ch        "0"
00003:  C=404      7 L        12 W          168 Ch        "2"
00004:  C=404      7 L        12 W          168 Ch        "3"
00005:  C=404      7 L        12 W          168 Ch        "4"
00006:  C=404      7 L        12 W          168 Ch        "5"
00007:  C=404      7 L        12 W          168 Ch        "6"
00009:  C=404      7 L        12 W          168 Ch        "8"
00010:  C=404      7 L        12 W          168 Ch        "9"
Interacting with the results
Once a Wfuzz result is available the grammar defined in the filter language can be used to work with the results’ values. For example:

