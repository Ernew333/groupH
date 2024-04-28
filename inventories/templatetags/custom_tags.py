from django import template

register = template.Library()

@register.simple_tag
def tag(value, fieldName, urlencode=None):
    url = '?{}={}'.format(fieldName, value)

    if urlencode:
        querystring = urlencode.split('&')
        filteredQueryString = filter(lambda parameter : parameter.split('=')[0]!=fieldName, querystring)
        encodedQueryString = '&'.join(filteredQueryString)
        url = '{}&{}'.format(url, encodedQueryString)

    return url