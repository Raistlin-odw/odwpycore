import os

def getUserName():
    '''
    return login user name
    '''
    # For Linux
    if os.name == 'posix':
        # for linux, we use getpass
        import getpass
        return getpass.getuser()
    
    # For Windows
    else:
        # for windows, we can use both getpass and ctypes.wintypes
        """Return user name as login name.
        If name cannot be obtained return None.
    
        Returned value can be unicode or plain sring.
        To convert plain string to unicode use
        s.decode(bzrlib.user_encoding)
        """
        import ctypes
        UNLEN = 256
        advapi32 = ctypes.windll.advapi32
        try:
            GetUserName = getattr(advapi32, 'GetUserNameW')
        except AttributeError:
            print 'getUserName Error: can not find attribute "GetUserNameW1"'
            return None
        except Exception:
            # use simple print to log exception
            import traceback
            traceback.print_exc()
            # otherwise try env variables
            return os.environ.get('USERNAME')
        else:
            buf = ctypes.create_unicode_buffer(UNLEN+1)
            n = ctypes.c_int(UNLEN+1)
            if GetUserName(buf, ctypes.byref(n)):
                return buf.value