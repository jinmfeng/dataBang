from renrenCache import *;
cache=RenrenCache();

cache.out()
cache.addItem('friends','23234',{'4323','534234'})
cache.addItem('friends','834',{'4323','534234'})
cache.addItems('name',{'4323':'yang','534234':'wang'})
cache.out()

cache.save()
