import os
import logging
import telnetlib
from bottle import route, get, request, run, template, response, static_file

HOST = "192.168.100.250"
USER = "leitch"
PASS = "leitchadmin"

@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='/home/leo/dev/mtx-controller')

@get('/mtxController')
def message():
  src = bytes(request.query.source, encoding='ascii')
  dst = bytes(request.query.destination, encoding='ascii')
  #src = str(request.query.source)
  #dst = str(request.query.destination)
  logging.info("Destination %s, Source %s" % (dst, src))
  tn = telnetlib.Telnet(HOST)
  #tn.set_debuglevel("1")
  tn.read_until(b"login: ")
  tn.write(USER.encode("ascii") + b"\r\n")
  tn.read_until(b"password: ")
  tn.write(PASS.encode("ascii") + b"\r\n")
  tn.write(b"@ X:0/" + bytes(dst) + b"," + bytes(src) + b"\r\n")
  tn.read_until(b">")
  #tn_read = tn.read_until(b"t*H,0")
  tn.close()

  response.content_type = 'application/json'
  resp = {"Message":"Routed","Destination":dst,"Source":src}
  return resp

@get('/mtxStatus')
def message():
  tn = telnetlib.Telnet(HOST)
  tn.read_until(b"login: ")
  tn.write(USER.encode("ascii") + b"\r\n")
  tn.read_until(b"password: ")
  tn.write(PASS.encode("ascii") + b"\r\n")
  tn.read_until(b">")
  tn.write(b"@ S?0\r\n")
  tn_read = tn.read_until(b"t*H,0")
  #tn.read_until(b">")
  #tn.write(b"EXIT\r\n")
  tn.close()
  tn_read_b = tn_read.decode("utf-8")
  return template('{{read}}', read=tn_read)



run(host='0.0.0.0', port=8080, reloader=True)
