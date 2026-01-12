from flask import Flask, request, Response
app=Flask(__name__)
@app.route('/')
def home():
    name=request.args.get('name')
    if name:
        return Response(f"<b><i>HELLO {name.upper()}</i></b>",mimetype="text/html")
    else:
        return Response("Please provide your name using ?name=yourname",mimetype="text/html")
if __name__=="__main__":
    app.run(debug=True)