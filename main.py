import os,time
import cv2
#from KAmove import kick,soadd
farm1Sudo=['账号','密码']#公会1会长帐密
farm2Sudo=[,]#公会2会长帐密
realAccount=[,]#大号帐密


def connect():
    try:
        os.system('adb connect 127.0.0.1:5554')
    except:
        print('连接失败')

def click(x, y,name):
    print(name)
    print(x,y)
    os.system('adb -s '+name+' shell input tap %s %s' % (x, y))

def screenshot(name):
    path = os.path.abspath('.') + '\images.png'
    os.system('adb -s '+name+' shell screencap /data/screen.png')
    os.system('adb -s '+name+' pull /data/screen.png %s' % path)

def resize_img(img_path):
    '''
    关于自己截图的问题
截图的时候要把模拟器放全屏，如果显示器不是1080p的话自己截的图得改resize函数里面的1920，
例如1600*900的1920就改成1600，而且要把其他所有图都截一遍。或者加一个if把你自己截的图作为特例，
写一个新的resize把1920换成1600来单独处理你自己截的图，其他图片的还是用原来的resize
    '''
    img1 = cv2.imread(img_path, 0)
    img2 = cv2.imread('images.png', 0)
    height, width = img1.shape[:2]
    
    ratio = 1920 / img2.shape[1]
    size = (int(width/ratio), int(height/ratio))
    return cv2.resize(img1, size, interpolation = cv2.INTER_AREA)

def Image_to_position(image, m = 0):
    image_path = 'images/' + str(image) + '.png'
    screen = cv2.imread('images.png', 0)
    template = resize_img(image_path)
    methods = [cv2.TM_CCOEFF_NORMED, cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR_NORMED]
    image_x, image_y = template.shape[:2]
    result = cv2.matchTemplate(screen, template, methods[m])
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(image,max_val)
    if max_val > 0.7:
        global center
        center = (max_loc[0] + image_y / 2, max_loc[1] + image_x / 2)
        return center
    else:
        return False

def mainrun(nameList,images):
    #对模拟器逐一识别
    now=''
    
    for image in images:
        while True:
            screenshot(nameList[0])
            if Image_to_position(image, m = 0) != False:
                for name in nameList:
                    while True:
                        screenshot(name)
                        if Image_to_position(image, m = 0) != False:
                            print(image)
                            now=image
                            print(center)
                            if image=='timeadd':
                                os.system('adb -s '+name+' shell input swipe %s %s %s %s %s'%(center[0],center[1],center[0],center[1],8000))
                            else:
                                click(center[0], center[1],name)
                            #time.sleep(0.5)
                            break
                break
    
def mainrunQuick(nameList,images):
    #只识别第一个模拟器，后面的点一样的位置
    for image in images:
        while True:
            screenshot(nameList[0])
            if Image_to_position(image, m = 0) != False:
                for name in nameList:
                    if image=='timeadd':
                        os.system('adb -s '+name+' shell input swipe %s %s %s %s %s'%(center[0],center[1],center[0],center[1],8000))
                    else:
                        click(center[0], center[1],name)
                    #time.sleep(0.)
                break

def tohomepage(nameList):
    for i in range(0,6):
        screenshot(nameList[0])
        if Image_to_position('skip', m = 0) != False:
            for name in nameList:
                for i in range(0,6):
                    screenshot(name)
                    if Image_to_position('skip', m = 0) != False:
                        print('skip')
                        now='skip'
                        print(center)
                        
                        click(center[0], center[1],name)
                        time.sleep(0.5)
                        break
                    else:
                        click(640,360,name)
            break
        else:
            click(640,360,nameList[0])
            
   for i in range(0,4):#兰得索尔赛马
        screenshot(nameList[0])
        if Image_to_position('complete_start', m = 0) != False:
            mainrun(nameList,['choose_one','complete_start','skip_white'])
            time.sleep(3)
            for name in lines:
                click(1100,60,name)
        else:
            time.sleep(1)
