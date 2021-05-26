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
    #clob => .read()
    data=(board_detail[0],board_detail[1],board_detail[2],board_detail[3].read(),board_detail[4],board_detail[5])
    cursor.close()
    conn.close()
    return data

def boardUpdateData(no):
    conn=getConnection()
    cursor=conn.cursor()
    sql=f"""
            SELECT no,name,subject,content 
            FROM spring_freeboard
            WHERE no={no}
          """
    cursor.execute(sql)
    data=cursor.fetchone()
    #print(data)
    update_data=(data[0],data[1],data[2],data[3].read())
    #print(update_data)
    cursor.close()
    conn.close()
    return update_data

def boardUpdate(update_data):
    conn=getConnection()
    cursor=conn.cursor()
    sql=f"""
           SELECT pwd FROM spring_freeboard
           WHERE no={update_data[3]}
          """
    cursor.execute(sql)
    redata=cursor.fetchone()
    cursor.close()
    result=False
    if redata[0] == update_data[4] :
        result=True
        cursor=conn.cursor()
        sql="""
                UPDATE spring_freeboard SET
                name=:1 , subject=:2 , content=:3
                WHERE no=:4 
              """
        cursor.execute(sql,(update_data[0],update_data[1],update_data[2],update_data[3]))
        conn.commit()
        cursor.close()
    else :
        result=False

        conn.close()
    return result


def boardDelete(no,pwd):
    conn=getConnection()
    cursor=conn.cursor()
    sql=f"""
             SELECT pwd FROM spring_freeboard
             WHERE no={no}
          """
    cursor.execute(sql)
    db_pwd=cursor.fetchone()
    # (1234,)
    cursor.close()
    result=False
    if pwd == db_pwd[0] :
        result=True
        cursor=conn.cursor()
        sql=f"""
                DELETE FROM spring_freeboard
                WHERE no={no}
              """
        cursor.execute(sql)
        conn.commit()
        cursor.close()
    else :
        result=False
    conn.close()
    return result


#board_totalPage()
#board_list(1)



