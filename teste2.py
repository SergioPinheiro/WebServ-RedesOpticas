counter = 0
findPath = False
finishSearch = False
i = 0
while(not finishSearch and (i < 10)):
    j = 0
    while(not finishSearch and (j<3)):
        k = 0
        while (not finishSearch and (k <2)):
            counter +=1;
            if(k==1):
                finishSearch = True
            k += 1
        j+=1
    i += 1

print(counter)