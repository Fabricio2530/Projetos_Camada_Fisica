from datetime import datetime
def server(server,com,type,packageSize,n,n_packages=68,CRC="0000"):
    if type == 3:
        line =  str(datetime.today())+" / "+str(com)+" / "+str(type)+" / "+str(packageSize)+" / "+str(n)+" / "+str(n_packages)+" / "+str(CRC)
    else:
        line =  str(datetime.today())+" / "+str(com)+" / "+str(type)+" / "+str(packageSize)
    
    newFile = open(f"Server{server}.txt", "a")
    newFile.writelines("\n"+line)
    newFile.close()
