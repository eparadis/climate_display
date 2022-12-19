from lcd import initialize, puts, clear, set_pos

initialize()
puts('Ready...')

def get_climate_json():
    import socket
    url = 'http://192.168.0.111/data.json'
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    # trash the first three lines, which is our very minimal header response
    s.readline()
    s.readline()
    s.readline()
    from json import loads
    j = loads(s.readline())
    s.close()
    return j

def update():
  data = get_climate_json()
  # get everything to a useful precision
  temp = str(round(data['temp'], 1))
  RH  = str(round(data['RH'], 1))
  light = str(round(data['light'], 1))
  vpd_prec = 2 if data['vpd'] < 1 else 1
  vpd = str(round(data['vpd'], vpd_prec))
  # assemble strings
  top = temp + "degF " + RH + "%RH"
  bot = light + "LT " + vpd + "kPa"
  set_pos(0,0)
  puts(top)
  set_pos(0,1)
  puts(bot)

