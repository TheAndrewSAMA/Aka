from sopel.module import commands, rule, event
import re
# prova
@event('JOIN')
@rule(r'.*')
def akajoin(bot, trigger):
    '''Controlla la presenza di un nick nel registro quando l'utente entra nel canale'''

    #Assegnazione delle variabili nick ed host
    nick = '%' + trigger.nick + '%'                        #Aggiunta del carattere percentuale ai lati del nick per evitare errori nel controllo
    nick_lo = nick.lower()
    host = trigger.host

    #Lettura del registro
    reg = read()
    reg_lo = reg.lower()

    #Ciclo di controllo
    if (host not in reg) and (nick_lo not in reg_lo):      #Se il nick e l'host non sono nel registro
        reg = reg.splitlines() 
        reg.append(host + ':' + nick)                      #Aggiungili alla fine, separati dai due punti
    elif (nick_lo in reg_lo) and (host in reg):            #Se ci sono entrambi, esci
        return
    else:                                                  #Altrimenti:
        reg = reg.splitlines()
        for x in range(len(reg)):                        
            line = reg[x]
            line_lo = line.lower()
            if (nick_lo in line_lo) and (host not in line):      #Se c'è già il nick, aggiungi l'host
                reg[x] = host + ', ' + line
            elif (host in line) and (nick_lo not in line_lo):    #Se c'è già l'host, aggiungi il nick
                reg[x] = line + ', ' + nick

    reg = '\n'.join(reg)                                   #Unisci la lista di linee in una sola stringa

    write(reg)                                             #Scrivi il registro

    return

@event('NICK')
@rule(r'.*')
def akanick(bot, trigger):
    '''Controlla la presenza di un nick nel registro quando l'utente lo cambia'''

    #Assegnazione delle variabili nick ed host
    nick = '%' + trigger.args[0] + '%'                        #Aggiunta del carattere percentuale ai lati del nick per evitare errori nel controllo
    nick_lo = nick.lower()
    host = trigger.host

    #Lettura del registro
    reg = read()
    reg_lo = reg.lower()

    #Ciclo di controllo
    if (host not in reg) and (nick_lo not in reg_lo):      #Se il nick e l'host non sono nel registro
        reg = reg.splitlines() 
        reg.append(host + ':' + nick)                      #Aggiungili alla fine, separati dai due punti
    elif (nick_lo in reg_lo) and (host in reg):            #Se ci sono entrambi, esci
        return
    else:                                                  #Altrimenti:
        reg = reg.splitlines()
        for x in range(len(reg)):                        
            line = reg[x]
            line_lo = line.lower()
            if (nick_lo in line_lo) and (host not in line):      #Se c'è già il nick, aggiungi l'host
                reg[x] = host + ', ' + line
            elif (host in line) and (nick_lo not in line_lo):    #Se c'è già l'host, aggiungi il nick
                reg[x] = line + ', ' + nick

    reg = '\n'.join(reg)                                   #Unisci la lista di linee in una sola stringa

    write(reg)                                             #Scrivi il registro

    return

def write(reg):
    '''Scrive il file di registro'''
    reg_file = open("aka.txt", "w")
    reg_file.write(reg)
    reg_file.close()
    return

def read():
    '''Legge il file di registro'''
    reg_file = open("aka.txt", "r")
    reg = reg_file.read()
    reg_file.close
    return reg

@commands('aka')
def akasearch(bot, trigger):
    '''Scrive l'elenco di nick usati da un utente'''
    
    if trigger.sender != bot.config.aka.channels:
        return
    
    #Assegnazione variabili
    nick_cln = trigger.group(2).strip()                   #Toglie gli spazi dal nick
    nick_reg = '%' + nick_cln + '%'                       #Aggiunge dei caratteri delimitatori intorno al nick
    nick_reg_lo = nick_reg.lower()

    #Lettura del registro
    reg = read()                                          #Legge il registro
    reg_lo = reg.lower()

    if nick_reg_lo not in reg_lo:                                         #Se il nick non è nel registro
        bot.say("Non ci sono dati su '" + nick_cln + "'.")  
    else:                                                           #Se c'è:
        reg = reg.splitlines()
        for x in range(len(reg)):                                   #Per ogni linea del registro
            line = reg[x]
            nicks_start = line.rfind(":") + 1
            nicks = line[nicks_start:]
            nicks_lo = nicks.lower()
            if nick_reg_lo in nicks_lo and nicks_lo != nick_reg_lo:
                if 'irccloud' in line:
                    msg = " usa una bnc pubblica. Dal suo indirizzo si sono connessi questi nick: "
                else:
                    msg = " ha usato altri nick: "
                nicks = nicks.replace('%', '')
                nick_cln_re0 = re.compile(nick_cln + ', ', re.IGNORECASE)
                nick_cln_re1 = re.compile(', ' + nick_cln + ',', re.IGNORECASE)
                nick_cln_re2 = re.compile(', ' + nick_cln, re.IGNORECASE)
                bf = line[line.find(nick_reg) - 1]
                try:
                    af = line[line.find(nick_reg) + len(nick_reg)]
                except IndexError:
                    af = '.'
                if bf == ':' and af == ',':
                    bot.say(nick_cln + msg + nick_cln_re0.sub('', nicks) + ".")
                elif bf == ',' and af == ',':
                    bot.say(nick_cln + msg + nick_cln_re1.sub('', nicks) + '.')
                else:
                    bot.say(nick_cln + msg + nick_cln_re2.sub('', nicks) + '.')
            elif nick_reg_lo in nicks_lo and nicks_lo == nick_reg_lo:           #Se il nick è l'unico nella lista:
                bot.say("Non sembra che " + nick_cln + " abbia usato altri nick.")
    return


