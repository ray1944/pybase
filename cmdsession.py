import json


class Cmdsession():
    '''recover previous job session
       like last part number, last server pid
       all session info was save in stream file in json format

    '''
    sessfile = '.sessald'
    def __init__(self, curpath):
        jsonobj = None
        self.fulpath = curpath + self.sessfile
        with open(self.fulpath, "a+") as fobj:
            try:
                jsonobj = json.load(fobj)
            except ValueError:
                print('No session before, setup a new one')

        self.serverids = []
        if jsonobj is not None:
            try:
                self.serverids  = jsonobj.serverids
            except AttributeError:
                print 'Json object has no serverids'
                del self.serverids[:]
                self.serverids = []
            try:
                self.lastprtid = jsonobj.lasprtid
            except:
                print 'Json object has no serverids'
                self.lastprtid = 1
        else:
            del self.serverids[:]
            self.serverids = []
            self.lastprtid = 1

    def savesess(self):
        with open(self.fulpath, "w") as fobj:
            data = {}
            data['serverids'] = self.serverids
            data['lastprtid'] = self.lastprtid
            json.dump(data, fobj)

    def __del__(self):
        self.savesess()

