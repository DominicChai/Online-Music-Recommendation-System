from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
# Create your views here.
from django.http import HttpResponse
from .models import Choice,Question,Music,Singer,Publisher,Listener,Mark,UserSongList
from django.urls import reverse
from django.template import loader
from django.views import generic
from django.contrib import auth
from django.contrib.auth.models import User #使用的是内置的user model
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.http import JsonResponse
import numpy as np
from . import recommandation_sys
import os

#generic类
#一个polls应用中 可以创建很多的view
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]
#.as_view() 肯定是ListView这个基类的一个method

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView): #这个resultview继承了generic里的datailview这个基于类的视图
    model = Question
    template_name = 'polls/results.html'

#利用封装类就要了解基类的限制 自己定义函数就要更自由一些额、
def get_songs(request):
    music_list = []
    song_list = []

    index= None

    new_song_list=None
    seleted_song_list_name=None
    seleted_song_list=None
    selected_song_name=None
    song_query_value=None
    singer_query_value=None
    song_name=None
    singer_name=None


    # 一开始的访问不是post方法 也要自动显示歌单列表
    try:
        current_user_name = request.session['user_name']
        song_list = UserSongList.objects.filter(listener__user__username__exact=current_user_name).values('songlistname').distinct()
    except:
        return HttpResponseRedirect('http://127.0.0.1:8000/polls/login/')



    if request.method == 'POST':
        try:
            song_name= request.POST.get('song_name')
            if song_name !=None and song_name!='' : #任何字符串都会包括空字符串
                song_query_value = song_name
                music_list=Music.objects.filter(name__icontains=song_name)

        except:
            pass
        try:
            singer_name=request.POST.get('singer_name')
            if singer_name != None and singer_name != '':
                singer_query_value = singer_name
                music_list = Music.objects.filter(singer__name__icontains=singer_name)
            #Note:访问singer对象还是不够的 真正匹配的是singer对象的name属性
        except:
            pass

        if song_name==None and singer_name == None: #如果这个时候是查询 注意get方法如果没有 返回的是None对象
            selected_song_name = request.POST.get('selected_song')
        else:
            selected_song_name=None


        #创建新的歌单
        try:
            current_user_name = request.session['user_name']
            name=request.POST.get('new_song_list_name')
            current_user = Listener.objects.filter(user__username__exact=current_user_name)[0]
            song_list_name = str(current_user_name)+"'s 的"+str(name)
            new_song_list = UserSongList(songlistname=song_list_name,listener=current_user)
        except:
            pass
        if request.POST.get('new_song_list_name') is not None:
            if len(UserSongList.objects.filter(songlistname__exact=song_list_name))==0:
                new_song_list.save()

        # 获取某一个歌单的所有歌曲
        try:
            #获取歌单名
            seleted_song_list_name=request.POST.get('seleted_song_list_name')

            seleted_song_list = UserSongList.objects.filter(songlistname__exact=seleted_song_list_name)[0].music.all()
            #Note: for many to many: obj.ManyToManyaAttr.all()

            #歌单是唯一的 所以set只会返回一个歌单
        except:
            pass

    else:
        selected_song_name=None #如果是初次访问 默认什么操作都没有做


    if len(music_list)==0:
        music_list=Music.objects.all()

    return render(request, 'polls/get_songs.html', {'music_list': music_list,
                                                    'song_list':song_list,
                                                    'seleted_song_list_songs':seleted_song_list,
                                                    'song_list_selected':seleted_song_list_name,
                                                    'selected_song_id_return':selected_song_name,
                                                    'song_query_value':song_query_value,
                                                    'singer_query_value':singer_query_value,
                                                    'request_data':request.POST})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

