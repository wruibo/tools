'''
    http request header for represent different browser vendors
'''


class chrome:
    '''
        chrome request headers
    '''
    default = [
        ("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"),
        ("Accept", "text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8"),
        ("Accept-Encoding", "gzip, deflate")
    ]

    mobile = [
        ("User-Agent","Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"),
        ("Accept", "text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8"),
        ("Accept-Encoding", "gzip, deflate")
    ]
