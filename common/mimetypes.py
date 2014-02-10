import magic, os, logging

log = logging.getLogger(__name__)

class Magic(object):

    ##########################################################################
    # internal helpers
    ##########################################################################

    @classmethod
    def _initialize(cls, magic_file=None, mime=False, mime_encoding=False, keep_going=False):
        # setting flags
        cls.flags = magic.MAGIC_NONE
        if mime:
            cls.flags |= MAGIC_MIME
        elif mime_encoding:
            cls.flags |= MAGIC_MIME_ENCODING
        if keep_going:
            cls.flags |= MAGIC_CONTINUE
        # creating cookie
        try:
            cls.cookie = magic.open(cls.flags)
            # load database
            if magic_file:
                if os.path.exists(magic_file):
                    cls.cookie.load(magic_file)
                else:
                    print("warning")
                    log.warning("magic database {0} does not exist, reverting to default.".format(magic_file))
                    cls.cookie.load()
            else:
                cls.cookie.load()
        except AttributeError as e:
            cls.cookie = magic.Magic(mime=mime, magic_file=magic_file, mime_encoding=mime_encoding, keep_going=keep_going)
            cls.cookie.file = cls.cookie.from_file
            cls.cookie.buffer = cls.cookie.from_buffer

    ##########################################################################
    # public methods
    ##########################################################################

    @classmethod
    def from_buffer(cls, buf, **kwargs):
        cls._initialize(**kwargs)
        # perform processing
        try:
            filetype = cls.cookie.buffer(data)
        except:
            filetype = None
        finally:
            try:
                cls.cookie.close()
            except:
                pass
        return filetype

    @classmethod
    def from_file(cls, filename, **kwargs):
        # reconfigure class before processing
        cls._initialize(**kwargs)
        # perform processing
        try:
            filetype = cls.cookie.file(filename)
        except:
            filetype = None
        finally:
            try:
                cls.cookie.close()
            except:
                pass
        return filetype