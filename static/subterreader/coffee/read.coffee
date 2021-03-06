DEBUG = window.DEBUG
HOLD = window.HOLD

if DEBUG
    window.debug = {}

window.load_url_to_container = (url, container) ->
    # Use YQL as advised in http://www.wait-till-i.com/2010/01/10/loading-external-content-with-ajax-using-jquery-and-yql/
    yql_url = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22' + encodeURIComponent(url) + '%22&format=xml&callback=?'
    $.getJSON(yql_url,
        (data) ->
            if not HOLD
                ext_html = $(data.results[0])
                clean_html = sanitize(ext_html)
                container.html(clean_html)
    )

sanitize = (ext_html) ->
    if DEBUG
        orig_ext_html = ext_html
    ext_html.find('script').remove()
    ext_html.find('noscript').remove()
    clean_html = (node for node in ext_html when node.constructor isnt HTMLScriptElement)
    if DEBUG
        window.debug.sanitize ?= []
        window.debug.sanitize.push([orig_ext_html, clean_html])
    return clean_html

window.mark_as_read = (webpage_id) ->
    # TODO: slide the article and controls closed (keep page position intact)
    ###
    Set cookie and then send an async poll to server.
    If server is reachable, the webpage will be marked as read
    and the cookie deleted by Django.
    If not, then the cookie will remain intact for subsequent requests.
    ###
    mark_as_read_cookie(webpage_id)
    $.post('.')
    return false

mark_as_read_cookie = (webpage_id) ->
    read_list = $.cookie('read_webpages')?.split(',')
    read_list ?= []
    webpage_id = webpage_id.toString()
    if webpage_id not in read_list
        read_list.push(webpage_id)
    $.cookie('read_webpages', read_list.join(','), {path: '/', expires:1000})
