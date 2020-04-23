from django.http import *
import simplejson
from .models import User
from django.db.models import *


def reg(request: HttpRequest):
    print(request, "````````````````")
    try:
        payload = simplejson.loads(request.body)
        print(payload)
        name = payload['name']
        email = payload['email']
        password = payload['password']
        print(name, email, password)

        # qs:结果集（列表） [0,10]相当于limit 0，10 或者limit 10 offset 0
        qs = User.objects.filter(email=email, name=name)[0, 10]
        # all(): 查询全部
        # filter(): 过滤。返回满足条件的数据 filter(pk=10),相当于主键=10的数据
        # exclude(): 排除。排除满足条件的数据
        # order_by(): 排序
        # values(): 返回一个对象字典的列表。类似json
        # get(): 相当于selectOne() 期待返回值只有一个，否则报错
        # count(): 返回当前查询总条数
        # first(): 返回第一个对象
        # last(): 返回最后一个对象
        # exist(): 判断结果集是否存在数据，如果有返回True

        # 运算符：在filter()/exclude()/get()中使用
        # 属性__exact:严格等于，可以忽略不写
        # 属性__contains: 是否包含，大小写敏感，等价于like %XXX%
        # 属性__startswith: 以XXX开头，大小写敏感（属性__endswith: 以XXX结尾）
        # 属性__isnull: 是否为空（属性__isnotnull: 是否不为空）
        # 属性__iexact、属性__icontains、属性__istartswith、属性__endswith 忽略大小写
        # 属性__in: 是否在指定范围数据内
        # 属性__gt/gte/lt/lte: 大于/大于等于/小于/小于等于
        # 属性__year/month/day/week_day/hour/minute/second: 对日期进行处理

        # Q对象 django.db.moudels.Q,可以使用&(and)、|(or)操作符来组成逻辑表达式。~表示not
        # User.objects.filter(Q(pk__gt=1) & Q(pk__lt=10)):表示主键大于1小于10的数据

        # 打印sql
        print(qs.query)
        # 判断是否已存在该邮箱
        if qs:
            return HttpResponseBadRequest
        user = User()
        user.name = name
        user.email = email
        user.password = password
        try:
            user.save()
            # user.delete()
            return JsonResponse({'userId': user.id})
        except Exception as e:
            # 捕获到异常，往外抛
            raise
    except Exception as e:
        return HttpResponseBadRequest
