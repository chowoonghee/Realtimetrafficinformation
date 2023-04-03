import datetime

import pymysql


class member: #멤버 관련 클래스

    def member_insert(self,mem_id,mem_pw,name,age,sex,address,tel,date):#회원 추가 함수
        con = pymysql.connect(host="localhost",
                              user='root',
                              password='176688',
                              db="testcho_db",
                              charset='utf8'
                              )
        #cur = con.cursor()
        ppl = f"""INSERT INTO testcho_db.member VALUES ('{mem_id}','{mem_pw}','{name}','{age}','{sex}','{address}','{tel}','{date}'); """
        with con:
            with con.cursor() as cur:
                cur.execute(ppl)
                con.commit()
                cur.close()
        return

    def daejeon_insert(self,car_start,car_end,car_speed,car_see,car_ud):#회원 추가 함수
        con = pymysql.connect(host="localhost",
                              user='root',
                              password='176688',
                              db="testcho_db",
                              charset='utf8'
                              )
        #cur = con.cursor()
        ppl = f"""INSERT INTO testcho_db.daejeon VALUES (NULL,'{car_start}','{car_end}','{car_speed}','{car_see}','{car_ud}'); """
        with con:
            with con.cursor() as cur:
                cur.execute(ppl)
                con.commit()
                cur.close()
        return

    def daejeon_show(self):#멤버 정보 비밀번호 제외 보여줌
        con = pymysql.connect(host="localhost",
                              user='root',
                              password='176688',
                              db="testcho_db",
                              charset='utf8'
                              )

        cur = con.cursor()

        ppl = f"""SELECT car_start, car_end, car_speed, car_see, car_ud  FROM testcho_db.daejeon;"""
        #self.cur.execute(use)
        cur.execute(ppl)
        data = cur.fetchall()
        return data

    def daejeon_start(self):#멤버 정보 비밀번호 제외 보여줌
        con = pymysql.connect(host="localhost",
                              user='root',
                              password='176688',
                              db="testcho_db",
                              charset='utf8'
                              )

        cur = con.cursor()

        ppl = f"""SELECT car_start FROM testcho_db.daejeon;"""
        #self.cur.execute(use)
        cur.execute(ppl)
        data = cur.fetchall()
        return data

    def daejeon_ser(self,name):#트래픽 테이블에 name이 포함된 도로를 다 출력하는 함수
        con = pymysql.connect(host="localhost",
                              user='root',
                              password='176688',
                              db="testcho_db",
                              charset='utf8'
                              )

        cur = con.cursor()
        ppl = f"""SELECT num,car_start FROM testcho_db.daejeon WHERE car_start LIKE '%{name}%';"""
        #self.cur.execute(use)
        cur.execute(ppl)
        data = cur.fetchall()
        return data

    def daejeon_num(self, name):  # num값 안에 계산 가져오기
        con = pymysql.connect(host="localhost",
                              user='root',
                              password='176688',
                              db="testcho_db",
                              charset='utf8'
                              )

        cur = con.cursor()
        ppl = f"""SELECT car_start,car_end,car_speed,car_see,car_ud FROM testcho_db.daejeon WHERE num ={name};"""
        # self.cur.execute(use)
        cur.execute(ppl)
        data = cur.fetchall()
        return data




    def daejeon_delete(self): #가입된 회원 삭제 함수
        con = pymysql.connect(host="localhost",
                              user='root',
                              password='176688',
                              db="testcho_db",
                              charset='utf8'
                              )

        ppl = f"""delete from testcho_db.daejeon;"""
        with con:
            with con.cursor() as cur:
                cur.execute(ppl)
                con.commit()
                cur.close()
        return


    def member_log(self,mem_id,date): #로그인 시간 기록
        con = pymysql.connect(host="localhost",
                              user='root',
                              password='176688',
                              db="testcho_db",
                              charset='utf8'
                              )
        # cur = con.cursor()
        ppl = f"""INSERT INTO testcho_db.data VALUES (NULL,'{mem_id}','{date}'); """
        with con:
            with con.cursor() as cur:
                cur.execute(ppl)
                con.commit()
                cur.close()
        return

    def member_delete(self,name): #가입된 회원 삭제 함수
        con = pymysql.connect(host="localhost",
                              user='root',
                              password='176688',
                              db="testcho_db",
                              charset='utf8'
                              )
        #cur = con.cursor()
        ppl = f"""delete from testcho_db.member where mem_id='{name}';"""
        with con:
            with con.cursor() as cur:
                cur.execute(ppl)
                con.commit()
                cur.close()
        return

    def member_show(self,name):#멤버 정보 비밀번호 제외 보여줌
        con = pymysql.connect(host="localhost",
                              user='root',
                              password='176688',
                              db="testcho_db",
                              charset='utf8'
                              )
        cur = con.cursor()
        ppl = f"""SELECT mem_id, mem_name,  phone1, mem_addr amount FROM testcho_db.member WHERE mem_id='{name}';"""
        #self.cur.execute(use)
        cur.execute(ppl)
        data = cur.fetchall()
        return data

    # def latly_serch(self,name,count): #검색어 순위 + 이름 숫자
    #     con = pymysql.connect(host="localhost",
    #                           user='root',
    #                           password='176688',
    #                           db="testcho_db",
    #                           charset='utf8'
    #                           )
    #     ppl = f"""INSERT INTO testcho_db.lately_serch VALUES (NULL,'{name}','{count}'); """
    #     with con:
    #         with con.cursor() as cur:
    #             cur.execute(ppl)
    #             con.commit()
    #             cur.close()
    #     return

    def traffic_clear(self):
        con = pymysql.connect(host="localhost",
                              user='root',
                              password='176688',
                              db="testcho_db",
                              charset='utf8'
                              )
        # cur = con.cursor()
        ppl2 = f"""delete  from testcho_db.daejeon;"""
        with con:
            with con.cursor() as cur:
                cur.execute(ppl2)
                con.commit()
                cur.close()
        return


    def member_update(self,set,set1): #멤버 정보 변경 함수? => 일단 주소 변경
        con = pymysql.connect(host="localhost",
                              user='root',
                              password='176688',
                              db="testcho_db",
                              charset='utf8'
                              )
        #cur = con.cursor()
        ppl2=f"""UPDATE testshopping.member SET mem_addr = '{set1}' WHERE mem_id = '{set}';"""
        with con:
            with con.cursor() as cur:
                cur.execute(ppl2)
                con.commit()
                cur.close()
        return
    def member_id(self):#아이디 전부
        con = pymysql.connect(host="localhost",
                              user='root',
                              password='176688',
                              db="testcho_db",
                              charset='utf8'
                              )
        cur = con.cursor()
        ppl = f"""SELECT mem_id,mem_pw FROM testcho_db.member;"""
        # self.cur.execute(use)
        cur.execute(ppl)
        data = list(cur.fetchall())
        return data

    def member_id11(self,name):  # 아이디 전부
        con = pymysql.connect(host="localhost",
                              user='root',
                              password='176688',
                              db="testcho_db",
                              charset='utf8'
                              )
        cur = con.cursor()
        ppl = f"""SELECT mem_id,mem_pw FROM testcho_db.member where mem_id="{name}";"""
        # self.cur.execute(use)
        cur.execute(ppl)
        data = list(cur.fetchall())
        return data


    def member_table(self,name):  # 멤버 테이블 만드는 함수    아이디 검색어 횟수 날짜
        con = pymysql.connect(host="localhost",
                              user='root',
                              password='176688',
                              db="testcho_db",
                              charset='utf8'
                              )
        #cur = con.cursor()
        ppl = f"""create table {name}(
                    mem_id varchar(20) not null primary key,
                    serch varchar(20) not null,
                    amount varchar(20) not null,
                    debut_date date);"""
        with con:
            with con.cursor() as cur:
                cur.execute(ppl)
                con.commit()
                cur.close()
        return

