from flask import Flask, request, render_template
import re
app=Flask(__name__)
@app.route("/",methods=["GET","POST"])
def index():
    matches=[]
    no_matches=False
    error=None
    if request.method=="POST":
        test_string=request.form.get("test_string")
        regex_pattern=request.form.get("regex_pattern")
        try:
            matches=re.findall(regex_pattern,test_string)
            if not matches:
                no_matches=True
        except re.error:
            error="Invalid regular expression pattern."
    return render_template("regex.html",matches=matches,no_matches=no_matches,error=error)
if __name__=="__main__":
    app.run(debug=True)      
