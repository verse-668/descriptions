import connections

def get_passages_from_scripture(binary):
    delims = ['111011111100', '111101111100', '111100111101', '111101111011', '111011111011', '111011111101', '111100111011']
    passages = [[], [], [], [], [], [], []]
    x = 0
    current_passage = ''
    for i in range(0, len(binary), 6):
        c = binary[i:i+6]
        current_passage = current_passage + c
        delimcheck = current_passage[-24:]   
        if sum([len(s) for s in passages]) % 7 == 6:
            chapendcounter = c == '111011'
            for j in range(6, 90, 6):
                chapendcounter += current_passage[-j:-(j-6)] == '111011'
            if chapendcounter == 7:
                for s in range(7):
                    if len(passages[s]) == x // 7:
                        p = current_passage[:-84]
                        passages[s].append(p)
                        current_passage = ''
                        x += 1
                        chapendcounter = 0
                        break
            elif len(binary) - i == 6:
                for s in range(7):
                    if len(passages[s]) == x // 7:
                        p = current_passage
                        passages[s].append(p)
                        current_passage = ''
                        x += 1
                        chapendcounter = 0
                        break
                              
        if delimcheck[:12] in delims and delimcheck[12:] in delims and delimcheck[:12] != delimcheck[12:]:
            s = delims.index(delimcheck[:12])
            p = current_passage[:-24]
            passages[s].append(p)
            current_passage = ''
            x += 1
    return passages


def get_verses_from_passage(passage, alphabet):
    verses = [[],[],[]]
    currentverse = ''
    currentpart = 0
    verseend = False
    for i in range(0, len(passage), 6):
        c = passage[i:i+6]
        currentverse += c
        if c == '111000' or c == '111001':
            verseend = True
        if verseend and c == '110101':
            v = decode_binary(currentverse[:-6], alphabet, len(alphabet))
            verses[currentpart].append(v)
            currentverse = ''
            verseend = False
        if verseend and c == '111010':
            v = decode_binary(currentverse[:-6], alphabet, len(alphabet))
            verses[currentpart].append(v)
            currentpart += 1
            currentverse = ''
            verseend = False
    verses[currentpart].append(decode_binary(currentverse, alphabet, len(alphabet)))
    return verses
        
def get_data(passages, strandnames, alphabet):
    data = {}
    for i in range(len(strandnames)):
        name = strandnames[i]
        sdata = {}
        for j in range(7):
            pname = name + str(j + 1)
            verses = get_verses_from_passage(passages[i][j], alphabet)
            sdata[pname] = verses
        data[name] = sdata
    return data

def decode_binary(binary, alphabet, base):
    result = ''
    if base == 2:
        return binary
    elif base == 4:
        for i in range(0,len(binary), 2):
            c = binary[i:i+2]
            result = result + alphabet[int(c, 2)]
    elif base == 8:
        for i in range(0,len(binary), 3):
            c = binary[i:i+3]
            result = result + alphabet[int(c, 2)]
    elif base == 64:
        for i in range(0,len(binary), 6):
            c = binary[i:i+6]
            result = result + alphabet[int(c, 2)]
    return result
        
def get_connection_output(passages, connection):
    output = connection.__name__ + 'output:\n' 
    for s in passages:
        r = []
        for p in s:
            r.append(connection(p))
        output = output + str(r) + '\n'
    return output
            
with open('10.txt', 'r') as f:
    s = f.read()

passages = get_passages_from_scripture(s)

alph8 = '186*-TKS'
alph64 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\' ,\".?*@#^-_' 

verse_data = get_data(passages, ['AWM', 'TRL', 'LIM', 'RIT', 'RLI', 'TYX', 'WXY'], alph8)

with open('connection_outputs.txt', 'w') as f:
    print(get_connection_output(passages, connections.c1), file = f)
    print(get_connection_output(passages, connections.c2), file = f)
    print(get_connection_output(passages, connections.c3), file = f)
    print(get_connection_output(passages, connections.c4), file = f)
    print(get_connection_output(passages, connections.c5), file = f)
    print(get_connection_output(passages, connections.c6), file = f)
