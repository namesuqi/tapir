# coding=utf-8
# author: zengyuetian

import json
import requests


def http_request(method, address, port, url, headers=None, data=None, json_data=True, timeout=None):
    try:
        # remove / from url string
        if url[0] == "/":
            url = url[1:]
        # full url
        url = "http://{0}:{1}/{2}".format(address, port, url)

        # format data
        if json_data:
            data = json.dumps(data)

        # send request and get resp
        response = requests.request(method=method, url=url, headers=headers, data=data, timeout=timeout)
        return response
    except Exception as err:
        raise AssertionError('Connection error: %s\n%s' % (err, url))


def send_http_request(req_from, req_method, api_host, api_port, req_url, req_headers, req_cookies, req_data, timeout=None):
    try:
        url = "http://" + str(api_host) + ":" + str(api_port) + str(req_url)
        req_data = json.dumps(req_data)
        print '-------------------------%sRequest---------------------------' % req_from
        print "url: " + url
        print "method: " + str(req_method)
        print "headers: " + str(req_headers)
        print "data: " + str(req_data)
        print '------------------------------------------------------------------------'
        response = None
        if req_method == "GET":
            # if req_cookies == None:
            if req_cookies is None:
                response = requests.get(url, headers=req_headers, timeout=timeout)
            else:
                response = requests.get(
                    url, headers=req_headers, cookies=req_cookies, timeout=timeout)
        if req_method == "POST":
            # if req_data != None:
            if req_data is not None:
                response = requests.post(url, headers=req_headers,
                                         cookies=req_cookies, data=req_data, timeout=timeout)
            else:
                response = requests.post(
                    url, headers=req_headers, cookies=req_cookies, timeout=timeout)
        if req_method == "PUT":
            # if req_data != None:
            if req_data is not None:
                response = requests.put(url, headers=req_headers,
                                        cookies=req_cookies, data=req_data, timeout=timeout)
            else:
                response = requests.put(
                    url, headers=req_headers, cookies=req_cookies, timeout=timeout)
        if req_method == "DELETE":
            # if req_data != None:
            if req_data is not None:
                response = requests.delete(url, headers=req_headers,
                                           cookies=req_cookies, data=req_data, timeout=timeout)
            else:
                response = requests.delete(
                    url, headers=req_headers, cookies=req_cookies, timeout=timeout)
        print '+++++++++++++++++++++++++++%sResponse++++++++++++++++++++++++++' % req_from
        print response.status_code
        if (not (response.headers.get("Content-length") is None)) and (int(response.headers.get("Content-length")) < 868) or response.headers.get("Content-length") is None:   # donot print piece info of files
            print response.content

        # print response.headers.get("Content-length")
        print response.headers.get("set-cookie")
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        return response
    except Exception as err:
        raise AssertionError('Connection error: %s\n%s' % (err, url))


def send_http_request_without_json(req_from, req_method, api_host, api_port, req_url, req_headers, req_cookies, req_data):
    try:
        url = "http://" + str(api_host) + ":" + str(api_port) + str(req_url)

        print '-------------------------%sRequest---------------------------' % req_from
        print "url: " + url
        print "method: " + str(req_method)
        print "headers: " + str(req_headers)
        print "data: " + str(req_data)
        print '------------------------------------------------------------------------'
        response = None
        if req_method == "GET":
            # if req_cookies == None:
            if req_cookies is None:
                response = requests.get(url, headers=req_headers)
            else:
                response = requests.get(
                    url, headers=req_headers, cookies=req_cookies)
        if req_method == "POST":
            # if req_data != None:
            if req_data is not None:
                response = requests.post(url, headers=req_headers,
                                         cookies=req_cookies, data=req_data)
            else:
                response = requests.post(
                    url, headers=req_headers, cookies=req_cookies)
        if req_method == "PUT":
            # if req_data != None:
            if req_data is not None:
                response = requests.put(url, headers=req_headers,
                                        cookies=req_cookies, data=req_data)
            else:
                response = requests.put(
                    url, headers=req_headers, cookies=req_cookies)
        if req_method == "DELETE":
            # if req_data != None:
            if req_data is not None:
                response = requests.delete(url, headers=req_headers,
                                           cookies=req_cookies, data=req_data)
            else:
                response = requests.delete(
                    url, headers=req_headers, cookies=req_cookies)
        print '+++++++++++++++++++++++++++%sResponse++++++++++++++++++++++++++' % req_from
        print response.status_code
        print response.content
        print response.headers.get("set-cookie")
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        return response
    except Exception as err:
        raise AssertionError('Connection error: %s\n%s' % (err, url))


