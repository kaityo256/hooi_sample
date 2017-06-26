from PIL import Image
import os
import sys
import numpy as np
from scipy import linalg

def restored_tensor(X,a1,a2):
    pa1 = a1.T.dot(a1)
    pa2 = a2.T.dot(a2)
    X2 = np.tensordot(X,pa1,(1,0))
    X3 = np.tensordot(X2,pa2,(0,0))
    return X3.transpose(2,1,0)

def save_img(X, filename):
    Image.fromarray(np.uint8(X)).save(filename)
    print('Saved as ' + filename)

def hosvd(filename,ratio):
    path, ext = os.path.splitext(filename)
    img = Image.open(filename)
    w = img.width
    h = img.height
    X = np.asarray(img)
    X1 =  X.transpose(0,2,1).reshape(h*3,w)
    X2 = X.transpose(1,2,0).reshape(w*3,h)
    U,s,A1 = linalg.svd(X1)
    U,s,A2 = linalg.svd(X2)
    r1 = int(w*ratio)
    r2 = int(h*ratio)
    a1 = A1[:r1, :]
    a2 = A2[:r2, :]
    XP = restored_tensor(X, a1, a2)
    filename = path+'_hosvd'+ ext
    print linalg.norm(X-XP)/linalg.norm(X)
    save_img(XP, filename)

def hooi(filename, ratio):
    path, ext = os.path.splitext(filename)
    img = Image.open(filename)
    w, h = img.size
    r1 = int(w*ratio)
    r2 = int(h*ratio)
    X = np.asarray(img)
    np.random.seed(0)
    X1 = np.random.rand(w,w)
    X2 = np.random.rand(h,h)
    U,s,A1 = linalg.svd(X1)
    U,s,A2 = linalg.svd(X2)
    a1 = A1[:r1, :]
    a2 = A2[:r2, :]
    XP = restored_tensor(X,a1,a2)
    for i in range(10):
    	X1 = np.tensordot(X,a2.T,(0,0)).transpose(2,1,0).reshape(r2*3,w)
    	U,s,A1 = linalg.svd(X1)
    	a1 = A1[:r1, :]
    	X2 = np.tensordot(X,a1.T,(1,0)).transpose(2,1,0).reshape(r1*3,h)
    	U,s,A2 = linalg.svd(X2)
    	a2 = A2[:r2, :]
        XP = restored_tensor(X,a1,a2)
        print linalg.norm(X-XP)/linalg.norm(X)
    filename = path+'_hooi'+ ext
    save_img(XP, filename)

def main():
    ratio = 0.2
    argc = len(sys.argv)
    if (argc <2):
        print("usage:")
        print("$ python %s filename ratio" % sys.argv[0])
        return
    filename = sys.argv[1]
    if (os.path.exists(filename) == False):
        print ("File is not found: %s" % filename)
        return
    if (argc >2):
        ratio = float(sys.argv[2])
    print "Ratio = " + str(ratio)
    print "Performing HOSVD"
    hosvd(filename,ratio)
    print "Performing HOOI"
    hooi(filename,ratio)

if __name__ == '__main__':
    main()
