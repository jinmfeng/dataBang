molest
=====

1. login

url:http://www.renren.com/PLogin.do
success:http://www.renren.com/233330059
time cost:ave=0.3s,max=3.17s
fail:passwd error, http://www.renren.com/SysHome.do?catchaCount=1&failCode=4

2. friendList

url:http://friend.renren.com/GetFriendList.do?curpage={}&id={}
success: the same as orig
fail:(1) no permission
(2)not login: http://www.renren.com/SysHome.do?origURL=http%3A%2F%2Ffriend.renren.com%2FGetFriendList.do%3Fcurpage%3D2%26id%3D240303471
