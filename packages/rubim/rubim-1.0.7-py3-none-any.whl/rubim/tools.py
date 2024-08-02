from filetype import video_match,image_match

class tools:

    def getTypeByte(byte:bytes):
        if video_match(byte) != None:return 'Video'
        elif image_match(byte) != None:return 'Picture'
        else:raise FileNotFoundError('File Format Not Found')
        
    def noneKeysFind(dict_method:list):
        for x in tuple(dict_method):
            if dict_method[x] == None or dict_method[x] == "":dict_method.pop(x)
        if len(dict_method.keys()) != 0:return dict_method
        else:raise ValueError('Enter at least one argument')

    def dictFind(dictList:list,key,value):
        for d in dictList:
            try:
                if d[key] == value:return d
            except KeyError:raise KeyError('Key Not Found')
        return jsonEror.NOT_FOUND
        
class jsonEror:

    NOT_FOUND = {"status":"EROR_GENERIC","status_det":"NOT_FOUND"}

    USERNAME_EXIST = {"status":"EROR_GENERIC","status_det":"USERNAME_EXIST"}

    PERMISSION_DENIED = {"status":"EROR_GENERIC","status_det":"PERMISSION_DENIED"}