def login(name,idset):
        while True:
            screenshot(name)
            if Image_to_position('ID', m = 0) != False:#普通登陆
                print('ID')
                print(center)
                click(center[0], center[1],name)
                os.system('adb -s '+name+' shell input text "'+idset[0]+'"')
                for image in ['password','login']:
                    while True:
                        screenshot(name)
                        if Image_to_position(image, m = 0) != False:
                            print(image)
                            print(center)
                            click(center[0], center[1],name)
                            if image=='password':
                                    os.system('adb -s '+name+' shell input text "'+idset[1]+'"')
                            break
                break
            elif Image_to_position('back_to_title_cn', m = 0) != False:#出现网络错误返回主页
                click(center[0], center[1],name)
                time.sleep(4)
                while True:
                    screenshot(name)
                    if Image_to_position('delete_white', m = 0) != False:
                        time.sleep(4)
                        print('delete_white')
                        print(center)
                        click(center[0], center[1],name)
                        time.sleep(4)
                        os.system('adb -s '+name+' shell input text "'+idset[0]+'"')
                        click(640, 330,name)
                        for _ in range(0,15):
                            os.system('adb -s '+name+' shell input keyevent 67')
                        time.sleep(3)
                        os.system('adb -s '+name+' shell input text "'+idset[1]+'"')
                        while True:
                            screenshot(name)
                            if Image_to_position('login', m = 0) != False:
                                print('login')
                                print(center)
                                click(center[0], center[1],name)
                                time.sleep(4)
                                break
                        break
                    else:
                        click(1200, 50,name)
                break
                        
            else:
                click(1200,50,name)

def getaccount(txtname):
    lines=[]
    with open(txtname, 'r') as f:
        lines=f.readlines()
        return lines

def kick(enumList):
    #公会踢人
    mainrun(enumList,['society'])
    time.sleep(3)
    mainrun(enumList,['memberinfo'])
    time.sleep(3)
    mainrun(enumList,['place','level','ok_blue'])
    time.sleep(3)
    mainrun(enumList,['take','fuck_off','ok_blue'])
    time.sleep(3)
    mainrun(enumList,['ok_white'])
    time.sleep(3)
    mainrun(enumList,['level1','place2','ok_blue'])
    time.sleep(3)
    mainrun(enumList,['homepage_red'])

def soadd(enumList,soName):
    #加公会
    mainrun(enumList,['society','sosetting','sosearch'])
    screenshot(enumList[0])
    while True:
        if Image_to_position('soname', m = 0) != False:
            print(center)
            click(center[0], center[1],enumList[0])
            time.sleep(5)
            os.system('adb -s '+enumList[0]+' shell input text "'+soName+'"')
            time.sleep(2 )
            #k = PyKeyboard()
            mainrun(enumList,['ensurecn'])
            break
    time.sleep(3)
    #click(enumList[0])
    mainrun(enumList,['search'])
    time.sleep(4)
    mainrun(enumList,['farmicon','farmjoin'])
    time.sleep(3)
    mainrun(enumList,['ok_blue'])
    time.sleep(3)
    mainrun(enumList,['ok_blue'])

