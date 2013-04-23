def getUserName():
    '''
    get login user name
    '''
    # test
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
        from ctypes.wintypes import MAX_PATH
        UNLEN = 256
        try:
            advapi32 = ctypes.windll.advapi32
            GetUserName = getattr(advapi32, 'GetUserNameW')
        except :
            # otherwise try env variables
            return os.environ.get('USERNAME', None)
        else:
            buf = ctypes.create_unicode_buffer(UNLEN+1)
            n = ctypes.c_int(UNLEN+1)
            if GetUserName(buf, ctypes.byref(n)):
                return buf.value
    