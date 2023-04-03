import socket
import time
import tkinter as tk
import threading
import datetime
from tkinter import Tk
import tkinter.font as tkFont
from tkinter import messagebox
import PyInstaller
from tkinter import *


HOST = '192.168.0.61'
PORT = 9900
app=0
#input_msg = tk.StringVar()

sock = socket.socket()#socket.AF_INET, socket.SOCK_STREAM
sock.connect_ex((HOST,PORT))

date = datetime.datetime.now()

msg_call= ""



db_load=1

user_name= []

data1=None # 로딩 프레임

class log_main(Tk):

    recv_msg = ""
    car_traffic = None
    home_coming = None
    map = None
    logout=None


    def __init__(self):
        Tk.__init__(self)
        self.geometry("400x500")
        self._frame = None
        self.switch_frame(StartPage)

    def msg_handler(self, msg):#동적 생성 ########################################메세지 ############################
        global db_load
        global user_name
        print(f"받은 msg는 {msg}")
        print(len(msg),"##########")
        if "/명소" in msg:

            self.next_frame(map_frame)
            #time.sleep(0.2)
            #print(type(self._frame),"셀프프프프프프레레레임")
            self._frame.maps()

        elif "/로딩종료" in msg:

            asd= loading_start()
            time.sleep(0.2)
            asd.loading_close()

        elif "/검색" in msg:

            asd = loading_start()
            time.sleep(0.2)
            asd.loading_close()
        
        elif "/없는아이디" in msg:
            messagebox.showerror("오류","아이디를 확인해주세요")

        elif "/비번틀림" in msg:
            messagebox.showerror("오류", "비밀번호를 확인해주세요")


        elif "/로그인 성공" in msg:
            #self.switch_frame(log_go)
            messagebox.showerror("로그인성공",f"{user_name}환영합니다!!")
            self.next_frame(main_frame)


        elif "/가입완료" in msg:
            messagebox.showerror("회원가입완료","회원가입성공!")
            self.switch_frame(StartPage)

        elif "/가입실패" in msg:
            messagebox.showerror("가입실패","입력정보를다시확인하세요.")

        elif "/클릭명소" in msg:
            self._frame.serch_list()

        elif "/실행중" in msg:
            messagebox.showerror("오류","이미 접속중인 아이디입니다.")

        else:
            pass


    def switch_frame(self, frame_class):

        self.geometry("400x500")
        new_frame = frame_class(self)

        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        #self._frame.pack(anchor="c",ipadx=200,pady=200)

    def next_frame(self, frame_class):
        self.geometry("1200x700")
        self.car_traffic = tk.PhotoImage(file="car_frame.png")
        self.home_coming = tk.PhotoImage(file="main_home.png")
        self.map = tk.PhotoImage(file="map.png")
        self.logout=tk.PhotoImage(file="logout.png")


        home_button = tk.Button(self, bg="paleturquoise", image=self.home_coming, width=150, height=80, bd=0,
                                command=lambda: self.next_frame(main_frame))
        home_button.bind("<Button-1>",self.chat_massge1)
        home_button.place(x=50, y=50)


        traffic_button = tk.Button(self, bg="paleturquoise", image=self.car_traffic, width=150, height=80, bd=0,
                                   command=lambda: self.next_frame(daejeon_traffic))
        traffic_button.place(x=50, y=150)

        temperature_button = tk.Button(self, bg="paleturquoise", image=self.map, width=150, height=80, bd=0,
                                       command=lambda: self.next_frame(map_frame))
        temperature_button.place(x=50, y=250)

        logout_button = tk.Button(self, bg="paleturquoise", image=self.logout, width=150, height=80, bd=0,
                                       command=lambda: self.switch_frame(StartPage))
        logout_button.bind("<Button-1>",self.log_out)
        logout_button.place(x=50, y=350)

        new_frame = frame_class(self)

        # self.next_frame_frame(test)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame

    def log_out(self,e):
        global sock
        sock.send("/나가기".encode())

    def chat_massge1(self,e): # 채팅을 쳤을 때 서버에 보내는 함수

        global sock
        #data = str(date.year) + "-" + str(date.month) + "-" + str(date.day)
        name = f"/채팅인"
        # sock.send(bytes(name, "utf-8"))
        #print(name)
        sock.send(name.encode())

# class main_frame(tk.Frame): # 로그인 후 프레임
#
#     def __init__(self,master):
#         tk.Frame.__init__(self,master,bg='white',width=1000,height=600)
#         tk.Frame.grid(self, row=0, column=0, sticky="nsew")
#         tk.Frame.place(self, x=90, y=50)

