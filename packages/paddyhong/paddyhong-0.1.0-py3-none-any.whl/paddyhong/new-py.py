print('新的py文件的名字:')
filename=input()
if '.py' in filename:
    file=open(filename,'w')
    file.write('from paddy import *\n\"\"\"_________________________________________________________________________________________________\"\"\"')
    print('成功新建了一个py文件')
    input('按下【回车】键以退出')
else:
    file=open(filename+'.py','w')
    file.write('from paddy import *\n\"\"\"_________________________________________________________________________________________________\"\"\"')
    print('成功新建了一个py文件')
    input('按下【回车】键以退出')