from django.shortcuts import render, HttpResponse, redirect
import random
from django.views.decorators.csrf import csrf_exempt

nextID = 4
topics = [
{'id':1, 'title':'routing', 'body':'Rounting is ...'},
{'id':2, 'title':'view', 'body':'View is ...'},
{'id':3, 'title':'Model', 'body':'Model is ...'}
]

def HTMTemplate(articletag, id=None):
    global topics
    contextUI=''
    if id != None:
        contextUI = f'''
                <li>
                    <form action="/delete/" method="post">
                        <input type='hidden' name="id" value={id}>
                        <input type="submit" value = "delete">
                    </from>
                </li>
                <li><a href="/update/{id}">update</a></li>
        '''
    
    ol = ''
    for topic in topics:
        ol += f'<li><a href = "/read/{topic["id"]}">{topic['title']}</a></li>'
    return f'''
        <html>
        <body>
            <h1><a href='/'>Django</a></h1>
            <ul>
                {ol}
            </ul>
            {articletag}
            <ul>
                <li><a href="/create/">create</a></li>
                {contextUI}
            </ul>
        </body>
        </html>
        '''
    


def index(request):
    article = '''
        <h2>Welcome</h2>
        Hello, Django
    '''
    return HttpResponse(HTMTemplate(article))

def read(request, id):
    global topics
    article = ''
    for topic in topics:
        if topic['id'] == int(id):
            article = f'<h2>{topic['title']}</h2>{topic["body"]}'
    return HttpResponse(HTMTemplate(article, id))

@csrf_exempt
def create(request):
    global nextID
    if request.method == "GET":
        article = '''
        <form action="/create/" method="post">
            <p><input type = "text" name = "title" placeholder = "title"></p>
            <p><textarea name = "body" placeholder = "body"></textarea></p>
            <p><input type = "submit"></p>
        </form>
        '''
        return HttpResponse(HTMTemplate(article))

    elif request.method == "POST":
        title = request.POST['title']
        body = request.POST['body']
        newTopic = {"id":nextID, 'title':title, 'body':body}
        topics.append(newTopic)
        url = '/read/' + str(nextID)
        nextID = nextID + 1
        return redirect(url)

@csrf_exempt
def delete(request):
    global topics
    if request.method == 'POST':
        id = request.POST['id']
        newTopics = []
        for topic in topics:
            if topic['id'] != int(id):
                newTopics.append(topic)
        topics = newTopics
        return redirect('/')    
    
@csrf_exempt
def update(request, id):
    global topics
    if request.method == 'GET':
        for topic in topics:
            if topic['id'] == int(id):
                selectedTopic = {
                    "title":topic["title"],
                    "body":topic["body"]
                }
        article = f'''
        <form action="/update/{id}/" method="post">
            <p><input type = "text" name = "title" placeholder = "title" value={selectedTopic["title"]}></p>
            <p><textarea name = "body" placeholder = "body">{selectedTopic["body"]}</textarea></p>
            <p><input type = "submit"></p>
        </form>
        '''
        return HttpResponse(HTMTemplate(article, id))
    elif request.method == 'POST':
        title = request.POST["title"]
        body = request.POST["body"]
        for topic in topics:
            if topic['id'] == int(id):
                topic["tutle"] = title
                topic["body"] = body
        return redirect(f'/read/{id}')