import datetime
import socketserver
import threading
import time
import dbtest
from selenium.webdriver.common.by import By
from  selenium import webdriver
import requests,xmltodict, json
import queue

HOST = '192.168.0.61' # 서버의 ip를 열음. (이 서버의 ip로 클라이언트가 접속을 해야 한다), 그전에 ping을 먼저 확인하도록.
PORT = 9900     		 # 포트번호 (같아야 함)
lock = threading.Lock()  # syncronized 동기화 진행하는 스레드 생성
chatTime=datetime.datetime.now()

asd=dbtest
asd=asd.member()

serch = dbtest
serch = serch.lately_serch()

nod = [] #대전 교통정보 담은 리스트 1. 출발지 2. 도착지 3. 평균속도 4. 교통정보 5. 상행 하행
tag_name = []
class_name=[]

user_name=""

class menu_data(By): #네이버 검색어 + 명소 크롤링

    def mail_post(self,name):
        option = webdriver.ChromeOptions()
        option.add_argument("--headless")

        driver = webdriver.Chrome( options=option)
        driver.get(f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query={name} + 명소")

        element = driver.find_elements(self.CLASS_NAME,'ouxiq.icT4K')
        element1 = driver.find_elements(self.CSS_SELECTOR,"lazyload-wrapper ")
        sad=[]
        for i in element:
            sad.append(i.text)

        driver.close()
        return sad



class daejeonTraffic: # api 크롤링 클래스

    def daejeon(self):
        API_key = "C%2FJiO78BfqlxUM3%2FjoGW7Faix6jNaT53JEBdIQp%2F8KFO7qP3aU5s9XDp9LJ3Oo8fXhADyK13yodJzheq9xcSvg%3D%3D"

        url = "http://openapitraffic.daejeon.go.kr/traffic/rest/getTrafficInfoAll.do?serviceKey={API}&numOfRows=9000&pageNo=1".format(
            API=API_key)
        #date = datetime.datetime.now()
        #data = str(date.hour) + "시" + str(date.minute)+"분"+str(date.second)+"초"
        content = requests.get(url).content
        dict = xmltodict.parse(content)

        jsonString = json.dumps(dict['response']['body']['TRAFFIC-LIST']['TRAFFIC'], ensure_ascii=False)
        jsonObj = json.loads(jsonString)

        for i in range(len(jsonObj)):
            # jin = jsonObj[i]['startNodeName'], jsonObj[i]['endNodeName'], jsonObj[i]['speed'], jsonObj[i]['congestion'],
            # jsonObj[i]['udType']
            asd.daejeon_insert(jsonObj[i]['startNodeName'], jsonObj[i]['endNodeName'], jsonObj[i]['speed'], jsonObj[i]['congestion'],
            jsonObj[i]['udType'])


    def daejeon_ser(self):
        API_key = "C%2FJiO78BfqlxUM3%2FjoGW7Faix6jNaT53JEBdIQp%2F8KFO7qP3aU5s9XDp9LJ3Oo8fXhADyK13yodJzheq9xcSvg%3D%3D"

        url = "http://openapitraffic.daejeon.go.kr/traffic/rest/getTrafficInfoAll.do?serviceKey={API}&numOfRows=1000&pageNo=1".format(
            API=API_key)
        # date = datetime.datetime.now()
        # data = str(date.hour) + "시" + str(date.minute)+"분"+str(date.second)+"초"
        content = requests.get(url).content
        dict = xmltodict.parse(content)

        jsonString = json.dumps(dict['response']['body']['TRAFFIC-LIST']['TRAFFIC'], ensure_ascii=False)
        jsonObj = json.loads(jsonString)
        ser=[]
        for i in range(len(jsonObj)):
            ser.append(jsonObj[i]['startNodeName'])
            ser.append(jsonObj[i]['endNodeName'])
            ser.append(jsonObj[i]['speed'])

        return ser

class UserManager:  # 사용자관리 및 채팅 메세지 전송을 담당하는 클래스
    # ① 채팅 서버로 입장한 사용자의 등록
    # ② 채팅을 종료하는 사용자의 퇴장 관리
    # ③ 사용자가 입장하고 퇴장하는 관리
    # ④ 사용자가 입력한 메세지를 채팅 서버에 접속한 모두에게 전송
    user = None
    def __init__(self):
        self.users = {}  # 사용자의 등록 정보를 담을 사전 {사용자 이름:(소켓,주소),...}

    def addUser(self, user_id, conn):  # 사용자 ID를 self.users에 추가하는 함수
        try:
            #lock.locked()
            for i in asd.member_id11(user_id[0]):
                if user_id[0] not in self.users:
                    if user_id[0] == i[0]:
                        if user_id[1] == i[1]:
                            self.users[user_id[0]] = (conn)
                            print("딕셔너리 안에 값",self.users)
                            conn.send("/로그인 성공".encode())

                        else:
                            conn.send("/비번틀림".encode())

                    else:
                        conn.send("/없는아이디".encode())

                else:
                    conn.send("/실행중".encode())
            #lock.acquire()

        except Exception as e:
            print("오류발생",e)
    #
    def removeUser(self, username):  # 사용자를 제거하는 함수

        if username not in self.users:
            return
        del self.users[username]


    def messageHandler(self,username, msg):  # 전송한 msg를 처리하는 부분
        data = datetime.datetime.now()
        data = str(data.year) + "-" + str(data.month) + "-" + str(data.day) + "-" + str(data.hour)

        if "/가입" in msg:
            # asd = dbtest
            # asd = asd.member()
            user_insert=msg.split(",")
            #print(user_insert[1].isdigit(),type(user_insert[1]),user_insert[1])
            if user_insert[1].isdigit() == False:
                asd.member_insert(user_insert[1],user_insert[2],user_insert[3],int(user_insert[4]),user_insert[5],
                                  user_insert[6],int(user_insert[7]),user_insert[8])
               # asd.member_table(user_insert[1])
                username.send("/가입완료".encode())

            else:
                username.send("/가입실패".encode())


        elif '/로그인' in msg:
            global user_name
            # print(datetime.datetime.now())
            # asd.traffic_clear()
            # bb = daejeonTraffic()
            # bb.daejeon()
            # print(datetime.datetime.now())
            username.send("/로딩종료".encode())
            time.sleep(0.2)
            user_id = msg.split(",")
            asd.member_log(user_id[1], data)
            user_id = [user_id[1], user_id[2]]
            self.user = user_id[0]
            user_name= user_id[0]
            self.addUser(user_id, username)


        elif "/교통" in msg:
            print("교통########################################")
            print(msg)
            serch.latly_serch(str(msg[4:]),'1')
            bb=str(asd.daejeon_ser(msg[4:]))
            bb.split(',),')
            bb = bb.replace("(","")
            bb= bb.replace(",","")
            bb.replace("'","")
            username.send(f"/검색,{bb}".encode())



        elif "/서치순" in msg:
            sort = str(serch.latly_count())
            sort.split(',),')
            sort = sort.replace("(","")
            sort = sort.replace(",","")
            sort.replace("'", "")
            print(sort,"채팅 메세지 고고고고고고")
            username.send(f"/서치순,{sort}".encode())

        elif "/채팅인" in msg:
            if len(str(msg[5:])) > 0:
                serch.chat_insert(self.user, str(msg[5:]))
                sort = str(serch.chat_list())
                sort.split(',),')
                sort = sort.replace("(", "")
                sort = sort.replace(",", "")
                sort.replace("'", "")
                username.send(f"/채팅고,{sort}".encode())
            else:
                sort = str(serch.chat_list())
                sort.split(',),')
                sort = sort.replace("(", "")
                sort = sort.replace(",", "")
                sort.replace("'", "")
                username.send(f"/채팅고,{sort}".encode())


        elif "/넘버" in msg:
            #bb = asd.daejeon_ser(msg[4:])
            print(msg[4:])
            bb = str(asd.daejeon_num(msg[4:]))
            print(bb)
            bb.split(',),')
            bb.split(',')
            bb = bb.replace("(", "")
            bb = bb.replace(",", "")
            bb.replace("'", "")
            print(bb,"스플릿 정리 후")
            username.send(f"/넘버,{bb}".encode())


        elif "/명소" in msg:
            map = menu_data()
            map = map.mail_post(msg[4:])
            serch.serch_insert(self.user,str(msg[4:]))

            username.send(f"/명소,{map}".encode())
            time.sleep(0.1)
            username.send("/로딩종료".encode())

        elif "/클릭명소" in msg:
            bb=str(serch.serch_list_member(self.user))
            print(bb)
            bb.split(',),')
            bb.split(',')
            bb = bb.replace("(", "")
            bb = bb.replace(",", "")
            bb.replace("'", "")
            print(bb, "스플릿 정리 후")
            username.send(f"/클릭명소,{bb}".encode())
         

        elif "/나가기" in msg:
            self.removeUser(self.user)

        # elif "/뉴스" in msg:
        #     news = str(tag_name[0],class_name[3])
        #     username.send(news.encode())

    def sendMessageToAll(self, msg):
        for conn, addr in self.users.values():
            conn.send(msg.encode())

class MyTcpHandler(socketserver.BaseRequestHandler):
    userman = UserManager()

    def handle(self):  # 클라이언트가 접속시 클라이언트 주소 출력
        print('[%s] 연결됨' % self.client_address[0])
        try:
            while True:
                msg = self.request.recv(10485760)
                self.userman.messageHandler(self.request, msg.decode())


        except Exception as e:
            print(e)

        print('[%s] 접속종료' % self.client_address[0])
        self.userman.removeUser(user_name)


class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def runServer():
    print('+++ 채팅 서버를 시작합니다.')
    print('+++ 채텅 서버를 끝내려면 Ctrl-C를 누르세요.')

    try:
        server = ChatingServer((HOST, PORT), MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('--- 채팅 서버를 종료합니다.')
        server.shutdown()
        server.server_close()

runServer()