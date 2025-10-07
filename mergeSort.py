# simple merge sort to re-order the ips for readability
def mergeSortHostByValue(li):
    '''
    Basic merge sort specialised for sorting ips
    '''
    length = len(li)
    if length<2:
        return li
    
    first = mergeSortHostByValue(li[:int(length/2)])
    last = mergeSortHostByValue(li[int(length/2):])
    tmp = []

    for i in range(length):
        
        if len(first)==0:
            tmp.append(last.pop(0))
            continue
        elif len(last)==0:
            tmp.append(first.pop(0))
            continue
        # split the strings into sub-strings for better sorting
        firstval = first[0][0].split(".")
        lastval = last[0][0].split(".")

        if int(firstval[2])<int(lastval[2]): # sort by third quarter (255.255.!!!.255)
            tmp.append(first.pop(0))
        elif int(firstval[3])<int(lastval[3]): # sort by fourth quarter (255.255.255.!!!)
            tmp.append(first.pop(0))
        else:
            tmp.append(last.pop(0))
    return tmp