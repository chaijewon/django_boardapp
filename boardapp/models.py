from django.db import models
import cx_Oracle

'''
 from (패키지명) import 필요한 파일명  (여러개사용이 가능 : *)
 from django.shortcuts import render,redirect
 import 폴더 없이 ...
 => import BoardDAO
 => import com.sist.BoardDAO
'''
# Create your views here.
def getConnection():
    try:
        conn = cx_Oracle.connect("hr/happy@localhost:1521/xe")
    except Exception as e:
        print(e)
    return conn

def board_list(page):
    conn=getConnection()
    cursor=conn.cursor()
    #페이지 나누기
    rowSize=10
    start=(rowSize*page)-(rowSize-1)
    end=rowSize*page
    sql=f"""
            SELECT no,subject,name,TO_CHAR(redate,'YYYY-MM-DD'),hit,num
            FROM (SELECT no,subject,name,redate,hit,rownum as num
            FROM (SELECT no,subject,name,redate,hit 
            FROM spring_freeboard ORDER BY no DESC))
            WHERE num BETWEEN {start} AND {end}
          """
    #실행 요청
    # 날짜데이터 => HTML  {{vo.redate|date:'Y-M-D'}}
    cursor.execute(sql)
    #결과값 읽기
    board_list=cursor.fetchall()
    #print(board_list)
    #닫기
    cursor.close()
    conn.close()
    return board_list  # () => 튜플 => HTML => 딕트 {"key":값}  => model.addAttribute("key",값) ${key}

def board_totalPage():
    conn=getConnection()
    cursor=conn.cursor()
    sql="SELECT CEIL(COUNT(*)/10.0) FROM spring_freeboard"
    cursor.execute(sql)
    total=cursor.fetchone()
    #print(total[0])
    cursor.close()
    conn.close()
    return total[0]

def board_insert(insert_value):
    conn=getConnection()
    cursor=conn.cursor()
    sql="""
           INSERT INTO spring_freeboard VALUES(
            (SELECT NVL(MAX(no)+1,1) FROM spring_freeboard),:1,:2,:3,:4,SYSDATE,0)
         """
    cursor.execute(sql,insert_value)
    print("게시물 등록 완료")
    conn.commit()
    cursor.close()
    conn.close()

def board_detail(no):
    conn=getConnection()
    cursor=conn.cursor()
    sql=f"""
            UPDATE spring_freeboard SET
            hit=hit+1
            WHERE no={no}
          """
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    cursor=conn.cursor()
    sql=f"""
            SELECT no,name,subject,content,TO_CHAR(redate,'YYYY-MM-DD'),hit
            FROM spring_freeboard
            WHERE no={no}
          """
    cursor.execute(sql)
    board_detail=cursor.fetchone()
    cursor.close()
    conn.close()
    return board_detail

def boardUpdateData(no):
    pass

def boardUpdate(update_data,pwd):
    pass

def boardDelete(no,pwd):
    pass
#board_totalPage()
#board_list(1)



