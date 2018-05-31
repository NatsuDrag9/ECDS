import numpy as np
from PIL import Image
lst_string=[]
lst_out=[]
lst_numpy_arrays=[]
lst_tst_string=[]
lst_tst_out=[]
test_data=[]
training_data=[]
with open("dataset.txt","r") as f:
    for line in f:
        process_lst=line.split(",")
        if(process_lst[2]=="Training\n" or process_lst[2]=="PublicTest\n" or process_lst[2]=="PrivateTest\n"):
            lst_string.append(process_lst[1])
            lst_out.append(process_lst[0])
            
        if(process_lst[2]=="PublicTest\n" or process_lst[2]=="PrivateTest\n"):
            lst_tst_string.append(process_lst[1])
            lst_tst_out.append(process_lst[0])
            break
xy=lst_string[100].split(" ")
xyz=[int(x) for x in xy]
np_array=np.asarray(xyz).reshape(48,48)
print(np_array.shape)
img=Image.fromarray(np_array,"L")
img.show()
