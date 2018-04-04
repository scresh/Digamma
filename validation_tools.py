from BeautifulSoup import BeautifulSoup

html_mime = 'text/html'
plain_mime = 'text/plain'

correct_mime = [html_mime, plain_mime]
correct_extensions = ['html', 'html', 'txt']


def has_correct_extension(url):
    supposed_extension = url.split('.')[-1]
    if len(supposed_extension) > 4:
        return True
    if supposed_extension in correct_extensions:
        return True
    return False


def is_onion_domain(url):
    try:
        if url.split('/')[2][-6:] != '.onion':
            return False
        return True
    except IndexError:
        return False


def get_urls(content, content_type):
    # Previously is_mime_correct() did it
    mime_type = content_type.split(';')[0]
    if not (mime_type in correct_mime):
        return None

    # Different processing for different MIME types
    urls = []
    if mime_type == html_mime:
        try:
            soup = BeautifulSoup(content)
            for a_href in soup.findAll('a', href=True):
                urls.append(a_href['href'])
        except UnicodeEncodeError:
            print 'Invalid HTML/TEXT file'
    else:
        words = content.replace('\n', ' ').split(' ')
        for word in words:
            if word[:4] == 'http':
                urls.append(word)

    # Final validation
    results = []
    for url in urls:
        if is_onion_domain(url) and has_correct_extension(url):
            results.append(url)
    return results