class StartPage(tk.Frame): # 첫화면 프레임
    back =None
    def __init__(self, master):
        print("starPageMaster",master)
        self.user_id = tk.StringVar()
        self.user_pw = tk.StringVar()
        tk.Frame.__init__(self, master,bg="white",width=320, height=420)

        tk.Frame.place(self,x=38,y=30)
        tk.Label(self,text="user ID :",width=10,bg="white").place(x=50,y=160)
        tk.Label(self,text="user PW :",width=10,bg="white").place(x=50,y=210)
        #tk.Label(self,text=msg_call,width=30,bg="white").place(x=60,y=110)
        #msg = sock.recv(1024)
        #tk.Label(self,text=msg.decode("utf-8"),width=10).place(x=10,y=10)

        id=tk.Entry(self, textvariable=self.user_id, width=20)
        id.place(x=130, y=160)
        pw=tk.Entry(self, show="*", textvariable=self.user_pw, width=20)
        pw.place(x=130, y=210)
        
        log_button=tk.Button(self, width=10, text="login",bg="paleturquoise")
        log_button.bind("<Button-1>",self.log_message)
        log_button.place(x=190, y=270)

        tk.Button(self, width=10, text="회원가입",
                               command=lambda: master.switch_frame(create_frame),bg="paleturquoise").place(x=100, y=270)


        if "ID를" in msg_call:
            messagebox.showerror("오류", "잘못입력하셨습니다.")

        #print(sock.recv(1024))
    def log_message(self,e):
        global user_name
        global sock
        user_id = self.user_id.get()
        user_pw = self.user_pw.get()
        name = f"/로그인,{user_id},{user_pw}"
        user_name=user_id
        #print(name)
        sock.send(name.encode())
        asd= loading_start()
        asd.data_loading()

class log_go(tk.Frame): #아이디 비번이 맞는 지 확인
    # Tk지움
    smile= None
    sad = None
    back=None
    login=None
    def __init__(self,master):
        tk.Frame.__init__(self, master, bg="white", width=320, height=420)

        tk.Frame.place(self, x=38, y=30)
        data = str(date.year) + "-" + str(date.month) + "-" + str(date.day)

        tk.Label(self,text=data,width=15, bg="white").place(x=31, y=30)

        self.back = tk.PhotoImage(file="back.png")

        tk.Button(self, width=60, image=self.back,
                  command=lambda: master.switch_frame(StartPage), bg="white",bd=0).place(x=100, y=270)

        self.smile=tk.PhotoImage(file="smile_face.png")
        self.sad = tk.PhotoImage(file="sad_face.png")
        happy = tk.Label(self, width=100, image=self.smile,bg="white")
        sad = tk.Label(self, width=100, image=self.sad,bg="white")

        fontExample = tkFont.Font(family="휴먼둥근헤드라인", size=14, weight="bold", slant="italic")


        log_in = tk.Label(self,bg="white",font=fontExample,fg="darkCyan",text=f"{user_name}님,반갑습니다~")
        log_out= tk.Label(self,bg="white",font=fontExample,fg="darkCyan",text="로그인 정보를 \n 다시 확인해주세요 ㅠㅠ")

        if "성공" in msg_call:
            happy.place(x=100,y=100)
            log_in.place(x=40,y=200)
            #self.login = tk.PhotoImage(file="login.png")
            #image = self.login,
            tk.Button(self, width=60, text="로그인", bg="white",bd=0,
                      command=lambda: master.next_frame(main_frame)).place(x=200, y=270)


        else:
            sad.place(x=100, y=100)
            log_out.place(x=40,y=200)
           # tk.Label(self,text=msg_call,width=30, bg="white").place(x=31, y=80)


    def log_message(self, e):
        global sock
        name = "/뉴스"
        sock.send(name.encode())


