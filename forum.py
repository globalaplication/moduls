# -*- coding: utf-8 -*-
#!/usr/bin/env python
import urllib
url = 'https://forum.ubuntu-tr.net/index.php?action=recent'
data = urllib.urlopen(url)
beta, dict, test = {}, {}, {}
repl = {'<br />':'', '</div>':'<END>', '&#039;':"'", '&nbsp;':'', '&quot;':'', '<b>':'', '</b>':''}
def cutstring(string, referans, start, end):
    for replace in repl:
        string = string.replace(replace, repl[replace])
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
class beta:
    def recent(self):
        counter, chapter, subject, profile, date, post = '', '', '', '', '', ''
        for line in data.readlines():
            for rep in repl: line = line.replace(rep, repl[rep])
            line = cutreplace(line, '<span style="color: red;" class="bbc_color">', '</span>')
            line = cutreplace(line, 'img', '/>')
            line = cutreplace(line, '<span class="bbc_u">', '</span>')
            line = cutreplace(line, '<div class="codeheader">', '</code>')
            line = cutreplace(line, '<a href="#"', '</a>')
            for rep in repl: line = line.replace(rep, repl[rep])
            if line.find('<div class="counter">') is not -1:
                counter = cutstring(line, 'counter', '>', '<')
                continue
            if line.find('<h5>') is not -1:
                chapter = cutstring(line, '<h5>', '>', '<')
                dict[counter] = {'counter':counter, 'chapter':chapter, 'subject':subject, 'profile':profile, 'date':date, 'post':post}
            if line.find('nofollow') is not -1:
                subject = cutstring(line, 'nofollow', '>', '<')
                dict[counter] = {'counter':counter, 'chapter':chapter, 'subject':subject, 'profile':profile, 'date':date, 'post':post}
                continue
            if line.find('<span class="smalltext">') is not -1:
                profile = cutstring(line, 'action=profile', '>', '<')
                dict[counter] = {'counter':counter, 'chapter':chapter, 'subject':subject, 'profile':profile, 'date':date, 'post':post}
            if line.find('<span class="smalltext">') is not -1:
                date = cutstring(line, 'action=profile', '<em>', '</em>')
                dict[counter] = {'counter':counter, 'chapter':chapter, 'subject':subject, 'profile':profile, 'date':date, 'post':post}
                continue
            list_post = line.find('<div class="list_posts">')
            bbc_code = line.find('<code class="bbc_code">')
            if bbc_code is not -1: bbc_code = 1
            codeheader = line.find('<div class="codeheader">')
            if codeheader is not -1: codeheader = 1
            smfSelectText = line.find('onclick="return smfSelectText(this);')
            if smfSelectText is not -1: smfSelectText = 1
            topslice_quote = line.find('<div class="topslice_quote">')
            if topslice_quote is not -1: topslice_quote = 1
            bbc_link = line.find('class="bbc_link" target="_blank"')
            if bbc_link is not -1: bbc_link = 1
            bbc_img = line.find('<img src=')
            if bbc_img is not -1: bbc_img = 1
            bbc_size = line.find('class="bbc_size"')
            if bbc_size is not -1: bbc_size = 1
            botslice_quote = line.find('<div class="botslice_quote">')
            if botslice_quote is not -1: botslice_quote = 1

            if list_post is not -1:
                #line = cutreplace(line, '<a href', '</a>')
                #print counter, {'bbc_code':bbc_code, 'codeheader':codeheader, 'smfSelectText':smfSelectText, 'topslice_quote':topslice_quote, 'bbc_link':bbc_link, 'bbc_img':bbc_img, 'bbc_size':bbc_size, 'botslice_quote':botslice_quote}
                if bbc_code is -1 and codeheader is -1 and smfSelectText is -1 and topslice_quote is -1 and bbc_link is -1: 
                    if bbc_img == -1 and bbc_size == -1 and botslice_quote == -1:
                        post = cut(line, '<div class="list_posts">' ,'<END>')
                        dict[counter] = {'counter':counter, 'chapter':chapter, 'subject':subject, 'profile':profile, 'date':date, 'post':post}
                        continue
                if bbc_code is -1 and codeheader is -1 and smfSelectText is -1 and topslice_quote is -1 and bbc_link is 1: #target
                    if bbc_img == -1 and bbc_size == -1 and botslice_quote == -1:
                        post = cutstring(line, 'class="bbc_link" target="_blank"' ,'</a>', '<END>')
                        dict[counter] = {'counter':counter, 'chapter':chapter, 'subject':subject, 'profile':profile, 'date':date, 'post':post}
                        continue
        return dict
class member:
    def last(self):
        url = 'https://forum.ubuntu-tr.net/index.php'
        data = urllib.urlopen(url)
        for line in data.readlines():
            if line.find('Forum İstatistikleri') is not -1:
                continue
            elif line.find('Son Üye:') is not -1:
                lastmember = cutstring(line, 'action=profile', '>', '<').decode('Utf-8').strip()
                break
        return lastmember
class statistic:
    def beta(self):
        url = 'https://forum.ubuntu-tr.net/index.php'
        data = urllib.urlopen(url)
        for line in data.readlines():
            if line.find('Forum İstatistikleri') is not -1:
                continue
            elif line.find('Son Üye:') is not -1:
                beta = line[0:line.find('Konu')].decode('Utf-8').strip()
                beta = beta + ' '+ 'Konu'
                beta = beta.split()
                test['statistic'] = {'ileti':int(beta[0]), 'konu':int(beta[-2])}
                break
        return test
class online:
    def member(self):
        url = 'https://forum.ubuntu-tr.net/index.php'
        data = urllib.urlopen(url)
        id, online_member = [], {}
        for line in data.readlines():
            if line.find('Son 60 dakika içinde aktif olan üyeler') > 0:
                for on in range(0, len(line), +1):
                    if line[on:on+len('action=profile;')] == 'action=profile;':
                        startuid = line.find('u=' ,on)
                        uid = line[startuid:startuid+line.find('"', startuid)-startuid][2:]
                        id.append(uid)
                        user = cutstring(line, id[-1], '>', '<')
                        online_member[user] = {'id':uid}
        return online_member
online = online()
online.member()
member = member()
member.last()
beta = beta()
beta.recent()
statistic = statistic()
statistic.beta()
