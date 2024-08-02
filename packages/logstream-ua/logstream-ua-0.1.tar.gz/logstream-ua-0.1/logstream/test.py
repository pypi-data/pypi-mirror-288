from logstream import LogStream
import unittest, os

class Test(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.logfile_dir = logfile_dir = './logs.txt'
		with open(logfile_dir, 'w') as f:
			f.write('')

	def setUp(self):
		self.logstream = LogStream(self.logfile_dir)

	def testRecordCreating(self):
		new_record = self.logstream(description='Test', level=2)
		self.assertEqual(new_record, None)

	def testReadReport(self):
		lines = self.logstream.read()
		self.assertEqual(isinstance(lines, list), True)

	def testClearAllFile(self):
		clear_file  = self.logstream.clear()
		self.assertEqual(clear_file, None)

	@classmethod
	def tearDownClass(cls):
		logfile_dir = cls.logfile_dir
		if os.path.exists(logfile_dir):
			os.remove(logfile_dir)

if __name__ == '__main__':
	unittest.main()