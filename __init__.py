import json, datetime
from flask import Flask, render_template, request

global name
global email
global dicta

op_file = open('data.txt', 'r')
dicta = eval(op_file.read())
op_file.close()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/submitJSON1', methods=["POST"])
def processJSON1():
    global dicta
    global name
    global email
    jsonStr = request.get_json()
    jsonObj = json.loads(jsonStr)
    
    book = jsonObj['A']
    b = jsonObj['B']

    if len(book) != 0:
        count = int(b)
    result = ''
    
    if book in dicta.keys():
        dicta[book][0] += count
    elif len(book) != 0:
        dicta[book] = [count]
    
    file = open('data.txt', 'w')
    file.write(str(dicta))
    file.close()
    
    for j,k in dicta.items():
        result += j+':'+str(k[0])+'<br>'
        if len(k) == 2:
            for p,q in k[1].items():
                result += 'User '+p+' has '+str(q[0])+' piece(s) of this book.<br>'
                if len(q) == 2:
                    result += f'He has taken the book on {(q[1]).day}-{(q[1]).month}-{(q[1]).year}'
                else:
                    pass
                result += '<br><br>'
        else:
            pass
    
    return '<b>'+result

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/submitJSON2', methods = ['POST'])
def processJSON2():
    global name
    global email
    global dicta
    jsonStr = request.get_json()
    jsonObj = json.loads(jsonStr)
    name = jsonObj['A']
    email = jsonObj['B']
    if len(dicta.keys()) != 0:
        for k in dicta.values():
            if len(k) == 1:
                k.append({})
    
    file = open('data.txt', 'w')
    file.write(str(dicta))
    file.close()
    
    return 'Your name and email has been added!!!'

@app.route('/issue')
def issue():
    global dicta
    return render_template('issue.html', issue = dicta)

@app.route('/submitJSON3', methods = ['POST'])
def processJSON3():
    global name
    global email
    global dicta
    jsonStr = request.get_json()
    jsonObj = json.loads(jsonStr)
    
    a = jsonObj['A']
    b = jsonObj['B']
    c = jsonObj['C']

    response = ''
    x = datetime.datetime.now()

    for j in dicta.values():
        if name not in j[1].keys():
            for i in dicta.keys():
                dicta[i][1][name] = []
                dicta[i][1][name].append(0)

            if len(a) != 0:
                if a in dicta.keys() and dicta[a][0] != 0:
                    if dicta[a][1][name][0] == 0:
                        dicta[a][1][name][0] = 1
                        dicta[a][0] -= 1
                        dicta[a][1][name].append(x)
                        response += f'Book {a} has been issued on {x.day}-{x.month}-{x.year}<br>'
                    else:
                        response += 'You cannot take more than one piece of a book!!!'              
                else:
                    response += f'Book {a} is not present<br>'
            else:
                pass

            if len(b) != 0:
                if b in dicta.keys() and dicta[b][0] != 0:
                    if dicta[b][1][name][0] == 0:
                        dicta[b][1][name][0] = 1
                        dicta[b][0] -= 1
                        dicta[b][1][name].append(x)
                        response += f'Book {b} has been issued on {x.day}-{x.month}-{x.year}<br>'
                    else:
                        response += 'You cannot take more than one piece of a book!!!'
                else:
                    response += f'Book {b} is not present<br>'
            else:
                pass

            if len(c) != 0:
                if c in dicta.keys() and dicta[c][0] != 0:
                    if dicta[c][1][name][0] == 0:
                        dicta[c][1][name][0] = 1
                        dicta[c][0] -= 1
                        dicta[c][1][name].append(x)
                        response += f'Book {c} has been issued on {x.day}-{x.month}-{x.year}<br>'
                    else:
                        response += 'You cannot take more than one piece of a book!!!'
                else:
                    response += f'Book {c} is not present'
            else:
                pass
            break

        else:
            sum = 0
            
            for i in dicta.keys():
                sum += dicta[i][1][name][0]
            
            if sum == 3:
                response += 'You cannot take more than three books. Kindly return one or more to issue another!!!'
                break
            
            elif sum == 2:
                response += 'You can take only one book. Kindly enter the name of book to be issued in the first box.<br><br>'
                
                if len(a) != 0:
                    if a in dicta.keys() and dicta[a][0] != 0:
                        if dicta[a][1][name][0] == 0:
                            dicta[a][1][name][0] = 1
                            dicta[a][0] -= 1
                            dicta[a][1][name].append(x)
                            response += f'Book {a} has been issued on {x.day}-{x.month}-{x.year}<br>'
                        else:
                            response += 'You cannot take more than one piece of a book!!!'
                    else:
                        response += f'Book {a} is not present<br>'
                else:
                    pass

                if len(b) != 0:
                    response += 'No further books can be issued. Kindly return the books first.<br>'
                else:
                    pass

                if len(c) != 0:
                    response += 'No further books can be issued. Kindly return the books first.'
                else:
                    pass
                break

            elif sum == 1:
                response += 'You can take two books. Kindly enter the name of book(s) to be issued in the first and second box.<br><br>'
                
                if len(a) != 0:
                    if a in dicta.keys() and dicta[a][0] != 0:
                        if dicta[a][1][name][0] == 0:
                            dicta[a][1][name][0] = 1
                            dicta[a][0] -= 1
                            dicta[a][1][name].append(x)
                            response += f'Book {a} has been issued on {x.day}-{x.month}-{x.year}<br>'
                        else:
                            response += 'You cannot take more than one piece of a book!!!'
                    else:
                        response += f'Book {a} is not present<br>'
                else:
                    pass

                if len(b) != 0:
                    if b in dicta.keys() and dicta[b][0] != 0:
                        if dicta[b][1][name][0] == 0:
                            dicta[b][1][name][0] = 1
                            dicta[b][0] -= 1
                            dicta[b][1][name].append(x)
                            response += f'Book {b} has been issued on {x.day}-{x.month}-{x.year}<br>'
                        else:
                            response += 'You cannot take more than one piece of a book!!!'
                    else:
                        response += f'Book {b} is not present<br>'
                else:
                    pass

                if len(c) != 0:
                    response += 'No further books can be issued. Kindly return the books first.'
                else:
                    pass
                break

    file = open('data.txt', 'w')
    file.write(str(dicta))
    file.close()

    return '<b>'+response


