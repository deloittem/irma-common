import hashlib, unittest, tempfile
from irma.ftp.handler import FtpTls
from irma.common.exceptions import IrmaFtpError

##############################################################################
# Test Cases
##############################################################################
class FtpTestCase(unittest.TestCase):
    # Test config
    test_ftp_host = "localhost"
    test_ftp_port = "21"
    test_ftp_user = "testuser"
    test_ftp_passwd = "testpasswd"

    def setUp(self):
        # check database is ready for test
        self.ftp_running()
        self.flush_all()

    def tearDown(self):
        # do the teardown
        self.flush_all()

    def flush_all(self):
        # check that ftp server is empty before running tests
        try:
            ftps = FtpTls(self.test_ftp_host, self.test_ftp_port, self.test_ftp_user, self.test_ftp_passwd)
            ftps.deletepath("/")
        except IrmaFtpError as e:
            print "Testftp Error: {0}".format(e)
            self.skipTest(FtpTestCase)

    def ftp_running(self):
        # check that ftp is up before running tests
        try:
            FtpTls(self.test_ftp_host, self.test_ftp_port, self.test_ftp_user, self.test_ftp_passwd)
        except IrmaFtpError as e:
            print "Testftp Error: {0}".format(e)
            self.skipTest(FtpTestCase)



class CheckFtpHandler(FtpTestCase):

    def test_ftp_upload_file(self):
        ftps = FtpTls(self.test_ftp_host, self.test_ftp_port, self.test_ftp_user, self.test_ftp_passwd)
        hashname = ftps.upload_file("/", "test.ini")
        self.assertEquals(len(ftps.list("/")), 1)
        self.assertEquals(hashname , hashlib.sha256(open("test.ini").read()).hexdigest())

    def test_ftp_upload_data(self):
        ftps = FtpTls(self.test_ftp_host, self.test_ftp_port, self.test_ftp_user, self.test_ftp_passwd)
        with open("test.ini", 'rb') as f:
            hashname = ftps.upload_data("/", f.read())
        self.assertEquals(len(ftps.list("/")), 1)
        self.assertEquals(hashname , hashlib.sha256(open("test.ini").read()).hexdigest())

    def test_ftp_create_dir(self):
        ftps = FtpTls(self.test_ftp_host, self.test_ftp_port, self.test_ftp_user, self.test_ftp_passwd)
        ftps.mkdir("test1")
        self.assertEquals(len(ftps.list("/")), 1)

    def test_ftp_create_subdir(self):
        ftps = FtpTls(self.test_ftp_host, self.test_ftp_port, self.test_ftp_user, self.test_ftp_passwd)
        ftps.mkdir("/test1")
        ftps.mkdir("/test1/test2")
        ftps.mkdir("/test1/test2/test3")
        self.assertEquals(len(ftps.list("/")), 1)
        self.assertEquals(len(ftps.list("/test1")), 1)
        self.assertEquals(len(ftps.list("/test1/test2")), 1)
        self.assertEquals(len(ftps.list("/test1/test2/test3")), 0)

    def test_ftp_upload_in_subdir(self):
        ftps = FtpTls(self.test_ftp_host, self.test_ftp_port, self.test_ftp_user, self.test_ftp_passwd)
        ftps.mkdir("/test1")
        ftps.mkdir("/test1/test2")
        ftps.mkdir("/test1/test2/test3")
        hashname = ftps.upload_file("/test1/test2/test3", "test.ini")
        self.assertEquals(len(ftps.list("/test1/test2/test3")), 1)
        self.assertEquals(hashname , hashlib.sha256(open("test.ini").read()).hexdigest())

    def test_ftp_remove_not_existing_file(self):
        ftps = FtpTls(self.test_ftp_host, self.test_ftp_port, self.test_ftp_user, self.test_ftp_passwd)
        with self.assertRaises(IrmaFtpError):
            ftps.delete(".", "lkzndlkaznd")

    def test_ftp_remove_not_existing_dir(self):
        ftps = FtpTls(self.test_ftp_host, self.test_ftp_port, self.test_ftp_user, self.test_ftp_passwd)
        with self.assertRaises(IrmaFtpError):
            ftps.deletepath("/test1", deleteParent=True)

    def test_ftp_modify_file_hash(self):
        ftps = FtpTls(self.test_ftp_host, self.test_ftp_port, self.test_ftp_user, self.test_ftp_passwd)
        hashname = ftps.upload_file("/", "test.ini")
        altered_name = "0000" + hashname[4:]
        ftps._conn.rename(hashname, altered_name)
        self.assertEquals(len(hashname), len(altered_name))
        _, tmpname = tempfile.mkstemp(prefix="test_ftp")
        with self.assertRaises(IrmaFtpError):
            ftps.download(".", altered_name, tmpname)

if __name__ == '__main__':
    unittest.main()
