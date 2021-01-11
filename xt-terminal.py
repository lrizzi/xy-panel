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
  src = request.query.source
  dst = request.query.destination
  logging.info("Destination %s, Source %s" % (dst, src))
  tn = telnetlib.Telnet(HOST)
  tn.read_until(b"login: ")
  tn.write(USER.encode("ascii") + b"\r\n")
  tn.read_until(b"password: ")
  tn.write(PASS.encode("ascii") + b"\r\n")
  tn.read_until(b">")
  tn.write(b"SOURCE " + src.encode("ascii") + b"\r\n")
  tn.read_until(b">")
  tn.write(b"DESTINATION" + dst.encode("ascii") + b"\r\n")
  tn.read_until(b">")
  tn.write(b"EXIT\r\n")

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
  tn.write(b"READ\r\n")
  tn_read = tn.read_until(b">")
  #tn.read_until(b">")
  tn.write(b"EXIT\r\n")
  tn_read_b = tn_read.decode("utf-8")
  tn_read_c1 = tn_read_b.replace("Level 00:","")
  tn_read_c2 = tn_read_c1.replace(">","")
  tn_read_c3 = tn_read_c2.replace(",","<--")
  tn_read_parsed = tn_read_c3
  return template('{{read}}', read=tn_read_parsed)


run(host='0.0.0.0', port=8080, reloader=True)
