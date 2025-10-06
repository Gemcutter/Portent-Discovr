def validateUserOptions(user_options):
    '''
    Checks to see if all inputs are of the correct data type, within appropriate range, and structured correctly 
    '''
    rangeMinValid = True
    rangeMaxValid = True
    intensityValid = True
    timeoutValid = True
    try:
        minRangeSplit = user_options['rangeMin'].split(".")
        if len(minRangeSplit) != 4 or type(user_options['rangeMin']) != str or len(minRangeSplit) == 4 and (int(minRangeSplit[0])>255 or int(minRangeSplit[0])<0 or int(minRangeSplit[1])>255 or int(minRangeSplit[1])<0 or int(minRangeSplit[2])>255 or int(minRangeSplit[2])<0 or int(minRangeSplit[3])>255 or int(minRangeSplit[3])<0):
            rangeMinValid = False
    except Exception as e:
        rangeMinValid = False
    try:
        maxRangeSplit = user_options['rangeMax'].split(".")
        rangeMaxValid = compareIpValues(user_options['rangeMin'], user_options['rangeMax'])
        if len(maxRangeSplit) != 4 or type(user_options['rangeMax']) != str or len(maxRangeSplit) == 4 and (int(maxRangeSplit[0])>255 or int(maxRangeSplit[0])<0 or int(maxRangeSplit[1])>255 or int(maxRangeSplit[1])<0 or int(maxRangeSplit[2])>255 or int(maxRangeSplit[2])<0 or int(maxRangeSplit[3])>255 or int(maxRangeSplit[3])<0):
            rangeMaxValid = False
    except Exception as e:
        rangeMaxValid = False
    try:
        if int(user_options['intensity']) > 5 or int(user_options['intensity']) <= 0:
            intensityValid = False
    except Exception as e:
        intensityValid = False
    try:
        if int(user_options['timeout']) < 5:
            timeoutValid = False
    except Exception as e:
        timeoutValid = False

    return rangeMinValid, rangeMaxValid, intensityValid, timeoutValid

def compareIpValues(min, max):
    splitMin = min.split('.')
    splitMax = max.split('.')
    if splitMin[0]>splitMax[0] or splitMin[1]>splitMax[1] and splitMin[0]>=splitMax[0] or splitMin[2]>splitMax[2] and splitMin[1]>=splitMax[1] and splitMin[0]>=splitMax[0] or splitMin[3]>splitMax[3] and splitMin[2]>=splitMax[2] and splitMin[1]>=splitMax[1] and splitMin[0]>=splitMax[0]:
        return False
    else:
        return True