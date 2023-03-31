import serial
import glob

def list_serial_devices():
  ports = glob.glob('/dev/ttyACM[0-9]*')
  res = []
  for port in ports:
    try:
      s = serial.Serial(port)
      s.close()
      res.append(port)
    except:
      pass
  return res
