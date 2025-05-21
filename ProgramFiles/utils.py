#Code that assigns a historical price and section name using the section number




def assign_price(section,price_list) :
    #Hard coding the indices for each section, will use later when assigning historical ticket prices

    di = [31,32,33,34,35,16,17,18,19,20,21]
    dr = [13,14,15,36,37,38,39]
    dc = [10,11,12,40,41,42]
    diamc = [107,108,109,110,111,112,140,141,142,143]
    tc = list(range(1,10))
    chairman = list(range(22,31))
    execs = list(range(122,131))
    diami = [131,133,135,120,118,116]
    diamr = [113,114,137,138]
    hrp = list(range(144,156))
    cht = list(range(156,161))
    cht.append(257)
    cht.append(258)
    li = [233,235,237,238,216,217,218]
    xc = list(range(220,232))
    lr = [213,214,215,239,240,241]
    lc = [210,211,212,243,242]
    hat = [244,245,246]
    ccc = [354,346,347]
    vc = list(range(340,345)) + [312,313,314]
    vr = [335,337,339,317,316,315]
    vi = list(range(318,334))
    gi = list(range(417,436))
    gr = [410,411,412,413,414,415,416,437,438]
    ga = list(range(439,445))

    #Write Ticket price to file
    #Have to get price from section number using conditional statement

    if (section.isdigit()):
        seat = int(section)
    else :
        seat = 1000

    #Getting sections into the groupings the braves use for pricing, also adding the historical price point 
    if (seat in di ):
        cat = 'Dugout Infield'
        price_hist = 185
        price = price_list[0]
    elif (seat in dr):
        cat = 'Dugout Reserved'
        price_hist = 150
        price = price_list[1]
    elif (seat in dc):
        cat = 'Dugout Corner'
        price_hist = 105
        price = price_list[2]
    elif (seat in diami):
        cat = 'Diamond Infield'
        price_hist = 140
        price = price_list[3]
    elif (seat in diamr):
        cat = 'Diamond Reserved'
        price_hist = 105
        price = price_list[4]
    elif (seat in diamc):
        cat = 'Diamond Corner'
        price_hist = 50
        price = price_list[5]
    elif (seat in tc):
        cat = 'Truist Club'
        price_hist = 400
        price = price_list[0] * 2
    elif (seat in chairman):
        cat = 'Chairman Seats'
        price_hist = 350
        price = price_list[0] * 1.5
    elif (seat in execs):
        cat = 'Executive Seats'
        price_hist = 300
        price =  price = price_list[3]*1.5
    elif (seat in cht):
        cat = 'Chop House'
        price_hist = 75
        price = price_list[6]
    elif (seat in hrp):
        cat = 'Home Run Porch'
        price_hist = 50
        price = price_list[7]
    elif (seat in xc):
        cat = 'XFINITY club seats'
        price_hist = 200
        price = 200
    elif (seat in li):
        cat = 'Lexus Infield'
        price_hist = 95
        price = price_list[8]
    elif (seat in lr):
        cat = 'Lexus Reserved'
        price_hist = 70
        price = price_list[9]
    elif (seat in lc):
        cat = 'Lexus Corner'
        price_hist = 50
        price = price_list[10]
    elif (seat in hat):
        cat = 'Hank Aaron Terrace'
        price_hist = 100
        price = price_list[14]*2
    elif (seat in ccc):
        cat = 'Coca Cola Corner'
        price_hist = 50
        price = price_list[14]
    elif (seat in vc):
        cat = 'Vista Corner'
        price_hist = 20
        price = price_list[13]
    elif (seat in vi):
        cat = 'Vista Infield'
        price_hist = 35
        price = price_list[1]
    elif (seat in vr):
        cat = 'Vista Reserved'
        price_hist = 30
        price = price_list[11]
    elif (seat in gi):
        cat = 'Granstand Infield'
        price_hist = 25
        price = price_list[15]
    elif (seat in gr):
        cat = 'Granstand Reserved'
        price_hist = 20
        price = price_list[16]
    elif (seat in ga):
        cat = 'General Admission'
        price_hist = 15
        price = price_list[17]
    else :
        cat = 'other'
        price_hist = 200
        price = 200

    return str(price) +  ',' + str(cat) + ',' + str(price_hist) 





