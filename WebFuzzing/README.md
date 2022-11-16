# Prerequisites

apt --purge remove python3-pycurl
apt install libcurl4-openssl-dev libssl-dev
pip3 install pycurl wfuzz

## select parameters

1st step we choose the URL 

2nd step we choose the dictionary Attention we must put the full path ex /home/user/document/common.txt
![image](https://user-images.githubusercontent.com/118366867/202224052-6d312d61-25f2-4b2c-ab2a-9710da1dea54.png)


## Fuzzing a URL


Now, let’s try to fuzz a web page to look for hidden content, such as directories. For this example, let’s use Acunetix’s testphp (http://testphp.vulnweb.com/):
![fuzzing url](https://user-images.githubusercontent.com/118366867/202223778-45a0b57a-2b4d-4475-be68-c4497f3992e3.png)

## Get payload

The get_payload function generates a Wfuzz payload from a Python iterable. It is a quick and flexible way of getting a payload programmatically without using Wfuzz payloads plugins.

Generating a new payload and start fuzzing is really simple:
![get](https://user-images.githubusercontent.com/118366867/202224094-20457027-c38b-4000-a052-dd2ad4a95952.png)


## Get session

The get_session function generates a Wfuzz session object from the specified command line. It is a quick way of getting a payload programmatically from a string representing CLI options:
![payload](https://user-images.githubusercontent.com/118366867/202224162-2898d51a-da39-45bd-8508-4e074d0f11ad.png)

## Interacting with the results

It allows you to retrieve user cookie data...
![resulta](https://user-images.githubusercontent.com/118366867/202224401-dd199799-0870-4e11-ac83-3c3a82cf8bef.png)

