# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import urllib.request
url = 'https://forum.ubuntu-tr.net/index.php'
file, headers = urllib.request.urlretrieve(url)
statistic_dict, online_member_dict  = {}, {}
userid = []
def cutstring(string, referans, start, end):
    return string[string.find(start, string.find(referans)+len(referans))+len(start):string.find(end,
                    string.find(start, string.find(referans)+len(referans))+len(start))]
def cutreplace(line, ref, end='</div>'):
    if ref == 'img': ref = '<img' #1
    try:
        if line.find(ref) > -1:  
            for ch in range(0, len(line), +1):
                if line[ch:ch+len(ref)] == ref:
                    k = line.find(end, line.find(ref))-line.find(ref)
                    line = line.replace(line[ line.find(ref):line.find(ref)+k ] + str(end), '')
            return line
        else:
            return line
    except:
        pass
def trim(string):
    index = []
    for trim in range(0, len(string), +1):
        if string[trim:trim+1] != ' ': 
            index.append(trim)
            break   
    for trim in range(len(string)-1,-1, -1):
        if string[trim:trim+1] != ' ': 
            index.append(trim+1)
            break
    return string[index[0]:index[1]]
def cut(line, ref, end='</div>'):
    line = trim(line)
    for ch in range(len(line), -1, -1):
        if line[ch:ch+len(ref)] == ref:
            return line[ch+len(ref):len(line)-len(end)-1]



class member:
    def last(self):
        global lastmember
        data = open(file)
        for line in data.readlines():
            if line.find('Forum İstatistikleri') is not -1:
                continue
            elif line.find('Son Üye:') is not -1:
                lastmember = cutstring(line, 'action=profile', '>', '<').encode('Utf-8').strip()
                break
        return lastmember

class statistic:
    def beta(self):
        global test
        data = open(file)
        for line in data.readlines():
            if line.find('Forum İstatistikleri') is not -1:
                continue
            elif line.find('Son Üye:') is not -1:
                test = line[0:line.find('Konu')].strip()
                test = test +' '+ 'Konu'
                test = test.encode('Utf-8').split()
                statistic_dict['statistic'] = {'ileti':int(test[0]), 'konu':int(test[-2])}
                break
        return statistic_dict


class online:
    def member(self):
        data = open(file)
        for line in data.readlines():
            if line.find('Son 60 dakika içinde aktif olan üyeler') > 0:
                for on in range(0, len(line), +1):
                    if line[on:on+len('action=profile;')] == 'action=profile;':
                        startuid = line.find('u=' ,on)
                        uid = line[startuid:startuid+line.find('"', startuid)-startuid][2:]
                        userid.append(uid)
                        user = cutstring(line, userid[-1], '>', '<')
                        online_member_dict[user] = {'u':int(uid)}
        return online_member_dict
member = member()
member.last()
statistic = statistic()
statistic.beta()
online = online()
online.member()