class create_frame(tk.Frame): #가입 프레임
    #Tk지움

    def __init__(self,master):
        self.mem_id=tk.StringVar()
        self.mem_pw=tk.StringVar()
        self.name=tk.StringVar()
        self.age=tk.StringVar()
        self.sex=tk.StringVar()
        self.addr=tk.StringVar()
        self.tel=tk.StringVar()

        tk.Frame.__init__(self,master,bg="white",width=320, height=420)
        tk.Frame.place(self, x=38, y=30)

        cancer_button=tk.Button(self, text="취소",
                  command=lambda: master.switch_frame(StartPage),width=10,bg="paleturquoise")
        cancer_button.place(x=130, y=380)


        tk.Label(self, text="user ID :", width=15, bg="white").place(x=31, y=30)
        tk.Label(self, text="user PW :", width=15, bg="white").place(x=29, y=65)
        tk.Label(self, text="user name :", width=15, bg="white").place(x=23, y=95)
        tk.Label(self, text="user age :", width=15, bg="white").place(x=28, y=125)
        tk.Label(self, text=" 성별 :", width=15, bg="white").place(x=36, y=155)
        tk.Label(self, text=" 주소 :", width=15, bg="white").place(x=35, y=185)
        tk.Label(self, text="전화번호 :", width=15, bg="white").place(x=27, y=215)
        #tk.C
        id=tk.Entry(self, width=20, bg="white",textvariable=self.mem_id)
        #id.insert("숫자만 입력 금지")
        id.place(x=120,y=30)

        tk.Entry(self, width=20, bg="white",textvariable=self.mem_pw).place(x=120, y=60)
        tk.Entry(self, width=20, bg="white",textvariable=self.name).place(x=120, y=90)
        tk.Entry(self, width=20, bg="white",textvariable=self.age).place(x=120, y=120)
        tk.Entry(self, width=20, bg="white",textvariable=self.sex).place(x=120, y=150)
        tk.Entry(self, width=20, bg="white",textvariable=self.addr).place(x=120, y=180)
        tk.Entry(self, width=20, bg="white",textvariable=self.tel).place(x=120, y=210)

        creat_button = tk.Button(self, text="가입",
                                 command=lambda: master.switch_frame(StartPage), width=10, bg="paleturquoise")
        creat_button.bind("<Button-1>", self.insert_message)
        creat_button.place(x=230, y=380)

    def insert_message(self, e): # 가입 메세지 보내기 함수
        global sock
        data = str(date.year) + "-" + str(date.month) + "-" + str(date.day)
        mem_id=self.mem_id.get()
        mem_pw=self.mem_pw.get()
        name=self.name.get()
        age=self.age.get()
        sex=self.sex.get()
        addr=self.addr.get()
        tel=self.tel.get()
        name = f"/가입,{mem_id},{mem_pw},{name},{age},{sex},{addr},{tel},{data}"
        # sock.send(bytes(name, "utf-8"))
        #print(name)
        sock.send(name.encode())


def recv_message(): # 메세지 받는 함수
    global sock
    global default_msg
    global msg_call
    global app
    while True:
        msg = sock.recv(10485760)
        msg_call = msg.decode("utf-8")

        if app != 0:
            app.msg_handler(msg_call)

        print("rcv done", datetime.datetime.now())


receive_thread = threading.Thread(target=recv_message)
receive_thread.daemon = True
receive_thread.start()


class main_frame(tk.Frame): # 로그인 후 프레임
    main =None
    def __init__(self,master):


        self.chat_Get = tk.StringVar()

        tk.Frame.__init__(self,master,bg='white',width=900,height=600,relief="solid",bd=1)
        tk.Frame.place(self, x=250, y=50)

        fontExample = tkFont.Font(family="Arial", size=14, weight="bold", slant="italic")
        fontExample1 = tkFont.Font(family="Arial", size=19, weight="bold", slant="italic")

        fontExample2 = tkFont.Font(family="Arial", size=30, weight="bold", slant="italic")

        #self.main = tk.PhotoImage(file="main_icon.png")
        #main_title = Label(self,image=self.main,font=fontExample2,width=200,height=300,bg="white",bd=0)


        chat_bar = tk.Entry(self,bg='white',width=50,bd=2,font=fontExample1,textvariable=self.chat_Get)


        self.chat_send = tk.PhotoImage(file="chat_send1.png")
        chat_button = tk.Button(self,bg='white',width=70,height=60,bd=0,font=fontExample1,image=self.chat_send,
                                command=lambda: master.next_frame(main_frame))




        chat_button.bind("<Button-1>",self.chat_massge)

        chat_frame = tk.Frame(self, bg="white", width=840, height=300, relief="solid", bd=1)


        chat_list = tk.Listbox(chat_frame,bg="white",bd=1,width=75,height=11,font=fontExample,relief="flat",
                               selectborderwidth=1)
        #chat_scrollbar = tk.Scrollbar(chat_frame, orient="vertical")
        #chat_scrollbar.config(command=chat_list.yview)

        #chat_list.config(yscrollcommand=chat_scrollbar.set)

        self.insert_listbox(chat_list)

        ################메인 프레임
        chat_bar.place(x=20, y=190)
        chat_button.place(x=760, y=170)
        #main_title.place(x=250,y=30)#############################

        ##########################채팅 프레임
        chat_frame.place(x=20, y=250)
        chat_list.place(x=0,y=0)
        #chat_scrollbar.pack(side="right", fill="y")



    def insert_listbox(self,name):#한줄 채팅리스트 ###################################################################
        #if "채팅고" in msg_call:
            try:

                if "채팅고" in msg_call:
                    #a = 1
                    msg = msg_call[4:]
                    msg = msg[1:-1]
                    msg.replace("\n", "")
                    msg.replace("","")
                    msg = msg.split(')')
                    for i in msg:
                        name.insert(1, i[2:-1])
                        #a+=1
                else:
                    pass
            except Exception as e:
                print("list_view함수", e)

    def chat_massge(self,e): # 채팅을 쳤을 때 서버에 보내는 함수

        global sock
        #data = str(date.year) + "-" + str(date.month) + "-" + str(date.day)
        try:
            chat_send = self.chat_Get.get()
            if len(chat_send) > 0:
                name = f"/채팅인,{chat_send}"
            # sock.send(bytes(name, "utf-8"))
            #print(name)
                sock.send(name.encode())
                
            elif "/" in chat_send:
                messagebox.showerror("오류","/는 넣지마세요")
            else:
                messagebox.showerror("오류","한글자 이상 입력하세요")
                #pass
        except Exception as e:
            print(e,"chat_massge")



