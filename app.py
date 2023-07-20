import json, datetime
from flask import Flask, render_template, request
import os 

global name
global email
global dicta
global sum

file_path = 'data.txt'
op_file = open(file_path, 'r')
dicta = eval(op_file.read())
op_file.close()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/submitJSON1', methods=["POST"])
def processJSON1():
    global dicta
    global name
    global email
    global sum
    jsonStr = request.get_json()
    jsonObj = json.loads(jsonStr)
    
    book = (jsonObj['A']).strip().lower()
    b = jsonObj['B']

    if len(book) != 0:
        count = int(b)
    result = ''
    
    if book in dicta.keys():
        dicta[book][0] += count
    elif len(book) != 0:
        dicta[book] = [count]
    
    file = open(file_path, 'w')
    file.write(str(dicta))
    file.close()
    
    for j,k in dicta.items():
        result += j+':'+str(k[0])+'<br>'
        if len(k) == 2:
            for p,q in k[1].items():
                result += 'User '+p+' has '+str(q[0])+' piece(s) of this book.'
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
    global sum
    jsonStr = request.get_json()
    jsonObj = json.loads(jsonStr)
    email = (jsonObj['A']).strip().lower()
    name = jsonObj['B'].strip().lower()
    response = ''
    sum = 0
    
    if len(name) != 0:    
        if len(dicta.keys()) != 0:
            for k in dicta.values():
                if len(k) == 1:
                    k.append({})
                    k[1][name] = [0]
                else:
                    if name in k[1].keys():
                        sum += k[1][name][0]
                    else:
                        k[1][name] = [0]
            response += f'Your name and email have been recorded.<br>You can take {3 - sum} books from the library.<br>'
        else:
            response += 'Sorry! No book in the library.<br>'
    else:
        response += 'Enter correct name and email<br>'
    
    file = open(file_path, 'w')
    file.write(str(dicta))
    file.close()
    
    return '<b>'+response

@app.route('/issue')
def issue():
    global dicta
    return render_template('issue.html', issue = dicta)

@app.route('/submitJSON3', methods = ['POST'])
def processJSON3():
    global name
    global email
    global dicta
    global sum
    jsonStr = request.get_json()
    jsonObj = json.loads(jsonStr)
    
    a = (jsonObj['A']).strip().lower()
    b = (jsonObj['B']).strip().lower()
    c = (jsonObj['C']).strip().lower()

    response = ''
    x = datetime.datetime.now()

    if len(a) != 0 or len(b)!= 0 or len(c)!= 0:    
        if len(name) != 0:
            if len(a) != 0:
                if sum < 3:
                    if a in dicta.keys() and dicta[a][0] != 0:
                        if dicta[a][1][name][0] == 0:
                            sum += 1
                            dicta[a][1][name][0] = 1
                            dicta[a][0] -= 1
                            dicta[a][1][name].append(x)
                            response += f'Book {a} has been issued on {x.day}-{x.month}-{x.year}<br>'
                        else:
                            response += 'You cannot take more than one piece of a book!!!<br>'              
                    else:
                        response += f'Book {a} is not present<br>'
                else:
                    response += 'You cannot take any more books.<br>'

            if len(b) != 0:
                if sum < 3 :
                    if b in dicta.keys() and dicta[b][0] != 0:
                        if dicta[b][1][name][0] == 0:
                            sum += 1
                            dicta[b][1][name][0] = 1
                            dicta[b][0] -= 1
                            dicta[b][1][name].append(x)
                            response += f'Book {b} has been issued on {x.day}-{x.month}-{x.year}<br>'
                        else:
                            response += 'You cannot take more than one piece of a book!!!<br>'
                    else:
                        response += f'Book {b} is not present<br>'
                else:
                    response += 'You cannot take any more books.<br>'
            
            if len(c) != 0:
                if sum < 3 :
                    if c in dicta.keys() and dicta[c][0] != 0:
                        if dicta[c][1][name][0] == 0:
                            sum += 1
                            dicta[c][1][name][0] = 1
                            dicta[c][0] -= 1
                            dicta[c][1][name].append(x)
                            response += f'Book {c} has been issued on {x.day}-{x.month}-{x.year}<br>'
                        else:
                            response += 'You cannot take more than one piece of a book!!!'
                    else:
                        response += f'Book {c} is not present'
                else:
                    response += 'You cannot take any more books.<br>'
        else:
            response += 'You didn\'t enter correct name in the previous page.'
    else:
        response += 'Please fill the required fields!!!'

    file = open(file_path, 'w')
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
    global sum
    jsonStr = request.get_json()
    jsonObj = json.loads(jsonStr)

    a = (jsonObj['A']).strip().lower()
    b = (jsonObj['B']).strip().lower()
    c = (jsonObj['C']).strip().lower()
    datetime_now = datetime.datetime.now()
    
    response = ''
    
    if len(a) != 0 or len(b) != 0 or len (c) != 0:   
        if len(name) != 0:
            if name in dicta[a][1].keys() or dicta[b][1].keys() or dicta[c][1].keys():
                if len(a) != 0 :
                    if dicta[a][1][name][0] == 1:
                        dicta[a][1][name][1] = datetime.datetime.now()
                        response += f'{a} has been reissued on {datetime_now.day}-{datetime_now.month}-{datetime_now.year}<br>'
                    else:
                        response += 'You don\'t have this book to reissue<br>'
                else:
                    pass
            else:
                response += 'You don\'t have these books. Please issue the books first.<br>'
                return response
        else:
            response += 'You didn\'t enter correct name in the previous page.'

        if len(name) != 0:
            if name in dicta[a][1].keys() or dicta[b][1].keys() or dicta[c][1].keys():
                if len(b) != 0 :
                    if dicta[b][1][name][0] == 1:
                        dicta[b][1][name][1] = datetime.datetime.now()
                        response += f'{b} has been reissued on {datetime_now.day}-{datetime_now.month}-{datetime_now.year}<br>'
                    else:
                        response += 'You don\'t have this book to reissue<br>'
                else:
                    pass
            else:
                response += 'You don\'t have these books. Please issue the books first.<br>'
                return response
        else:
            response += 'You didn\'t enter correct name in the previous page.'
            
        if len(name) != 0:    
            if name in dicta[a][1].keys() or dicta[b][1].keys() or dicta[c][1].keys():
                if len(c) != 0 :
                    if dicta[c][1][name][0] == 1:
                        dicta[c][1][name][1] = datetime.datetime.now()
                        response += f'{c} has been reissued on {datetime_now.day}-{datetime_now.month}-{datetime_now.year}<br>'
                    else:
                        response += 'You don\'t have this book to reissue<br>'
                else:
                    pass
            else:
                response += 'You don\'t have these books. Please issue the books first.<br>'
                return response
        else:
            response += 'You didn\'t enter correct name in the previous page.'
    else:
        response += 'Please fill the required fields!!!'

    file = open(file_path, 'w')
    file.write(str(dicta))
    file.close()

    return '<b>'+response