# 用户注册
@csrf_exempt
def register(request):
    errors = []
    account = None
    password = None
    password2 = None
    email = None
    CompareFlag = False


    if request.method == 'POST':
        if not request.POST.get('account'):
            errors.append('用户名不能为空')
        else:
            account = request.POST.get('account')

        if not request.POST.get('password'):
            errors.append('密码不能为空')
        else:
            password = request.POST.get('password')
        if not request.POST.get('password2'):
            errors.append('确认密码不能为空')
        else:
            password2 = request.POST.get('password2')
        if not request.POST.get('email'):
            errors.append('邮箱不能为空')
        else:
            email = request.POST.get('email')

        if password is not None:
            if password == password2:
                CompareFlag = True
            else:
                errors.append('两次输入密码不一致')

        if account is not None and password is not None and password2 is not None and email is not None and CompareFlag :
            user = User.objects.create_user(account,email,password)
            user.save() #存入一个新的用户资料

            userlogin = auth.authenticate(username = account,password = password)
            auth.login(request,userlogin)
            return HttpResponseRedirect('/polls/login')

    return render(request,'polls/register.html', {'errors': errors})

# 用户登录
@csrf_exempt
def my_login(request):
    errors =[]
    account = None
    password = None


    if request.method == "POST":
        if not request.POST.get('account'):
            errors.append('用户名不能为空')
        else:
            account = request.POST.get('account')

        if not request.POST.get('password'):
            errors = request.POST.get('密码不能为空')
        else:
            password = request.POST.get('password')

        if account is not None and password is not None:
            user = auth.authenticate(username=account,password=password)
            if user is not None:
                if user.is_active:

                    auth.login(request,user)

                    request.session['is_login'] = True
                    request.session['user_name'] = request.POST.get('account')
                    request.session['user_password'] = request.POST.get('password')

                    return HttpResponseRedirect('/polls/login_success')
                else:
                    errors.append('用户名错误')
            else:
                errors.append('用户名或密码错误')
    return render(request,'polls/login.html', {'errors': errors})
    #context: 要传入文件中用于渲染呈现的数据, 默认是字典格式 所以errors就是传回去的错误dict

def login_success(request):
    return HttpResponseRedirect('http://127.0.0.1:8000/polls/get_songs/')
    #return render(request,'polls/login_success.html')

# 用户退出
def my_logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return HttpResponseRedirect("/polls/login")
    request.session.flush() #清除这个用户的session
    return HttpResponseRedirect('http://127.0.0.1:8000/polls/get_songs/')

def ajax_demo(request):
    return render(request, 'polls/ajax_demo.html')

def demo_add(request):
    a=request.GET['a']
    b=request.GET['b']

    if request.is_ajax():
        ajax_string = 'ajax request: '
    else:
        ajax_string = 'not ajax request: '

    c = int(a) + int(b)
    r = HttpResponse(ajax_string + str(c))
    return r

def getdata(request):
    music=str(Music.objects.all())
    return JsonResponse({'music':music,'haha':"haha I am Haahahaa"})

def addsong(request):
    song_list_name = request.GET['song_list_name']
    music_id = request.GET['music_id']
    #再次注意 返回的都是一个长度为1的set 需要把唯一的查询结果取出来
    target_music = Music.objects.filter(id__exact=music_id)[0]
    target_song_list = UserSongList.objects.filter(songlistname__exact=song_list_name)[0]
    target_song_list.music.add(target_music)
    target_song_list.save()
    return JsonResponse({'note':"add new song into list success"})
    #对于views 返回的格式必须是特定的html或jason 不可以是一个简单的字符串

def song_play(request):
    music_id = request.GET['music_id']
    music = Music.objects.filter(id__exact=music_id)[0]

    print(os.listdir('.'))
    try:
        lrc_file = open('./polls/static/polls/lyrics/'+music.lyrics, encoding='GBK')
        lyrics = ''.join(lrc_file.readlines())
    except:
        lrc_file = open('./polls/static/polls/lyrics/'+music.lyrics, encoding='utf-8')
        lyrics = ''.join(lrc_file.readlines())



    return JsonResponse({'song_file': music.audio,
                         'lyric_file': lyrics,
                         'singer': music.singer.name})