@app.route('/reissue')
def reissue():
    return render_template('reissue.html')

@app.route('/submitJSON4', methods = ['POST'])
def processJSON4():
    global name
    global dicta
    global email
    jsonStr = request.get_json()
    jsonObj = json.loads(jsonStr)

    a = jsonObj['A']
    b = jsonObj['B']
    c = jsonObj['C']
    
    response = ''
    
    if name in dicta[a][1].keys() or dicta[a][1].keys() or dicta[a][1].keys():
        if len(a) != 0 :
            if dicta[a][1][name][0] == 1: 
                response += f'{a} has been reissued<br>'
            else:
                response += 'You don\'t have any book to reissue'
        else:
            pass
    else:
        response += 'You are a new user. You don\'t have any book to reissue. Please issue a book first.'

    if name in dicta[b][1].keys() or dicta[b][1].keys() or dicta[b][1].keys():
        if len(b) != 0 :
            if dicta[b][1][name][0] == 1: 
                response += f'{b} has been reissued<br>'
            else:
                response += 'You don\'t have any book to reissue'
        else:
            pass
    else:
        response += 'You are a new user. You don\'t have any book to reissue. Please issue a book first.'
    
    if name in dicta[c][1].keys() or dicta[c][1].keys() or dicta[c][1].keys():
        if len(c) != 0 :
            if dicta[c][1][name][0] == 1: 
                response += f'{c} has been reissued<br>'
            else:
                response += 'You don\'t have any book to reissue'
        else:
            pass
    else:
        response += 'You are a new user. You don\'t have any book to reissue. Please issue a book first.'

    return response

@app.route('/return')
def ret():
    return render_template('return.html')

@app.route('/submitJSON5', methods = ['POST'])
def processJSON5():
    global name
    global email
    global dicta
    jsonStr = request.get_json()
    jsonObj = json.loads(jsonStr)

    a = jsonObj['A']
    b = jsonObj['B']
    c = jsonObj['C']

    datetime_now = datetime.datetime.now() 
    
    response = ''

    if name in dicta[a][1].keys() or dicta[a][1].keys() or dicta[a][1].keys():
        if len(a) != 0:
            if a in dicta.keys():
                if dicta[a][1][name][0] == 1:
                    x = (datetime_now - dicta[a][1][name][1]).days
                    dicta[a][1][name][0] = 0
                    dicta[a][0] += 1
                    response += f'Book {a} has been returned on {datetime_now.day}-{datetime_now.month}-{datetime_now.year}<br>'
                    del dicta[a][1][name][1]

                    if x > 14:
                        response += f'Kindly pay Rs.{x*10}/- for late submission.<br>'
                    else:
                        pass
                else:
                    response += 'You don\'t have this book'
            else:
                response += 'Enter correct book<br>'
        else:
            pass
    else:
        response += 'You are a new user. You don\'t have any book to reissue. Please issue a book first.'

    
    if name in dicta[b][1].keys() or dicta[b][1].keys() or dicta[b][1].keys():
        if len(b) != 0:
            if b in dicta.keys():
                if dicta[b][1][name][0] == 1:
                    y = (datetime_now - dicta[b][1][name][1]).days
                    dicta[b][1][name][0] = 0
                    dicta[b][0] += 1
                    response += f'Book {b} has been returned on {datetime_now.day}-{datetime_now.month}-{datetime_now.year}<br>'
                    del dicta[b][1][name][1]

                    if y > 14:
                        response += f'Kindly pay Rs.{y*10}/- for late submission.<br>'
                    else:
                        pass
                else:
                    response += 'You don\'t have this book'
            else:
                response += 'Enter correct book<br>'
        else:
            pass
    else:
        response += 'You are a new user. You don\'t have any book to reissue. Please issue a book first.'

    if name in dicta[c][1].keys() or dicta[c][1].keys() or dicta[c][1].keys():
        if len(c) != 0:
            if c in dicta.keys():
                if dicta[c][1][name][0] == 1:
                    z = (datetime_now - dicta[c][1][name][1]).days
                    dicta[c][1][name][0] = 0
                    dicta[c][0] += 1
                    response += f'Book {c} has been returned on {datetime_now.day}-{datetime_now.month}-{datetime_now.year}<br>'
                    del dicta[c][1][name][1]

                    if z > 14:
                        response += f'Kindly pay Rs.{z*10}/- for late submission.<br>'
                    else:
                        pass
                else:
                    response += 'You don\'t have this book'
            else:
                response += 'Enter correct book<br>'
        else:
            pass
    else:
        response += 'You are a new user. You don\'t have any book to reissue. Please issue a book first.' 

    file = open('data.txt', 'w')
    file.write(str(dicta))
    file.close()
    
    return '<b>'+response
    
if __name__ == '__main__':
    app.run(debug = True)