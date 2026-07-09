from flask import Flask,render_template,request,redirect,flash
from config import Config
from models import db,Record
app=Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
with app.app_context(): db.create_all()
@app.route("/")
def index(): return render_template("index.html")
@app.route("/records")
def records(): return render_template("records.html",records=Record.query.all())
@app.route("/add",methods=["GET","POST"])
def add():
    if request.method=="POST":
        n=request.form["name"];e=request.form["email"];p=request.form["phone"]
        if Record.query.filter_by(email=e).first():
            flash("Duplicate Email Found!","danger");return redirect("/add")
        db.session.add(Record(name=n,email=e,phone=p));db.session.commit()
        flash("Record Added Successfully","success");return redirect("/records")
    return render_template("add_record.html")
@app.route("/delete/<int:id>")
def delete(id):
    r=Record.query.get_or_404(id);db.session.delete(r);db.session.commit()
    flash("Record Deleted","warning");return redirect("/records")
@app.route("/search",methods=["POST"])
def search():
    k=request.form["keyword"]
    return render_template("records.html",records=Record.query.filter(Record.name.contains(k)).all())
if __name__=="__main__": app.run(debug=True)
