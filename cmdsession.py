import json
import os
import logging


class Cmdsession():
    '''recover previous job session
       like last part number, last server pid
       all session info was save in stream file in json format

    '''
    sessfile = '.sessald'
    lasterrors = []
    def __init__(self, curpath):
        jsonobj = None
        self.workpath = curpath
        self.sesspath = os.path.join(self.workpath, self.sessfile)
        with open(self.sesspath, "a+") as fobj:
            try:
                jsonobj = json.load(fobj)
            except ValueError:
                print('No session before, setup a new one')

        self.serverids = []
        if jsonobj is not None:
            try:
                self.serverids  = jsonobj['serverids'][:]
            except AttributeError:
                print 'Json object has no serverids'
                del self.serverids[:]
                self.serverids = []
            try:
                self.lastchkoutprtid = jsonobj['lastchkoutprtid']
                self.lastchkinprtid = jsonobj['lastchkinprtid']
            except:
                print 'Json object has no serverids'
                self.lastchkoutprtid = 1
                self.lastchkinprtid = 1
        else:
            del self.serverids[:]
            self.serverids = []
            self.lastchkoutprtid = 1
            self.lastchkinprtid = 1
        logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s',
            datefmt='%a, %d %b %Y %H:%M:%S',
            filename=os.path.join(self.workpath, '.sesslog'),
            filemode='w')

    def savesess(self):
        with open(self.sesspath, "w") as fobj:
            data = {}
            data['serverids'] = self.serverids
            data['lastchkoutprtid'] = self.lastchkoutprtid
            data['lastchkinprtid'] = self.lastchkinprtid
            json.dump(data, fobj)

    def __del__(self):
        self.savesess()

    def log(self, logmsg):
        logging.info(logmsg)


