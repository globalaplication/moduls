# -*- coding: utf-8 -*-
#!/usr/bin/env python
import forum, time
beta, ubuntu, string  = [], [], ''
while(True):
    ubuntu = forum.online.user().keys()
    if len(beta) is 0:
        beta = ubuntu
    if len(ubuntu) < len(beta):
        for test in beta:
            if test not in ubuntu:
                forum.balloon('forum.ubuntu-tr.net.png', 'offline', test)
                string = string.replace(test, '')
            beta = ubuntu
    else:
        for test in ubuntu:
            if test not in beta:
                forum.balloon('forum.ubuntu-tr.net.png','online', test)
                beta.append(test)
    for user in ubuntu:
        if string.find(user) is -1: 
            string = string + ' ' + str(user)
    time.sleep(60)
