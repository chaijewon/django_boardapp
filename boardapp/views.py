from django.shortcuts import render,redirect
from boardapp import  models
'''
   url 설정 
   데이터 받기, 데이터 전송 
   CURD(INSERT,UPDATE,DELETE,SELECT)
'''
def boardList(request):
    # 사용자 요청값을 받는다
    page=request.GET['page']
    curpage=int(page)
    board_list=models.board_list(curpage)
    totalpage=models.board_totalPage()
    # 데이터베이스 연결
    # 데이터 전송준비
    list=[]
    for row in board_list:
        data = {"no": row[0], "subject": row[1], "name": row[2], "regdate": row[3], "hit": row[4]}
        list.append(data)

    return render(request, 'board/board_list.html', {"curpage": curpage, "totalpage": totalpage, "list": list})
'''
  (11, '홍길동', '성동구 송정동 바퀴벌레 조치 바랍니다(수정)', <cx_Oracle.LOB ob
   ject at 0x0000025FEF54CAE0>)
   
'''

def boardDetail(request):
    no=request.GET['no']
    board_detail=models.board_detail(int(no))
    print(board_detail)
    data={"no":board_detail[0],
            "name":board_detail[1],
            "subject":board_detail[2],
            "content":board_detail[3],
            "regdate":board_detail[4],
            "hit":board_detail[5],"result":False}
    return render(request,'board/board_detail.html',data)


def boardInsert(request):
    return render(request, 'board/board_insert.html')


def boardInsertOk(request):
    print("boardInsertOk")
    #print(request.POST)
    name=request.POST['name']
    subject=request.POST['subject']
    content=request.POST['content']
    pwd=request.POST['pwd']
    print('name='+name,'subject='+subject,'content='+content,'pwd='+pwd)
    data=(name,subject,content,pwd)
    models.board_insert(data)
    return redirect('/board/?page=1')

def boardUpdate(request):
    no=request.GET['no']
    data=models.boardUpdateData(int(no))
    updata={"no":data[0],"name":data[1],"subject":data[2],"content":data[3]}
    return render(request,'board/board_update.html',{"updata":updata})

def boardUpdateOk(request):
    name=request.POST['name']
    no=request.POST['no']
    subject=request.POST['subject']
    content=request.POST['content']
    pwd=request.POST['pwd']
    print(name,no,subject,content,pwd)
    data=(name,subject,content,no,pwd)
    result=models.boardUpdate(data)
    return render(request,'board/board_update_ok.html',{"no":no,"result":result})

def boardDelete(request):
    no=request.GET['no']
    return render(request,'board/board_delete.html',{"no":no})

def boardDeleteOk(request):
    no=request.POST['no']
    pwd=request.POST['pwd']
    #print("no="+no,"pwd="+pwd)
    result=models.boardDelete(int(no),pwd)
    return render(request,'board/board_delete_ok.html',{"result":result})