def main_page(request):
    return render(request,'polls/main_page.html')

def managesong(request):
    if request.method == 'POST':
        music_name=request.POST.get('music_nm')
        singer_name=request.POST.get('singer_name')
        publisher_name=request.POST.get('publisher_name')
        type = request.POST.get('type')
        #获取文件
        audio = request.FILES['audio']
        with open('./polls/static/polls/music/'+audio.name, 'wb+') as destination:
            for chunk in audio.chunks():
                destination.write(chunk)

        lyrics = request.FILES['lyrics']
        with open('./polls/static/polls/lyrics/'+lyrics.name, 'wb+') as destination:
            for chunk in lyrics.chunks():
                destination.write(chunk)



        singer=Singer.objects.filter(name__exact=singer_name)[0]
        publisher = Publisher.objects.filter(name__exact=publisher_name)[0]
        new_music=Music(name=music_name,singer=singer,publisher=publisher,
                        lyrics=lyrics.name,audio=audio.name,type=type)
        new_music.save()
        return render(request,'polls/managesong.html',{'music_name':music_name})

    else:
        return render(request,'polls/managesong.html')



def recommand(request):
    user_name=request.GET['user_name']
    u = Listener.objects.filter(user__username__exact=user_name)[0] #精确查找只有一个查询结果
    user_id=u.user.id

    rows=len(Listener.objects.all())
    cols=len(Music.objects.all())


    mat = np.zeros((rows, cols))  # 基础打分都是0
    print(mat)
    # print(mat.shape)
    for i in range(rows):
        for j in range(cols):
            uid=i+1
            music_id=j+1
            try:
                #给定歌曲和用户 mark 就是唯一确定的
                mat[i][j]=Mark.objects.filter(music__id__exact=music_id).filter(listener__user__id__exact=uid)[0].mark
            except:
                pass #如果没有打分 那打分就是0 不赋值了
    print(mat)
    rem_music_id,rem_user_id=(recommandation_sys.recommendation(mat, user_id))
    print("the rem result is:")
    print(rem_music_id,rem_user_id)

    if rem_music_id==None or rem_user_id==None:
        rem_music=Music.objects.order_by('-volume')[0]#选取收听量最高的 最热门的歌曲进行推荐
        rem_user_name="No User"
    else:
        rem_music=Music.objects.filter(id__exact=rem_music_id)[0]
        rem_user_name = Listener.objects.filter(user__id__exact=rem_user_id)[0].user.username



    #查询数据库 建立mark矩阵

    #推荐
    return JsonResponse({'similar_user_name':rem_user_name,
                         'recommanded_song':rem_music.name,
                         'recommanded_song_singer':rem_music.singer.name,
                         'recommanded_song_type':rem_music.type,
                         'recommanded_song_id':rem_music_id})


class Paginator(object):

    def __init__(self, object_list, per_page, orphans=0,
                 allow_empty_first_page=True):
        self.object_list = object_list
        self.per_page = int(per_page)
        self.orphans = int(orphans)
        self.allow_empty_first_page = allow_empty_first_page


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render


def splitpage(request):
    contact_list = Music.objects.all()
    paginator = Paginator(contact_list, 3)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'polls/split_page.html', {'contacts': contacts})

def mark(request):
    print("now in mark view")
    mark = request.GET['mark']
    print(mark)
    marked_song_id = request.GET['music_id']
    print(marked_song_id)
    marked_song = Music.objects.filter(id__exact=marked_song_id)[0]
    current_user_name = request.session['user_name']
    # 注意 mark里的对象是一个listener 不是一个user
    current_user = Listener.objects.filter(user__username__exact=current_user_name)[0]
    new_mark = Mark(listener=current_user, music=marked_song, mark=int(mark))
    new_mark.save()
    # note: filter查询返回的是一个查询集 所以是多元素数组 如果精确搜索只有一个的话 那么需要取查询集的第一个元素
    return JsonResponse({'note':'mark success'})

