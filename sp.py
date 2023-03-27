import math
import numpy as np
import scipy
fs = 12000
def bearing_fault_freq_cal(n, d, D, alpha, fr=None):
    '''
    基本描述：
        计算滚动轴承的故障特征频率
    详细描述：
        输入4个参数 n, fr, d, D, alpha
    return C_bpfi, C_bpfo, C_bsf, C_ftf,  fr
           内圈    外圈    滚针   保持架  转速

    Parameters
    ----------
    n: integer
        The number of roller element
    fr: float(r/min)
        Rotational speed
    d: float(mm)
        roller element diameter
    D: float(mm)
        pitch diameter of bearing
    alpha: float(°)
        contact angle
    fr:：float(r/min)
        rotational speed
    Returns
    -------
    BPFI: float(Hz)
        Inner race-way fault frequency
    BPFO: float(Hz)
        Outer race-way fault frequency
    BSF: float(Hz)
        Ball fault frequency
    FTF: float(Hz)
        Cage frequency
    '''
    C_bpfi = n*(1/2)*(1+d/D*np.math.cos(alpha))
    C_bpfo = n*(1/2)*(1-(d/D)*np.math.cos(alpha))
    C_bsf = D*(1/(2*d))*(1-np.square(d/D*np.math.cos(alpha)))
    C_ftf = (1/2)*(1-(d/D)*np.math.cos(alpha))
    if fr!=None:
        return C_bpfi*fr/60, C_bpfo*fr/60, C_bsf*fr/60, C_ftf*fr/60, fr/60
    else:
        return C_bpfi, C_bpfo, C_bsf, C_ftf, fr


def cal_Ls1(bpfi, bpfo, bsf, ftf, fs, a):
    return (a*fs)/np.min([bpfi, bpfo, bsf, ftf])



def input_size(bpfi, bpfo, bsf, ftf, order, fs):
    b = []
    a = np.array([bpfi, bpfo, bsf, ftf])
    for i in range(1, order+1):
        b.extend(a*i)
    b = np.abs(np.array(b)[:, np.newaxis] - np.array(b)[np.newaxis, :])
    b = b[b !=0]
    b = np.min(b)
    return fs/b


bpfi, bpfo, bsf, ftf, fr = bearing_fault_freq_cal(n=9, alpha=0, d=7.94, D=39.04, fr=1730)
# print(np.min([bpfi, bpfo, bsf, ftf]))
Ls1 = cal_Ls1(bpfi, bpfo, bsf, ftf, fs=fs, a=2)
# print(Ls1)
# print('内圈故障特征频率',bpfi)
# print('外圈故障特征频率',bpfo)
# print('滚动体故障特征频率',bsf)
# print('保持架故障特征频率',ftf)
# print(fr)
Ls2 = input_size(bpfi, bpfo, bsf, ftf, order=5, fs=fs)
Ls = np.ceil(np.sqrt(np.max([Ls1, Ls2])))**2
H = np.ceil([fs/fr])
W = np.ceil(Ls/H)
print(H)
print(W)

def kernel_width(m,B):
    # A_0 = np.max(data)
    # at = np.sqrt(scipy.signal.hilbert(data)**2+data**2)  #获得信号的包络
    return np.ceil(-math.log(m)/B*fs)
f = np.arange(0.1,1.0,0.1)
B = 654
print(f)
for i in f:
    print(kernel_width(m=i, B=B))
b = kernel_width(m=0.8, B=B)
print(b)








