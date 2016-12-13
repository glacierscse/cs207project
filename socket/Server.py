import socket
from concurrent.futures import ThreadPoolExecutor 
import threading
from tsdb_op import *
from serialization import *
from error import *
import json
import socketserver
import sys
sys.path.append('../')
from p7_simsearch.search_engine import searchEngine
from timeseries.FileStorageManager import FileStorageManager


LENGTH_FIELD_LENGTH = 4

class TSDB_Server(socketserver.BaseServer):

	def __init__(self, database1,database2, port = ("localhost", 12341)):
		self.rbdb = database1
		self.smdb = database2
		self.addr = port
		self.deserializer = Deserializer()


	def run(self):
		pool = ThreadPoolExecutor(12)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.bind(self.addr)
		sock.listen(5)
		while True:
			print("Connecting...")
			client_sock, client_addr = sock.accept()
			pool.submit(self.echo_client, client_sock, client_addr)


	def echo_client(self, socket, client_addr):
		print('Got connection from', client_addr) 
		while True:
			msg = socket.recv(1024)
			if not msg:
				break
			socket.sendall(msg)
			print("Client closed connection")
			socket.close()

# get it on the socket, then (perhaps in a thread)
	def data_received(self, data):
		self.server.deserializer.append(data)
		if self.server.deserializer.ready():
			msg = self.server.deserializer.deserialize()
			status = TSDBStatus.OK  # until proven otherwise.
			response = TSDBOp_Return(status, None)  # until proven otherwise.
			try:
				op = TSDBOp.from_json(msg)
			except TypeError as e:
				status = TSDBStatus.INVALID_OPERATION
				response = TSDBOp_Return(status, None)

			if status is TSDBStatus.OK:
				if isinstance(op, TSDBOp_Simquery_WithTS):
					response = self._simquery_with_ts(op)
				elif isinstance(op, TSDBOp_Simquery_WithID):
					response = self._simquery_with_id(op)
				elif isinstance(op, TSDBOp_GetTS_WithID):
					response = self._getts_with_id(op)
				else:
					response = TSDBOp_Return(TSDBStatus.UNKNOWN_ERROR, op['op'])

			self.request.send(serialize(response.to_json()))
			# send it out


##### Myra need to revise
	def _simquery_with_ts(self, op):
		id_list = self.rbdb.search_by_ts(op['ts'], op['n'])

		result = TSDBOp_Simquery_WithTS('simquery_ts')
		result['id'] = id_list
		return result

	def _simquery_with_id(self, op):
		id_list = self.rbdb.search_by_id(op['id'], op['n'],self.smdb)
		result = TSDBOp_Simquery_WithID('simquery_id')
		result['id'] = id_list
		return result

##### Myra need to revise
	def _getts_with_id(self, op):
		ts = self.rbdb.getts_with_id(op['id'],self.smdb)
		ts_list = [list(ts.times()), list(ts.values())]
		result = TSDBOp_GetTS_WithID('get_id')  ##just changed this
		result['ts'] = ts_list
		return result

if __name__ == '__main__':
	s = searchEngine()
	f = FileStorageManager("../timeseries/timeseriesDB")
	tsdb = TSDB_Server(s,f)
	tsdb.run()