if __name__ == '__main__':
    
    accountList=getaccount('accountlist1.txt')#获取账号列表1
    
    connect()

    result = os.popen('adb devices')  
    res = result.read()
    lines=res.splitlines()[1:]
    
    for i in range(0,len(lines)):
        lines[i]=lines[i].split('\t')[0]
    lines=lines[0:-1]
    print(lines)

    # for step in range(0,10):
    #     for i in range(0,len(lines)):
    #         login(lines[i],[accountList[i+step*4].split(' ')[0],accountList[i+step*4].split(' ')[1][0:-1]])
    #         print(accountList[i+step*4].split(' ')[0])
    #     time.sleep(5)
    #     tohomepage(lines)
    #     mainrunQuick(lines,['close_white'])

    #     mainrunQuick(lines,['mainpage','backtotitle','ok_blue'])
    #     time.sleep(3)

    '''
    共28个号，4开为例


    改多开方式就改range(0,n)中的n，例如改成双开就是改成range(0,10),10*2=20,20是一个公会小号的数量
    '''
    for step in range(0,7):

        '''
        依次登陆4个号
        '''
        
        for i in range(0,len(lines)):
            login(lines[i],[accountList[i+step*len(lines)].split(' ')[0],accountList[i+step*len(lines)].split(' ')[1][0:-1]])
            print(accountList[i+step*len(lines)].split(' ')[0])
        time.sleep(5)
        tohomepage(lines)
        time.sleep(5)
        mainrunQuick(lines,['close_white'])
        time.sleep(4)

        #买六次体力，如果体力满了就会一直卡在这儿，所以第一次用的时候提前手动把体力全刷完
        for _ in range(0,6):
            mainrunQuick(lines,['add_blue','ok_blue','ok_white'])
        time.sleep(6)
        mainrunQuick(lines,['explor','masterbatch'])
        time.sleep(3)
        mainrunQuick(lines,['3-1','timeadd','run_cn','ok_blue'])
        time.sleep(2)
        mainrunQuick(lines,['skip_cn','ok_white'])

        for name in lines:
            click(1100,60,name)
        mainrun(lines,['cancel_white'])
        time.sleep(5)
        mainrunQuick(lines,['explor_blue'])
        '''
        地下城战斗
        '''
        time.sleep(5)
        mainrunQuick(lines,['explor_blue','underground','normalUD','ok_blue'])
        time.sleep(8)
        mainrunQuick(lines,['floor1'])
        time.sleep(2)
        mainrunQuick(lines,['challenge_blue'])
        time.sleep(3)
        #mainrunQuick(lines,['u1','pico','kkl','cat','getassist','assist','battlestart','ok_blue'])
        mainrunQuick(lines,['getassist','assist','battlestart','ok_blue'])
        time.sleep(5)
        mainrunQuick(lines,['menu_white','giveup_white','giveup_blue'])
        time.sleep(5)
        mainrunQuick(lines,['withdraw','ok_blue'])
        time.sleep(5)
        '''
        回登陆页，开始下一次iteration

        '''
        mainrunQuick(lines,['mainpage','backtotitle','ok_blue'])
        time.sleep(3)

    
    '''
    踢出换工会上支援
    '''
    login(lines[0],farm1Sudo)
    login(lines[1],realAccount)
    tohomepage([lines[0]])
    tohomepage([lines[1]])
    time.sleep(3)
    mainrun([lines[0],lines[1]],['close_white'])
    time.sleep(2)
    kick([lines[0]])
    time.sleep(2)
    soadd([lines[1]],名称)#公会2名称，注意要英文加数字，不能有中文
    time.sleep(4)
    mainrun([lines[1]],['setassist','addselect','myassist','set','ok_blue'])
    time.sleep(3)
    mainrun([lines[1]],['homepage_red'])
    time.sleep(3)
    mainrun([lines[0],lines[1]],['mainpage','backtotitle','ok_blue'])



    accountList=getaccount('accountlist2.txt')#获取账号列表2

    '''
    共12个号，4开为例
    '''    
    for step in range(0,3):

        '''
        依次登陆4个号
        '''
        
        for i in range(0,len(lines)):
            login(lines[i],[accountList[i+step*len(lines)].split(' ')[0],accountList[i+step*len(lines)].split(' ')[1][0:-1]])
            print(accountList[i+step*len(lines)].split(' ')[0])
        time.sleep(5)
        tohomepage(lines)
        time.sleep(5)
        mainrunQuick(lines,['close_white'])
        time.sleep(4)

        #买六次体力，如果体力满了就会一直卡在这儿，所以第一次用的时候提前手动把体力全刷完
        for _ in range(0,6):
            mainrunQuick(lines,['add_blue','ok_blue','ok_white'])
        time.sleep(6)
        mainrunQuick(lines,['explor','masterbatch'])
        time.sleep(3)
        mainrunQuick(lines,['3-1','timeadd','run_cn','ok_blue'])
        time.sleep(2)
        mainrunQuick(lines,['skip_cn','ok_white'])

        for name in lines:
            click(1100,60,name)
        mainrun(lines,['cancel_white'])
        time.sleep(5)
        mainrunQuick(lines,['explor_blue'])
        '''
        地下城战斗
        '''
        time.sleep(5)
        mainrunQuick(lines,['explor_blue','underground','normalUD','ok_blue'])
        time.sleep(8)
        mainrunQuick(lines,['floor1'])
        time.sleep(2)
        mainrunQuick(lines,['challenge_blue'])
        time.sleep(3)
        #mainrunQuick(lines,['u1','pico','kkl','cat','getassist','assist','battlestart','ok_blue'])
        mainrunQuick(lines,['getassist','assist','battlestart','ok_blue'])
        time.sleep(5)
        mainrunQuick(lines,['menu_white','giveup_white','giveup_blue'])
        time.sleep(5)
        mainrunQuick(lines,['withdraw','ok_blue'])
        time.sleep(5)
        '''
        回登陆页，开始下一次iteration

        '''
        mainrunQuick(lines,['mainpage','backtotitle','ok_blue'])
        time.sleep(3)

    
    '''
    踢出换工会上支援
    '''
    login(lines[0],farm2Sudo)
    login(lines[1],realAccount)
    tohomepage([lines[0]])
    tohomepage([lines[1]])
    time.sleep(2)
    mainrun([lines[0],lines[1]],['close_white'])
    time.sleep(2)
    kick([lines[0]])
    time.sleep(2)
    soadd([lines[1]],名称)#公会1名称，注意要英文加数字，不能有中文
    time.sleep(4)
    mainrun([lines[1]],['setassist','addselect','myassist','set','ok_blue'])
    time.sleep(3)
    mainrun([lines[1]],['homepage_red'])
    time.sleep(3)
    mainrun([lines[0],lines[1]],['mainpage','backtotitle','ok_blue'])


    #退出程序
    os.system('adb kill-server')
