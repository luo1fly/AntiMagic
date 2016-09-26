# AntiMagic说明文档 #
## settings.py起始设置 ##
1.	数据库连接：
	- 创建名为antimagic的数据库，指定默认字符集utf8，授权django用户所有权限
	
		 	mysql> create database antimagic charset utf8;
			Query OK, 1 row affected (0.00 sec)
			
			mysql> grant all on antimagic.* to 'django'@'localhost' identified by 'django';
			Query OK, 0 rows affected (0.00 sec)
	- setttings.py相关配置，Python3.5使用pymssql代替mysqldb
	
			__import__('pymysql').install_as_MySQLdb()
			DATABASES = {
			    'default': {
			        'ENGINE': 'django.db.backends.mysql',
			        'NAME': 'antimagic',
			        'USER': 'django',
			        'PASSWORD': 'django',
			        'HOST': '',
			        'PORT': '3306',
			    }
			}
	- 参考：[https://docs.djangoproject.com/en/1.10/ref/settings/#databases](https://docs.djangoproject.com/en/1.10/ref/settings/#databases)
2.	静态文件存放路径：
	- 项目根目录下创建statics目录
	- settings.py添加配置如下：
	
			STATICFILES_DIRS = [
		    	os.path.join(BASE_DIR, "statics"),
			]
	- 参考：[https://docs.djangoproject.com/en/1.10/howto/static-files/](https://docs.djangoproject.com/en/1.10/howto/static-files/)
3.	自定义用户认证相关配置：
	- settings.py添加配置如下：
	
			AUTH_USER_MODEL = 'hosts.UserProfile'
	- 参考：[https://docs.djangoproject.com/en/1.10/topics/auth/customizing/](https://docs.djangoproject.com/en/1.10/topics/auth/customizing/)
4.	修改默认登录链接：
	- settings.py添加配置如下，默认链接'/accounts/login/'：
	
			LOGIN_URL = '/login/'
	- 参考：[https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-LOGIN_URL](https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-LOGIN_URL)
5.	配置启用django的rest_framework:
	- settings.py修改如下：
	
			INSTALLED_APPS = [
			    'django.contrib.admin',
			    'django.contrib.auth',
			    'django.contrib.contenttypes',
			    'django.contrib.sessions',
			    'django.contrib.messages',
			    'django.contrib.staticfiles',
			    'rest_framework',
			    'assets',
			    'hosts',
			]
	- 添加如下：
	
			REST_FRAMEWORK = {
			    # Use Django's standard `django.contrib.auth` permissions,
			    # or allow read-only access for unauthenticated users.
			    'DEFAULT_PERMISSION_CLASSES': [
			        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
			    ]
			}
## 创建自定义用户认证 ##
> 由于我们要建立包含cmdb和主机管理功能的项目，所以将用户认证的功能放置在主机管理app下

1.	创建一个app名叫hosts：

		[root@fedora-minion AntiMagic]# ./manage.py startapp hosts
2.	settings.py中确保已经注册：

		INSTALLED_APPS = [
		    'django.contrib.admin',
		    'django.contrib.auth',
		    'django.contrib.contenttypes',
		    'django.contrib.sessions',
		    'django.contrib.messages',
		    'django.contrib.staticfiles',
		    'assets',
		    'hosts',
		]
3.	hosts目录下创建一个cus_auth.py，创建两个类UserManager、UserProfile，这个UserProfile类就是映射为我们自定义的认证表
4.	hosts/models.py中导入UserProfile类
5.	hosts/admin.py中创建三个类UserCreationForm、UserChangeForm、UserProfileAdmin，前两个实现django的form表单，用来在后台做用户信息的修改，UserProfileAdmin用来做UserProfile表在后台的展示定制
6.	以上完成后到项目根目录下执行makemigrations和migrate操作，完成数据库初始化

		[root@fedora-minion AntiMagic]# ./manage.py makemigrations
		Migrations for 'hosts':
		  hosts/migrations/0001_initial.py:
		    - Create model UserProfile
		[root@fedora-minion AntiMagic]# ./manage.py migrate
		Operations to perform:
		  Apply all migrations: admin, auth, contenttypes, hosts, sessions
		Running migrations:
		  Applying hosts.0001_initial... OK
		  Applying contenttypes.0001_initial... OK
		  Applying admin.0001_initial... OK
		  Applying admin.0002_logentry_remove_auto_add... OK
		  Applying contenttypes.0002_remove_content_type_name... OK
		  Applying auth.0001_initial... OK
		  Applying auth.0002_alter_permission_name_max_length... OK
		  Applying auth.0003_alter_user_email_max_length... OK
		  Applying auth.0004_alter_user_username_opts... OK
		  Applying auth.0005_alter_user_last_login_null... OK
		  Applying auth.0006_require_contenttypes_0002... OK
		  Applying auth.0007_alter_validators_add_error_messages... OK
		  Applying auth.0008_alter_user_username_max_length... OK
		  Applying sessions.0001_initial... OK
7.	创建超级用户

		[root@fedora-minion AntiMagic]# ./manage.py createsuperuser
		Email address: luo1fly@gmail.com
		姓名: 
		Password: 
		Password (again): 
		Superuser created successfully.
8.	创建用户完成后pycharm启动服务，用刚刚创建的用户登录后台，可以查看到自己的数据
## 创建cmdb表结构 ##
> cmdb的核心在于数据库设计，我们把服务器端程序放置在assets应用下

1.	我们参考MadKing项目的数据库设计，引入本项目遇到了跨app引用数据库表的问题，解决方法如下：
		
		from hosts import models as hosts_models
		# 对models取别名hosts_models
		admin = models.ForeignKey(hosts_models.UserProfile, verbose_name=u'资产管理员', null=True, blank=True)
		# 外键关联的时候显式的生命hosts_models.UserProfile
2.	models.py和admin.py的其他内容并未做过多改动
3.	同步数据库，后台查看

## django的登录验证 ##
> 结合网站请求过程来看，访问的第一步是请求地址，服务器端接收到第一步应当是url模式匹配，交给对应视图去处理，以登录为例

1.	上文已经在settings.py中配置过登录的地址，所以在urls.py文件的urlpatterns列表中必须要有/login/对应的设置：

		urlpatterns = [
		    url(r'^admin/', admin.site.urls),
		    url(r'^login/$', views.acc_login, name='login'),
		]
2.	我们在项目同名目录AntiMagic下创建一个views.py视图文件，其中需要定义acc_login函数来处理登录验证：

		def acc_login(request):
		    if request.method == "POST":		
		        username = request.POST.get('email')
		        password = request.POST.get('password')
		        user = auth.authenticate(username=username, password=password)
		        if user:
		            if user.valid_begin_time < timezone.now() < user.valid_end_time:
					# 确保登录时间在账户有效期内
		                auth.login(request, user)
						# 登录动作
		                request.session.set_expiry(60*30)
		                # 设置session超时时间30分钟
		                return HttpResponseRedirect('/')
		            else:
		                return render(request, 'login.html', {
		                    'login_err': '对不起您的账户已过期，请联系系统管理员!'
		                })
		
		        else:
		            return render(request, 'login.html', {
		                'login_err': 'Wrong username or password!'
		            })
		    else:
		        return render(request, 'login.html')
3.	附带介绍一个django的带时区时间用法，区别于Python原生用法：

		from django.utils import timezone
		timezone.now()
4.	通常我们的习惯不会是直接访问登录页，而是访问首页，这就要求在显示homepage之前弹出登录页，这个做法在django中很常见：

		from django.contrib.auth.decorators import login_required

		@login_required
		def index(request):
		    return render(request, 'index.html')
		# 索引视图前加上login_required装饰器，强制进行登录验证，在你认为需要登录的页面视图前都可以这么用
## djangorestframework的引入 ##
>  CMDB本质上是维护了一个配置数据库，所以提供客户端导入数据接口和外部查询接口是必要的，我们引入一下restframework的概念：[http://www.ruanyifeng.com/blog/2014/05/restful_api.html](http://www.ruanyifeng.com/blog/2014/05/restful_api.html)。django中我们使用djangorestframework框架来实现，下面简单介绍一下在本项目中的运用。

1.	接口的访问本质上依然是一次http请求，所以我们还是遵循前面的规则，从url的匹配开始：

		from django.conf.urls import url, include
		# 引入include工具
		from assets import rest_urls
		# 引入assets目录下的rest_urls文件
		urlpatterns = [
		    url(r'^admin/', admin.site.urls),
		    url(r'^login/$', views.acc_login, name='login'),
			url(r'^api/', include(rest_urls)),
			# 二级路径指向的视图从rest_urls这个文件中引入
		]
2.	我们到assets目录下创建一个rest_urls.py文件：

		from django.conf.urls import (url, include)
		from rest_framework import routers
		# 引入routers
		from assets import rest_views
		# 引入assets下的rest_views文件
		
		router = routers.DefaultRouter()
		# 创建一个router
		router.register(r'users', rest_views.UserViewSet)
		router.register(r'asset', rest_views.AssetViewSet)
		router.register(r'server', rest_views.ServerViewSet)
3.	assest目录下创建rest_views.py文件：

		from rest_framework import viewsets
		# 引入rest_framework的viewsets视图集
		from assets import serializers
		# 引入assets目录下的serializers.py文件
		from hosts import models as hosts_models
		# 注意跨app引用数据库表的用法
		
		# import custom modules above

		class UserViewSet(viewsets.ModelViewSet):
		    """
	        API endpoint that allows users to be viewed or edited.
		    """
			# 以上docstring会在api说明页面展示出来，请认真填写
		    queryset = hosts_models.UserProfile.objects.all().order_by('-date_joined')
		    # 数据库查询结果集，根据时间倒序排列
		    serializer_class = serializers.UserSerializer
			# 使用自定义的serializers进行序列化
4.	assets目录下创建serializers.py文件：

		from rest_framework import serializers
		# 引入rest_framework的serializers
		from hosts import models as hosts_models
		# import custom modules above

		class UserSerializer(serializers.HyperlinkedModelSerializer):
		    """
		        重写父类，把实例对象转换成前端能够展示的json格式
		    """
		    class Meta:
		        """
		            @:parameter model:
		            @:parameter fields:
		        """
		        model = hosts_models.UserProfile
		        depth = 2
		        # fields = ('url', 'name', 'email', 'is_admin')
5.	访问[http://192.168.0.194:8000/api/](http://192.168.0.194:8000/api/)可以查看接口信息
6.	rest的使用还是比较复杂，这边简单说明一下，后面用到的时候再详细介绍
## 简单高效的身份验证方式 ##
> 身份验证方式和ssl协议是两种不同的安全机制，https重在数据传输的加密，建立连：

1.	客户端需要在向服务器post的消息体（json）中包含哪些：
	- 用户名username
	- 用户usertoken
	- 时间戳timestamp
2.	服务器端需要设定的规则有：
	- 一个token在固定时间段t内只能请求一次
	- 设定请求超时时间t
	- 维护一份token记录，仅保存时间段t内收到的usertoken
3.	服务器和客户端需要实现约定的规则，一个加密字符串（key），一个固定加密算法
4.	认证过程简述：
	- 合法用户在服务器注册一个账号为username，服务器给该用户分配一个加密字符串key
	- 合法用户将自己的username和key记录在客户端配置文件中
	- 客户端程序在生成了资产消息体后，根据当前系统时间戳timestamp和username以及key使用和服务器端约定好的算法生成一个token值，截取其中一段作为消息体中内容，发送给服务器端
	- 服务器端接收到客户端发过来的消息体，第一步会判断是否超时，如果超时都不需要再进行运算即可deny客户端请求；第二步，如果未超时，判断该次请求的usertoken是否已经使用过，如果已经用过则deny请求；第三步，若未用过，则用约定好的算法将本地保存的key和客户端发送过来的username以及timestamp计算出一个servertoken，并按照约定截取顺序截取其中一段与usertoken进行比较，若相等，则验证客户端身份合法，若不等，则deny客户端请求
5.	我们模拟一次攻击场景，假设黑客已经截取到一个完整的客户端请求：
	- 理论上来说客户端的请求是会在黑客的伪装请求到达服务器之前到达并完成，当黑客请求到达服务器之时，服务器进行第一步判断
	- 若此时已超时，则deny请求，若未超时，进行第二步判断
	- 此时请求未超时，在服务器端维护的记录表中一定是有真实客户端提交过来的usertoken的，所以黑客请求中的usertoken被认为已使用过，所以deny此次请求
	- 所以在黑客不知道加密算法和key的情况下，即便截获了请求数据，也无法随意提交到服务器端，保证了客户端身份的有效性
6.	这种认证策略简单高效，目前已经被广泛运用在各大网站（Amazon）
7.	我们来分析一下客户端和服务器端代码实现：
	- 先看客户端：
	
			import hashlib, time			
			
			def get_token(username, key):
			    timestamp = int(time.time())
				# 取客户端时间戳
			    md5_format_str = "%s\n%s\n%s" % (username, timestamp, key)
				# 拼接username timestamp key
			    obj = hashlib.md5()
			    obj.update(md5_format_str)
				# md5算法加密
			    return obj.hexdigest()[10:17], timestamp
	- 服务器端定义一个工具装饰器token_required来实现验证功能：
	
			def token_required(func):
			    def wrapper(*args, **kwargs):
			        response = {"errors": []}
			
			        get_args = args[0].GET
			        username = get_args.get("user")
					# 获取到username
			        token_md5_from_client = get_args.get("token")
					# 获取到客户端usertoken
			        timestamp = get_args.get("timestamp")
					# 获取到客户端时间戳timestamp
			        if not username or not timestamp or not token_md5_from_client:
			            response['errors'].append({"auth_failed": "This api requires token authentication!"})
			            return HttpResponse(json.dumps(response))
					# 缺任何一个都验证失败
			        try:
			            user_obj = hosts_models.UserProfile.objects.get(email=username)
			            token_md5_from_server = gen_token(username,timestamp,user_obj.token)
						# gen_token函数和客户端保证一致
			            if token_md5_from_client != token_md5_from_server:
			                response['errors'].append({"auth_failed":"Invalid username or token_id"})
			            else:
			                if abs(time.time() - int(timestamp)) > settings.TOKEN_TIMEOUT:
			                    # default timeout 120
			                    response['errors'].append({"auth_failed": "The token is expired!"})
			                else:
			                    pass
			                    # print "\033[31;1mPass authentication\033[0m"
			                print(
			                    "\033[41;1m;%s ---client:%s\033[0m" % (time.time(), timestamp),
			                    time.time() - int(timestamp)
			                )
						# 仅作时间验证，实际运用可以调整
			        except ObjectDoesNotExist as e:
			            response['errors'].append({"auth_failed": "Invalid username or token_id"})
			        if response['errors']:
			            return HttpResponse(json.dumps(response))
			        else:
			            return func(*args, **kwargs)
			    return wrapper
	- 由于是内网传输，实际运用中简化了安全认证方式，后续思考如何维护一个短期贮存的数据结构，定时刷新，目前有一种方式是给redis的key设置过期时间，没有去实现，但是难度不大，提示：
	
				127.0.0.1:6379> SET 4e877b4faaa37c used ex 60
				OK
				127.0.0.1:6379> TTL 4e877b4faaa37c
				(integer) 52

	- 最后我们使用token_required来装饰需要进行安全认证的接口视图函数：
	
				@utils.token_required
				def asset_report(request):
				    print(request.GET)
				    if request.method == 'POST':
				        ass_handler = core.Asset(request)
				        if ass_handler.data_is_valid():
				            ass_handler.data_inject()
				        return HttpResponse(json.dumps(ass_handler.response))
				    return HttpResponse('--test--')
	- 注意装饰器的使用，非常巧妙
## 自定义用户模板 ##
> 常用模版工具有filter和simpletag，他们本质上还是功能函数，下面简单说一下怎么使用，详细参考：[https://docs.djangoproject.com/en/1.10/howto/custom-template-tags/](https://docs.djangoproject.com/en/1.10/howto/custom-template-tags/)

1.	在包目录（hosts和assets）下面创建一个子包，名称叫templatetags，名称不要修改，目录树如下：

		[root@fedora-minion hosts]# tree .
		.
		├── admin.py
		├── apps.py
		├── __init__.py
		├── migrations
		│   └── __init__.py
		├── models.py
		├── templatetags
		│   └── __init__.py
		├── tests.py
		└── views.py
2.	在templatetags目录中创建一个custome.py，内容如下：

		from django import template
		# 导入template模块
		register = template.Library()
		# 创建一个注册器对象
	
		@register.simple_tag
		def build_comment_tree(tree_data):
		# 用register.simplte_tag装饰器生成自定义标签
		    html_ele = ""
		    for p, v in tree_data.items():
		        row = '''<div style="margin-top:15px;border-left:1px dashed green;border-bottom:1px  dashed green">
		                <span class="comment-user">%s</span>
		                <span class="comment-content">%s</span>
		                <span class="comment-date">%s</span>
		                </div>''' % (p.user.name, p.comment, p.add_date)
		        if v is not None:   # has son
		            row += insert_comment_node(v, 20)
		        html_ele += row
		    return html_ele

		@register.filter
		def insert_comment_node(data_dic, margin_val):
		# register.filter装饰器生成自定义过滤器
		    html = ''
		    for p, v in data_dic.items():
		        r = '''<div style="margin-left:%spx;margin-top:15px;border-left:1px dashed green;border-bottom:1px dashed green">
		                <span class="comment-user">%s</span>
		                <span class="comment-content">%s</span>
		                <span class="comment-date">%s</span>
		                </div>''' % (margin_val, p.user.name, p.comment, p.add_date)
		        if v is not None:
		            r += insert_comment_node(v, margin_val+20)
		        html += r
		    # print(html)
		    return html
3.	引用自定义模板的方式很简单，在模板文件中加入：

		{% load custom %}
		
		<div class="comments-box">
        	{% build_comment_tree comments as ac %}
            {{ ac|safe }}
			# 注意safe过滤器的用法
        </div>


## 主机管理相关介绍 ##
> cmdb这块主要偏重后端，前端按照具体需求来制作，下面我们讨论主机管理的应用

1.	数据库设计注意点：
	- 首先，我们考虑到管理终端操作的不仅仅是物理机，还有各种各样的虚拟机，所以不能直接外键cmdb的server表，需要调用接口来查询数据，当然了，我们也可以把两个项目剥离开，放在一起是为了共用一套登录验证，详细的设计参见hosts/models.py
	- 同步数据库
## 生产环境使用nginx+uwsgi运行django程序 ##
> 其实不仅仅django，所有支持wsgi方式托管的web框架开发的应用都可以用这种方式在生产环境来运行

1.	克隆项目到线上服务器

		[root@luo1fly ~]# git clone https://github.com/luo1fly/AntiMagic.git
2.	修改settings.py添加如下配置

		# added by luo1fly for STATIC_ROOT configuration
		STATIC_ROOT = 'static'
		# static是一个相对目录，参考官方文档
3.	在项目根目录执行如下命令，将静态文件都拷贝到该目录下：

		[root@luo1fly AntiMagic]# ./manage.py collectstatic
		[root@luo1fly AntiMagic]# ls
		AMClient  AntiMagic  assets  hosts  LICENSE  manage.py  README.md  static  statics  templates
		[root@luo1fly AntiMagic]# ls static
		admin  css  fonts  js  plugins  rest_framework
4.	以上是静态文件的相关配置，真实线上也可以用nginx的location去做，这边就简化一下配置到uwsgi里面
5.	我们采用ini文件（yaml和json也是支持的）的方式管理uwsgi，我们在项目同名目录下创建一个uwsgi.ini文件，内容如下：

		[uwsgi]
		socket = 127.0.0.1:8000
		pidfile = /var/run/uwsgi.pid
		daemonize = /var/log/AntiMagic/uwsgi.log
		chdir = /var/lib/nginx/AntiMagic
		wsgi-file = AntiMagic/wsgi.py
		module = AntiMagic.wsgi:application
		stats = 0.0.0.0:9191

6.	执行如下命令，后台会启动一个守护进程和一个工作进程：

		[root@luo1fly AntiMagic]# uwsgi --ini AntiMagic/uwsgi.ini
		[root@luo1fly AntiMagic]# ps aux|grep uwsgi
		root      9077  0.0  0.7 237936 29616 ?        S    14:18   0:00 uwsgi --ini AntiMagic/uwsgi.ini
		root      9080  0.0  0.9 282020 38516 ?        S    14:18   0:00 uwsgi --ini AntiMagic/uwsgi.ini
7.	以上过程只起了一个socket，我们可以通过telnet验证端口是否监听，但无法直接从浏览器访问页面，下面讲述提供http访问的步骤
8.	我们采用nginx服务器作为部署环境，下面是相关的server配置（去除了很多干扰项，实际运行中酌情配置）：

		server {
		        listen       80;
		        server_name  localhost;
		
		        location / {
		            include uwsgi_params;
			    	uwsgi_pass 127.0.0.1:8000;
		        }
		
				location ~ /static {
				    root /var/lib/nginx/AntiMagic;
				}
				...
		}
9.	我们要重点关注一下static相关的location，思考为什么第一第二步要将静态文件集中到一个路径，为什么不在uwsgi测进行静态文件处理（事实上是可以的，我们称之为动静分离，但这是web服务器的强项，而不应该交给cgi管理器去处理，这就是原因所在）
10.	启动nginx以后可以访问一下80端口
11.	一些常用的优化配置可以参考相关文档