class daejeon_traffic(tk.Frame):  # 교통 정보 프레임

    serch = None
    west = []
    ser = []
    number=[]
    list_box=None
    start =None
    end=None
    time=None
    speed=None
    updown=None

    def __init__(self, master):
        self.find_name= tk.StringVar()
        tk.Frame.__init__(self, master, bg='white', width=900, height=600, relief="solid", bd=1)
        tk.Frame.place(self, x=250, y=50)

        fontExample = tkFont.Font(family="Arial", size=19, weight="bold", slant="italic")
        tk.Entry(self, bg="white", width=40, font=fontExample,textvariable=self.find_name).place(x=75, y=50)

        self.serch = tk.PhotoImage(file="serch.png")
        serch = tk.Button(self, bg="paleturquoise", image=self.serch, width=70, height=35, command=self.daejeon_frame)
        serch.bind("<Button-1>", self.find_massage)
        serch.place(x=670, y=45)
        self.daejeon_frame()


    def daejeon_frame(self):
        # self.loading_start()
        # self.data_loading()
        # self.loading_end()

        trafic_show = tk.Frame(self, bg="white", width=800, height=450, relief="solid", bd=0)
        trafic_show.place(x=50, y=120)

        self.list_box = tk.Listbox(trafic_show, bg="white", width=30, height=20,selectmode="extended")
        #self.ser.append(trafic_load.curselection())
        self.list_box.place(x=50, y=20)
        # print(self.ser)

        trafic_button = tk.Button(trafic_show, bg="paleturquoise", text="검색",
                                  width=10)  # command=str(self.list_select(trafic_load)) )
        trafic_button.bind("<Button-1>", self.list_select)

        trafic_button.place(x=300, y=20)

        ###############################################################################################################
        self.list_view(self.list_box)
        ################################################0125######################
        self.working = tk.PhotoImage(file="aktwlq.png")
        shopping_button = tk.Button(trafic_show, bg="paleturquoise", image=self.working,
                                    width=60, height=25)  # command=str(self.list_select(trafic_load)) )
        shopping_button.bind("<Button-1>", self.shopping_frame)
        shopping_button.place(x=680, y=415)

    def shopping_frame(self, e):  #######################0125
        shopping_show = tk.Frame(self, bg="white", width=898, height=598, relief="solid", bd=0)
        shopping_show.place(x=0, y=0)


    def list_select(self,e):
        try:
            self.ser = []
            a= self.list_box.curselection()
            self.ser.append(str(self.list_box.get(a)).split())
            print(self.ser[0][0])
            self.insert_message()
            self.traffic_data()
            self.num_get()

        except Exception as e:
            print("list_select함수",e)
    
    def insert_message(self):
        global sock
        name = f"/넘버,{self.ser[0][0]}"
        # sock.send(bytes(name, "utf-8"))
        #print(name)
        sock.send(name.encode())


    def list_view(self,name): #
        try:
            if "/검색" in msg_call:
                a=1
                msg = msg_call[4:]
                msg.replace("\n","")
                msg = msg.split(')')

                for i in msg:
                    name.insert(a, i)
                    a += 1
            else:
                pass
        except Exception as e:
            print("list_view함수",e)


    def find_massage(self,e): #클라이언트 검색창 글씨를 서버에 보내는 함수
        global db_load
        global sock
        find_name = self.find_name.get()
        name = f"/교통,{find_name}"
        # sock.send(bytes(name, "utf-8"))
        #print(name)
        sock.send(name.encode())
        #asd=loading_start()
        #asd.data_loading()
        #time.sleep(0.5)
        #sock.send("/로딩".encode())
        # self.loading_start()
        # self.loading_end()
        # self.data_loading()
        #asd = log_main()
        #asd.next_frame(self.daejeon_frame)
        #self.master.switch_frame(self.daejeon_frame)
        #self.daejeon_frame()
       #db_load=1

    def traffic_data(self):

        data = tk.Frame(self,bg="white",width=450,height=340,relief="solid",bd=0)
        data.place(x=350, y=200)

        fontExample = tkFont.Font(family="휴먼둥근헤드라인", size=15, weight="bold", slant="italic")
        tk.Label(data, text="    출발지 :", width=10, bg="white", font=fontExample).place(x=5, y=30)
        tk.Label(data, text="    도착지 :", width=10, bg="white", font=fontExample).place(x=5, y=80)
        tk.Label(data, text=" 평균속도 :", width=10, bg="white", font=fontExample).place(x=1, y=130)
        tk.Label(data, text=" 교통정보 :", width=10, bg="white", font=fontExample).place(x=1, y=180)
        tk.Label(data, text=" 이동방향 :", width=10, bg="white", font=fontExample).place(x=1, y=230)

        self.start = tk.Text(data, width=15, height=1, bg="white", font=fontExample, bd=0)
        self.end = tk.Text(data, width=15, height=1, bg="white", font=fontExample, bd=0)
        self.time = tk.Text(data, width=15, height=1, bg="white", font=fontExample, bd=0)
        self.speed = tk.Text(data, width=15, height=1, bg="white", font=fontExample, bd=0)
        self.updown = tk.Text(data, width=15, height=1, bg="white", font=fontExample, bd=0)

        self.num_get()

        self.start.configure(state="disabled")
        self.end.configure(state="disabled")
        self.time.configure(state="disabled")
        self.speed.configure(state="disabled")
        self.updown.configure(state="disabled")
        self.start.place(x=170, y=30)
        self.end.place(x=170, y=80)
        self.time.place(x=170, y=180)
        self.speed.place(x=170, y=130)
        self.updown.place(x=170, y=230)
        #self.num_get()


    def num_get(self): #
        try:
            if "/넘버" in msg_call:
                msg = msg_call[4:]
                msg.replace("\n","")
                print(msg,"스플릿하기전")
                msg = msg.split()
                print(msg,"스플릿 한후")

                self.start.insert(1.0, msg[0][1:-1])
                self.end.insert(1.0, msg[1][1:-1])
                self.speed.insert(1.0, msg[2][1:-1])


                if "1" == msg[3][1:-1]:
                    self.time.insert(1.0,"소통원활")

                elif "2" == msg[3][1:-1]:
                    self.time.insert(1.0,"지체")

                elif "3" == msg[3][1:-1]:
                    self.time.insert(1.0,"정체")

                else:
                    self.time.insert(1.0, "정보없음")

                if "1" == msg[4]:
                    self.updown.insert(1.0, "상행선")
                else:
                    self.updown.insert(1.0, "하행선")
                #self.start.insert(1.0,msg[])
            else:
                pass
        except Exception as e:
            print("num_get함수",e)

