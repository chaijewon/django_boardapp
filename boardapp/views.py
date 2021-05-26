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


def boardDetail(request):
    no=request.GET['no']
    board_detail=models.board_detail(int(no))
    print(board_detail)
    data={"no":board_detail[0],
            "name":board_detail[1],
            "subject":board_detail[2],
            "content":board_detail[3],
            "regdate":board_detail[4],
            "hit":board_detail[5]}
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
    pass

def boardUpdateOk(request):
    pass

def boardDelete(request):
    pass

def boardDeleteOk(request):
    pass