def send_https_request(req_from, req_method, api_host, api_port, req_url, req_headers, req_cookies, req_data, timeout=None):
    try:
        url = "https://" + str(api_host) + ":" + str(443) + str(req_url)
        req_data = json.dumps(req_data)
        print '-------------------------%sRequest---------------------------' % req_from
        print "url: " + url
        print "method: " + str(req_method)
        print "headers: " + str(req_headers)
        print "data: " + str(req_data)
        print '------------------------------------------------------------------------'
        response = None
        if req_method == "GET":
            # if req_cookies == None:
            if req_cookies is None:
                response = requests.get(url, verify=False, headers=req_headers, timeout=timeout)
            else:
                response = requests.get(
                    url, verify=False, headers=req_headers, cookies=req_cookies, timeout=timeout)
        if req_method == "POST":
            # if req_data != None:
            if req_data is not None:
                response = requests.post(url, verify=False, headers=req_headers,
                                         cookies=req_cookies, data=req_data, timeout=timeout)
            else:
                response = requests.post(
                    url, verify=False, headers=req_headers, cookies=req_cookies, timeout=timeout)
        if req_method == "PUT":
            # if req_data != None:
            if req_data is not None:
                response = requests.put(url, verify=False, headers=req_headers,
                                        cookies=req_cookies, data=req_data, timeout=timeout)
            else:
                response = requests.put(
                    url, verify=False, headers=req_headers, cookies=req_cookies, timeout=timeout)
        if req_method == "DELETE":
            # if req_data != None:
            if req_data is not None:
                response = requests.delete(url, verify=False, headers=req_headers,
                                           cookies=req_cookies, data=req_data, timeout=timeout)
            else:
                response = requests.delete(
                    url, verify=False, headers=req_headers, cookies=req_cookies, timeout=timeout)
        print '+++++++++++++++++++++++++++%sResponse++++++++++++++++++++++++++' % req_from
        print response.status_code
        print response.content
        print response.headers.get("set-cookie")
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        return response
    except Exception as err:
        raise AssertionError('Connection error: %s\n%s' % (err, url))


def send_https_request_without_json(req_from, req_method, api_host, api_port, req_url, req_headers, req_cookies,
                                    req_data):
    try:
        url = "https://" + str(api_host) + ":" + str(443) + str(req_url)
        req_data = json.dumps(req_data)
        print '-------------------------%sRequest---------------------------' % req_from
        print "url: " + url
        print "method: " + str(req_method)
        print "headers: " + str(req_headers)
        print "data: " + str(req_data)
        print '------------------------------------------------------------------------'
        response = None
        if req_method == "GET":
            # if req_cookies == None:
            if req_cookies is None:
                response = requests.get(url, verify=False, headers=req_headers)
            else:
                response = requests.get(
                    url, verify=False, headers=req_headers, cookies=req_cookies)
        if req_method == "POST":
            # if req_data != None:
            if req_data is not None:
                response = requests.post(url, verify=False, headers=req_headers,
                                         cookies=req_cookies, data=req_data)
            else:
                response = requests.post(
                    url, verify=False, headers=req_headers, cookies=req_cookies)
        if req_method == "PUT":
            # if req_data != None:
            if req_data is not None:
                response = requests.put(url, verify=False, headers=req_headers,
                                        cookies=req_cookies, data=req_data)
            else:
                response = requests.put(
                    url, verify=False, headers=req_headers, cookies=req_cookies)
        if req_method == "DELETE":
            # if req_data != None:
            if req_data is not None:
                response = requests.delete(url, verify=False, headers=req_headers,
                                           cookies=req_cookies, data=req_data)
            else:
                response = requests.delete(
                    url, verify=False, headers=req_headers, cookies=req_cookies)
        print '+++++++++++++++++++++++++++%sResponse++++++++++++++++++++++++++' % req_from
        print response.status_code
        print response.content
        print response.headers.get("set-cookie")
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        return response
    except Exception as err:
        raise AssertionError('Connection error: %s\n%s' % (err, url))


def send_request(req_from, protocol, req_method, api_host, api_port, req_url, req_headers=None, req_cookies=None,
                 req_data=None, timeout=None):
    if str(protocol) == 'HTTPS':
        return send_https_request(req_from, req_method, api_host, api_port, req_url, req_headers, req_cookies, req_data, timeout)
    return send_http_request(req_from, req_method, api_host, api_port, req_url, req_headers, req_cookies, req_data, timeout)


def send_request_without_json(req_from, protocol, req_method, api_host, api_port, req_url, req_headers=None, req_cookies=None, req_data=None):
    if str(protocol) == 'HTTPS':
        return send_https_request_without_json(req_from, req_method, api_host, api_port, req_url, req_headers,
                                               req_cookies, req_data)
    return send_http_request_without_json(req_from, req_method, api_host, api_port, req_url, req_headers, req_cookies,
                                          req_data)


if __name__ == "__main__":
    resp = http_request('GET', "www.baidu.com", 80, "/")
    print resp.status_code
    print resp.content

    pass