class loading_start:

    def data_loading(self):  #로딩 프레임 잘됨 아주 굿!!!!!!
        # 정보 프레임
        global db_load
        global data1
        try:
            data1 = tk.Frame( bg="white", width=900,height=600, relief="solid", bd=0)
            data1.place(x=150, y=100)

            data1.canvas = Canvas(data1, bg="white")
            data1.canvas.pack(expand=True, fill=BOTH)

            data1.my_image_number = 0

            data1.myimages = [PhotoImage(file='speed50.gif', format='gif -index %i' % (i)) for i in range(4)]

            data1.dragon = data1.canvas.create_image(200, 140, image=data1.myimages[0], tags="dragon")

            #data.canvas.create_text(320, 400, font="Times 15 italic bold", text="Load GIF Image")


            while db_load:
                # canvas에서 self.dragon 이미지를 읽어오고 gif의 다음 이미지로 교체함
                data1.canvas.itemconfig(data1.dragon, image=data1.myimages[data1.my_image_number % len(data1.myimages)])
                time.sleep(0.1)
                data1.my_image_number += 1
                data1.after(33)
                data1.update()

        except:
            print("????????????????????????????????????")

    def loading_close(self):
        #global msg_call
        global db_load
        try:
        #print(msg_call,111111111111111111111111111111111111111)
        #if "/로딩종료" in msg_call:
            db_load=0
            data1.destroy()
            #print("111111111111111112222222222222222222222222222222")
            db_load=1
        except:
            pass

