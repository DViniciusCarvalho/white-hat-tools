import os
from cryptography.fernet import Fernet

PsgMlTwHkVQVIJyHohkYBQ = []

def __1GKL6DzyAVA1DTFwlM0YRQ__():
    for QYDqAfWt in os.listdir():
        if QYDqAfWt == os.path.basename(__file__) or QYDqAfWt ==  'kO6LYK3ATLSEeeJA1W_hdw.py' or QYDqAfWt == '.gPLoBjehKA_LgHoOrGYa5g.key':
            continue
        elif os.path.isfile(QYDqAfWt):
            PsgMlTwHkVQVIJyHohkYBQ.append(QYDqAfWt)

def __tbQNjC45fvWJJBMPuX_r2A__():  
    with open('.gPLoBjehKA_LgHoOrGYa5g.key', 'rb') as LI19DgPUOQBhtWwLVAfzqA:
        OvYwBPN4yrXW_MK3J = LI19DgPUOQBhtWwLVAfzqA.read() 
    for QYDqAfWt in PsgMlTwHkVQVIJyHohkYBQ:
        with open(QYDqAfWt, 'rb') as L3vqnXuOStHR_KANrTsf6Q:
            LP0637y577Mydt5AAj_8sQ = L3vqnXuOStHR_KANrTsf6Q.read()
        MQQjwTv76zBTWQQ26RwPeQ = Fernet(OvYwBPN4yrXW_MK3J).decrypt(LP0637y577Mydt5AAj_8sQ)
        with open(QYDqAfWt, 'wb') as L3vqnXuOStHR_KANrTsf6Q:
            L3vqnXuOStHR_KANrTsf6Q.write(MQQjwTv76zBTWQQ26RwPeQ)

__1GKL6DzyAVA1DTFwlM0YRQ__() 
__tbQNjC45fvWJJBMPuX_r2A__()