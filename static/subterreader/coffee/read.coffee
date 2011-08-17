
window.load_url_to_container = (url, container) ->
    # Use YQL as advised in http://www.wait-till-i.com/2010/01/10/loading-external-content-with-ajax-using-jquery-and-yql/
    yql_url = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22' + encodeURIComponent(url) + '%22&format=xml&callback=?'
    $.getJSON(yql_url,
        (data) ->
            ext_html = $(data.results[0])
            clean_html = sanitize(ext_html)
            container.html(clean_html)
    )

sanitize = (ext_html) ->
    ext_html.find('script').remove()
    ext_html.find('noscript').remove()
    return ext_html
