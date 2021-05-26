from django.urls import path
from boardapp import views
'''
   views : 요청시 => 함수 
   자바 : 어노테이션 @GetMapping..
'''
'''
   @GetMapping
      메소드
   @PostMapping
   @RequestMapping
   GET/POST 
   POST => 맨뒤에 /를 생략 
'''
urlpatterns=[
    path('',views.boardList),
    path('insert/',views.boardInsert),
    path('insert_ok',views.boardInsertOk),
    path('detail/',views.boardDetail),
    path('update/',views.boardUpdate),
    path('update_ok',views.boardUpdateOk),
    path('delete/',views.boardDelete),
    path('delete_ok',views.boardDeleteOk)
]