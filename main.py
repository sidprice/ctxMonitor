import gdb_remote_serial_protocol as gdb_rsp

gdb_rsp = sr.probe()
gdb_rsp.open('COM8')
