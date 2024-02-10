from flask import Flask , request , jsonify ,render_template
import os
import markupsafe
app = Flask(__name__)


def fetchFiles(file_name,start,end):
    result = ""
  
    with open(f'./static/{file_name}.txt','r' ,encoding='ascii',errors="ignore" ) as f:
        file_lines= f.readlines()
        if(end>len(file_lines)):
            end=len(file_lines)
        for line in file_lines[start:end]:
            result+=line
    return result
    
    

@app.route('/file-content/<file_name>')
def home_page(file_name):
    files_in_static = os.listdir('./static/')
    if(not file_name+'.txt' in files_in_static ):
        print(file_name+'.txt' +'does not exist!')
        return jsonify({
            'msg':"file does'nt Exists !"
        })
    print(file_name+'.txt exists')
    if(request.args.get('start')==None or request.args.get('end')==None):
       return  jsonify({
           'msg':'query params were not present !'
       })
    if(not str.isdigit(request.args.get('start')) or not str.isdigit(request.args.get('end'))):
        return jsonify({
            'msg':'query params should be a Digit'
        })
    start_line = int(request.args.get('start'))
    end_line = int(request.args.get('end'))
    if(start_line>end_line):
        return jsonify({
            'msg':'start line is greater than end line'
        })
    if(start_line<0):
        return jsonify({
            'msg':'invalid query params'
        })    
    response = fetchFiles(file_name,start_line,end_line)
    return render_template('index.html',data=response)   

app.run(debug=True)