@app.route('/return')
def ret():
    return render_template('return.html')

@app.route('/submitJSON5', methods = ['POST'])
def processJSON5():
    global name
    global email
    global dicta
    global sum
    jsonStr = request.get_json()
    jsonObj = json.loads(jsonStr)

    a = (jsonObj['A']).strip().lower()
    b = (jsonObj['B']).strip().lower()
    c = (jsonObj['C']).strip().lower()
    datetime_now = datetime.datetime.now() 
    
    response = ''

    if len(a) != 0 or len(b) != 0 or len (c) != 0:    
        if len(name) != 0:    
            if name in dicta[a][1].keys() or dicta[b][1].keys() or dicta[c][1].keys():
                if len(a) != 0:
                    if a in dicta.keys():
                        if dicta[a][1][name][0] == 1:
                            x = (datetime_now - dicta[a][1][name][1]).days
                            dicta[a][1][name][0] = 0
                            dicta[a][0] += 1
                            response += f'Book {a} has been returned on {datetime_now.day}-{datetime_now.month}-{datetime_now.year}<br>'
                            del dicta[a][1][name][1]

                            if x > 14:
                                response += f'Kindly pay Rs.{(x-14)*50}/- for late submission.<br>'
                            else:
                                pass
                        else:
                            response += 'You don\'t have this book<br>'
                    else:
                        response += 'Enter correct book<br>'
                else:
                    pass
            else:
                response += 'You haven\'t issued these books<br>'
                return response
        else:
            response += 'You didn\'t enter correct name in the previous page.'

            
        if len(name) != 0:    
            if name in dicta[a][1].keys() or dicta[b][1].keys() or dicta[c][1].keys():
                if len(b) != 0:
                    if b in dicta.keys():
                        if dicta[b][1][name][0] == 1:
                            y = (datetime_now - dicta[b][1][name][1]).days
                            dicta[b][1][name][0] = 0
                            dicta[b][0] += 1
                            response += f'Book {b} has been returned on {datetime_now.day}-{datetime_now.month}-{datetime_now.year}<br>'
                            del dicta[b][1][name][1]

                            if y > 14:
                                response += f'Kindly pay Rs.{(y-14)*50}/- for late submission.<br>'
                            else:
                                pass
                        else:
                            response += 'You don\'t have this book<br>'
                    else:
                        response += 'Enter correct book<br>'
                else:
                    pass
            else:
                response += 'You haven\'t issued these books<br>'
                return response
        else:
            response += 'You didn\'t enter correct name in the previous page.'

        if len(name) != 0:   
            if name in dicta[a][1].keys() or dicta[b][1].keys() or dicta[c][1].keys():
                if len(c) != 0:
                    if c in dicta.keys():
                        if dicta[c][1][name][0] == 1:
                            z = (datetime_now - dicta[c][1][name][1]).days
                            dicta[c][1][name][0] = 0
                            dicta[c][0] += 1
                            response += f'Book {c} has been returned on {datetime_now.day}-{datetime_now.month}-{datetime_now.year}<br>'
                            del dicta[c][1][name][1]

                            if z > 14:
                                response += f'Kindly pay Rs.{(z-14)*50}/- for late submission.<br>'
                            else:
                                pass
                        else:
                            response += 'You don\'t have this book<br>'
                    else:
                        response += 'Enter correct book<br>'
                else:
                    pass
            else:
                response += 'You haven\'t issued these books<br>'
                return response
        else:
            response += 'You didn\'t enter correct name in the previous page.'
    else:
        response += 'Please fill the required fields!!!'

    file = open(file_path, 'w')
    file.write(str(dicta))
    file.close()
    
    return '<b>'+response
    
if __name__ == '__main__':
    app.run(debug = True)
