from BeautifulSoup import BeautifulSoup

correct_mime = ['text/html', 'text/plain']


def is_mime_correct(content_type):
    if content_type.split(';')[0] in correct_mime:
        return True
    return False


def is_onion_domain(url):
    if url[:4] != 'http':
        return False
    if url.split('/')[2][-6:] != '.onion':
        return False
    return True


def get_urls(content):
    try:
        soup = BeautifulSoup(content)
    except UnicodeEncodeError:
        print 'Invalid HTML/TEXT file'
        return None
    return soup.findAll('a', href=True)