class map_frame(tk.Frame):  # 근처 명소 프레임
    map1 = None
    serch_get=[]
    data = None

    def __init__(self, master):

        #print("map_frame.init master",master,type(master))
        #self.data_loading()
        self.map_name= tk.StringVar()

        tk.Frame.__init__(self, master, bg='white', width=900, height=600, relief="solid", bd=1)
        tk.Frame.place(self, x=250, y=50)

        fontExample = tkFont.Font(family="Arial", size=14, weight="bold", slant="italic")
        map_bar = tk.Entry(self, bg='white', width=40, bd=2, font=fontExample,textvariable=self.map_name)

        #map_bar.bind("<Button-1>",self.map_bar_click)

        map_bar.place(x=10,y=30)

        self.map1 = tk.PhotoImage(file="audth.png")

        map_button = tk.Button(self, bg='white', width=70, height=60, bd=0,  image=self.map1)
                               #command=lambda: master.next_frame(map_frame))
        map_button.bind("<Button-1>",self.map_massage)


        map_button.place(x=480,y=10)

    def map_massage(self, e):  # 클라이언트 검색창 글씨를 서버에 보내는 함수
        global sock
        find_name = self.map_name.get()
        if len(find_name) > 0:
            name = f"/명소,{find_name}"
            # sock.send(bytes(name, "utf-8"))
            # print(name)
            sock.send(name.encode())
            asd= loading_start()
            asd.data_loading()
        else:
            messagebox.showerror("에러","한글자 이상 입력하세요.")

    def no_list_box(self):
        print("최다 검색어 뜨기")


    def maps(self):# 장소 근처 명소 확인 맵

        try:
            a= 10
            y=10
            c=0
            if "/명소" in msg_call:
                msg = msg_call[5:-1]
                msg = msg.replace("\\n","\n")
                msg = msg.replace(" 중"," 중\n")
                msg=msg.split(", ")

                for i in msg:
                    if a <= 700:

                        asd = tk.Frame(self, bg="white", width=190, height=150, relief="solid", bd=0)
                        asd.place(x=a, y=80)
                        tk.Label(asd,width=25,bd=0,text=msg[c],bg="white").place(x=10,y=10)
                        c+=1
                        a+=200

                    elif y <= 700:
                        asd = tk.Frame(self, bg="white", width=190, height=150, relief="solid", bd=0)
                        asd.place(x=y, y=300)
                        tk.Label(asd, width=25, bd=0, text=msg[c], bg="white").place(x=10, y=10)
                        c+=1
                        y += 200

                # self.configure(width=900, height=600)

        except Exception as e:
            print("maps",e)


    def map_bar_click(self,e): # 검색창 클릭시 서버에 명소클릭 보내는 함수
        global sock
        sock.send("/클릭명소".encode())
        #map_bar.place(x=10, y=30)


    def serch_list(self): # 최근 검색어 리스트 박스안에 넣기
        if "/클릭명소" in msg_call:

            msg = msg_call[8:-3]

            msg = msg.replace("'", "")

            msg = msg.split(") ")
            a=0
            b=1
            asd = tk.Listbox(self, height=5, width=10, bg="white", bd=1)
            asd.place(x=10, y=60)

            scroll = tk.Scrollbar(self,orient="vertical" ,command=asd.yview)
            scroll.pack(side="right", fill="y")

            asd.config(yscrollcommand=scroll.set)

            for i in range(len(msg)):
                asd.insert(END,msg[a])
                a+=1
                #b+=1


def start():
    if __name__ == "__main__":
        global app
        app =log_main()
        # app.geometry("400x500")
        app.resizable(False,False)
        app.configure(bg="paleturquoise")
        app.mainloop()
start()







