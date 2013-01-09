from renrenBrowser import *

renrenId='233330059'

browser=RenrenBrowser()
browser.login()
browser.setLogLevel(10)

#get one page of every kind of pageStyle
browser.savePage('friendList',browser.friendList(renrenId,1))
browser.savePage('status',browser.status(renrenId,1))
browser.savePage('profile',browser.profile(renrenId))

browser.friendList(renrenId)
browser.status(renrenId)