class lately_serch:

    def latly_serch(self,name,count): #검색어 순위 + 이름 숫자
        con = pymysql.connect(host="localhost",
                              user='root',
                              password='176688',
                              db="testcho_db",
                              charset='utf8'
                              )
        ppl = f"""INSERT INTO testcho_db.lately_serch VALUES (NULL,'{name}','{count}'); """
        with con:
            with con.cursor() as cur:
                cur.execute(ppl)
                con.commit()
                cur.close()
        return

    def latly_count(self): # 최다 검색어
        con = pymysql.connect(host="localhost",
                              user='root',
                              password='176688',
                              db="testcho_db",
                              charset='utf8'
                              )
        cur = con.cursor()
        ppl = """SELECT serch FROM testcho_db.lately_serch GROUP BY serch HAVING COUNT(serch) > 0 ORDER BY COUNT(serch) DESC ;"""
        cur.execute(ppl)
        data = list(cur.fetchall())
        return data

    def chat_insert(self,name,chat): #채팅테이블에 담기
        con = pymysql.connect(host="localhost",
                              user='root',
                              password='176688',
                              db="testcho_db",
                              charset='utf8'
                              )
        ppl = f"""INSERT INTO testcho_db.chat_list VALUES (NULL,'{name}','{chat}'); """
        with con:
            with con.cursor() as cur:
                cur.execute(ppl)
                con.commit()
                cur.close()
        return
    def serch_insert(self,name,chat): #검색어 인서트 하기
        con = pymysql.connect(host="localhost",
                              user='root',
                              password='176688',
                              db="testcho_db",
                              charset='utf8'
                              )

        ppl = f"""INSERT INTO testcho_db.serch_list VALUES (NULL,'{name}','{chat}'); """
        with con:
            with con.cursor() as cur:
                cur.execute(ppl)
                con.commit()
                cur.close()
        return


    def serch_list(self): # 인기 검색어
        con = pymysql.connect(host="localhost",
                              user='root',
                              password='176688',
                              db="testcho_db",
                              charset='utf8'
                              )
        cur = con.cursor()
        ppl = """SELECT serch FROM testcho_db.serch_list GROUP BY serch HAVING COUNT(serch) > 0 ORDER BY COUNT(serch) ASC ;"""
        cur.execute(ppl)
        data = list(cur.fetchall())
        return data

    def serch_list_member(self,name):#본인 검색 한거 최다
        con = pymysql.connect(host="localhost",
                              user='root',
                              password='176688',
                              db="testcho_db",
                              charset='utf8'
                              )
        cur = con.cursor()
        ppl = f"""SELECT serch FROM testcho_db.serch_list where mem_id='{name}' ORDER BY num DESC ;"""
        cur.execute(ppl)
        data = list(cur.fetchall())
        return data

    def chat_list(self): #무기명 채팅 리스트에 넣기
        con = pymysql.connect(host="localhost",
                              user='root',
                              password='176688',
                              db="testcho_db",
                              charset='utf8'
                              )
        cur = con.cursor()
        ppl = """SELECT serch FROM testcho_db.chat_list ORDER BY NULL DESC ;"""
        cur.execute(ppl)
        data = list(cur.fetchall())
        return data

class parking:
    def parking_check(self):
        con = pymysql.connect(host="localhost",
                              user='root',
                              password='176688',
                              db="jucha_db",
                              charset='utf8'
                              )
        cur = con.cursor()
        ppl = f"""SELECT car_number FROM jucha_db.parkng_in;"""
        # self.cur.execute(use)
        cur.execute(ppl)
        data = list(cur.fetchall())
        return data




asd = '1234'

print(len(asd))
