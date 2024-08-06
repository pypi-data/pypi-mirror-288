def 打印(文字):
    print(文字)
def 如果(条件,成功时执行,失败时执行):
    if 条件==True:
        成功时执行()
    else:
        失败时执行()
def 消息窗口(文字,标题,确认按钮='确认'):
    import easygui
    easygui.msgbox(文字,标题,确认按钮)
def 切分字符串(变量或字符串,字符串=None):
    变量或字符串.split(字符串)
def 列表增加(列表,要增加的字符串):
    列表.append(要增加的字符串)
def 输入窗口(文字,标题):
    import easygui
    easygui.enterbox(文字,标题)
def 列表选择(列表=None, 信息=None, 标题=None):
    if not 列表:
        print('\033[91m错误\n\t错误概述：没有提供选项列表，您必须填写这个参数，否则无法运行。')
        print('\033[0m程序因错误退出。')
        import sys
        sys.exit(1)
    try:
        import easygui
        return easygui.choicebox(信息, 标题, 列表)
    except Exception as e:
        print(f'\033[91m错误\n\t错误概述：发生了一个不可预料的错误 {e}')
        print('\033[0m程序因错误退出')
        import sys
        sys.exit(1)
def 尝试(尝试内容,出错执行):
    if not 尝试内容:
        print('\033[91m错误\n\t错误概述：没有提供尝试内容，您必须填写这个参数，否则无法运行。')
        print('\033[0m程序因错误退出。')
        import sys
        sys.exit(1)
    if not 出错执行:
        print('\033[91m错误\n\t错误概述：没有提供出错执行，您必须填写这个参数，否则无法运行。')
        print('\033[0m程序因错误退出。')
        import sys
        sys.exit(1)
    else:
        try:
            尝试内容()
        except:
            出错执行
def 获取输入(提示语):
    input(提示语)