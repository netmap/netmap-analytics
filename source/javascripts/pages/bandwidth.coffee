window.onMapData = (data) ->
  points = for item in data
    if item.bw < 1
      hue = 0
      light = Math.round(item.bw * 50) + 50
    else if item.bw < 5
      hue = 60
      light = Math.round(item.bw * 10) + 50
    else
      hue = 120
      light = Math.round(item.bw * 5)

    {
      lat: item.pos.lat, long: item.pos.long,
      color: "hsl(#{hue}, 100%, #{light}%)"
    }

  $ ->
    mapView.renderData points
