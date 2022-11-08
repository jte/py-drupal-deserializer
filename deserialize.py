import sys
import re

def deserialize(serialized):
    array = []
    i = 0
    while i < len(serialized):
        stype = serialized[i]
        if stype == 'a':
            match = re.search(r'a:(\d+):', serialized[i:])
            if match is None:
                print ('Error matching array descriptor at {}'.format(i))
                break
            scount = match.group(1)
            done = False
            curr = i + (match.span()[1] - match.span()[0])
            stackpos = 0
            stack = []
            # Use stack to find matching braces
            while not done:
                if serialized[curr] == '{':
                    stack.append({'open_at': curr})
                    stackpos = stackpos + 1
                elif serialized[curr] == '}':
                    stackpos = stackpos - 1
                    stack[stackpos]['close_at'] = curr
                    if stackpos == 0:
                        done = True
                curr = curr + 1
            open_at = stack[0]['open_at']
            close_at = stack[0]['close_at']
            result = deserialize(serialized[open_at + 1 : close_at])
            array += [result]
            i = close_at + 1
        elif stype == 's':     
            match = re.search(r's:(\d+):', serialized[i:])
            if match is None:
                print ('Error matching string descriptor at {}'.format(i))
                break
            slen = int(match.group(1))
            start = i + (match.span()[1] - match.span()[0])
            scontent = ''
            bstart = 0
            bend = 0
            serialized_bytes = serialized[start:].encode('utf-8')
            if serialized_bytes[0] == ord('"') and serialized_bytes[1] == ord('"') and serialized_bytes[2 + slen] == ord('"') and serialized_bytes[2 + slen + 1] == ord('"'):
                bstart = 2
                bend = 2+slen
                i = start + 2 + slen + 2
            elif serialized_bytes[0] == ord('"'):
                if serialized_bytes[1 + slen] == ord('"'):
                    bstart = 1
                    bend = 1 + slen
                    i = start + 1 + slen + 1
                else:
                    print ('Error string mismatch 1 at {}'.format(start))
                    break
            else:
                print ('Error string mismatch 2 at {}'.format(start))
                break
            serialized_bytes = serialized_bytes[bstart:bend]
            scontent = serialized_bytes.decode('utf-8')
            array += [scontent]
            if i < len(serialized) and serialized[i] == ';':
                i += 1
        elif stype == 'i':
            match = re.search(r'i:(\d+);', serialized[i:])
            if match is None:
                print ('Error matching string descriptor at {}'.format(i))
                break
            integer = match.group(1)
            array += [integer]
            i += (match.span()[1] - match.span()[0])
            if i < len(serialized) and serialized[i] == ';':
                i += 1
        elif stype == 'O':
            print ('Error ! Object descriptor not supported')
        elif stype == 'b':
            match = re.search(r'b:(\d+);', serialized[i:])
            if match is None:
                print ('Error matching boolean descriptor at {}'.format(i))
                break
            boolean = match.group(1)
            array += [boolean]
            i += (match.span()[1] - match.span()[0])
        elif stype == 'N':
            match = re.search(r'N;', serialized[i:])
            if match is None:
                print ('Error matching null descriptor at {}'.format(i))
                break
            i += (match.span()[1] - match.span()[0])
        else:
            print ('Unknown descriptor at {} - {}'.format(i, serialized[i-10:i+10]))
            break
    return array