from django import template

register = template.Library()

@register.simple_tag
def customURL(fieldName, value, urlencode=None):
    urlQuery = '?{}={}'.format(fieldName, value)

    if urlencode:
        queryString = urlencode.split('&')
        filteredQueryString = filter(lambda parameter : parameter.split('=')[0]!=fieldName, queryString)
        encodedQueryString = '&'.join(filteredQueryString)
        urlQuery = '{}&{}'.format(urlQuery, encodedQueryString)

    return urlQuery