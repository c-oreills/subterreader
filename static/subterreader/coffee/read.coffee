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
                linked_html = add_link_onclicks(clean_html)
                container.html(linked_html)
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

add_link_onclicks = (html) ->
    $(html).find('a').click(() ->
        click_link($(this))
        return false
    )
    return html

add_to_cookie_if_not_present = (cookie_name, value) ->
    cookie_list = $.cookie(cookie_name)?.split(',')
    cookie_list ?= []
    value = value.toString()
    if value not in cookie_list
        cookie_list.push(value)
    $.cookie(cookie_name, cookie_list.join(','), {path: '/', expires:1000})

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
    add_to_cookie_if_not_present('read_webpages', webpage_id)

window.click_link = (link) ->
    url = link.attr('href')
    link_add_div = $('#link-add-outer')
    link_add_div.css('width', $(window).width())
    link_add_div.slideDown()
    link_add_div.data('url', url)

window.add_url_to_list = (url) ->
    add_url_to_list_cookie(url)
    $.post('.')
    # TODO: Load content in dynamically and add to end of onscreen list
    return false

add_url_to_list_cookie = (url) ->
    add_to_cookie_if_not_present('add_urls', url)

window.goto_url = (url) ->
    window.location = url
