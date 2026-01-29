from flask import Flask,render_template,redirect,request,session
from os import path
import pymysql

tour=Flask(__name__)
conn=pymysql.connect(host="localhost",user="root",password="12345678",db="tourdb")
tour.secret_key="tour7010"
@tour.route("/",methods=["POST","GET"])
def home():
    return render_template("home121.html")




@tour.route("/chennai",methods=["GET","POST"])
def chennai():
    return render_template("chen1.html")


@tour.route("/mahabalipuram",methods=["GET","POST"])
def mahabalipuram():
    return render_template("mahabali2.html")

@tour.route("/vellore",methods=["GET","POST"])
def vellore():
    return render_template("vellore3.html")

@tour.route("/kanchipuram",methods=["GET","POST"])
def kanchipuram():
    return render_template("kanchi4.html")

@tour.route("/coimbatore",methods=["GET","POST"])
def coimbatore():
    return render_template("coimb5.html")

@tour.route("/ooty",methods=["GET","POST"])
def ooty():
    return render_template("ooty6.html")

@tour.route("/thanjavur",methods=["GET","POST"])
def thanjavur():
    return render_template("thanjavur7.html")

@tour.route("/madurai",methods=["GET","POST"])
def madurai():
    return render_template("madurai8.html")

@tour.route("/kodaikanal",methods=["GET","POST"])
def kodaikanal():
    return render_template("kodaikanal9.html")

@tour.route("/kanyakumari",methods=["GET","POST"])
def kanyakumari():
    return render_template("kanya10.html")

@tour.route("/rameswaram",methods=["GET","POST"])
def rameswaram():
    return render_template("rameswar11.html")

@tour.route("/tirunelveli",methods=["GET","POST"])
def tirunelveli():
    return render_template("tirunel12.html")




@tour.route("/cart",methods=["GET","POST"])
def cart():
    r=""
    if session:
        query=''' SELECT t.place,t.tdate,t.ttime,t.dest,t.tamount,h.hname,h.h_id,
        h.norooms,h.nodays,h.hamount,tr.total_amount,tr.tr_id FROM 
        transactions tr JOIN users u ON tr.tr_uid=u.u_id
        JOIN tour t ON tr.tr_tid=t.t_id 
        JOIN hotels h ON tr.tr_hid=h.h_id
        WHERE tr.p_status='cart' AND u.u_id='{0}'; '''.format(session['u_id'])
        cur=conn.cursor()
        cur.execute(query)
        r=cur.fetchall()
    if request.args.get("book") == "booked":
        uid = request.args.get("uid")
        place = request.args.get("place")
        men = request.args.get("men")
        women = request.args.get("women")
        kids = request.args.get("children")
        tdate = request.args.get("tdate")
        ttime = request.args.get("ttime")
        dest = request.args.get("dest")
        tamount = (800 * int(men)) + (750 * int(women)) + (500 * int(kids))
        hname = request.args.get("hname")
        hdays = request.args.get("hdays")
        hrooms = request.args.get("hrooms")
        hamount = int(hdays) * (800 * int(hrooms))
        totalamount = tamount + hamount
        cur=conn.cursor()
        query=''' INSERT INTO tour(place,tdate,ttime,dest,tamount)
         VALUES('{0}','{1}','{2}','{3}','{4}');'''.format(place,tdate,ttime,dest,tamount)
        cur.execute(query)
        conn.commit()
        tid=cur.lastrowid
        query='''  INSERT INTO hotels(hname,nodays,norooms,hamount)
        VALUES('{0}','{1}','{2}','{3}');'''.format(hname,hdays,hrooms,hamount)
        cur.execute(query)
        conn.commit()
        hid=cur.lastrowid
        query=''' INSERT INTO transactions(tr_uid,tr_tid,tr_hid,total_amount)
         VALUES('{0}','{1}','{2}','{3}');'''.format(uid,tid,hid,totalamount)
        cur.execute(query)
        conn.commit()
        return redirect("/cart")
    return render_template("cart23.html",rows=r)


@tour.route("/history",methods=["GET","POST"])
def history():
    r=""
    if session:
        cur=conn.cursor()
        query=''' SELECT t.place,t.tdate,t.ttime,t.dest,t.tamount,h.hname,h.h_id,h.norooms,h.nodays,h.hamount,
        tr.total_amount,tr.tr_id FROM transactions tr JOIN users u on tr.tr_uid=u.u_id 
        JOIN tour t on tr.tr_tid=t.t_id JOIN hotels h on tr.tr_hid=h.h_id
        WHERE tr.p_status='purchased' AND u.u_id='{0}'; '''.format(session['u_id'])
        cur.execute(query)
        r=cur.fetchall()
    if request.args.get("check") == "checked":
        ttid=request.args.get("ttid")
        query=''' UPDATE transactions SET p_status='purchased'
         WHERE tr_id='{0}'; '''.format(ttid)
        cur.execute(query)
        conn.commit()
        return redirect("/history")
    if request.args.get("remove")=="removed":
        ttid=request.args.get("ttid")
        query=''' DELETE FROM transactions WHERE tr_id='{0}'; '''.format(ttid)
        cur.execute(query)
        conn.commit()
        return redirect("/cart")
    return render_template("purchas23.html",rows=r)



@tour.route("/login",methods=["GET","POST"])
def login():
    e=""
    if request.args.get("log")=="logged":
        email=request.args.get("mail")
        pwd=request.args.get("pass")
        cur=conn.cursor()
        query=''' SELECT * FROM users WHERE email='{0}' AND pass='{1}'; 
        '''.format(email,pwd)
        cur.execute(query)
        r=cur.fetchone()
        if r:
            session["u_id"]=r[0]
            session["u_name"]=r[1]
            session["email"]=r[2]
            session["mobno"]=r[3]
            return redirect("/")
        else:
            e="Invalid email or password!..."
    return render_template("login231.html",err=e)



@tour.route("/logout",methods=["GET","POST"])
def logout():
    session.clear()
    return redirect("/")

@tour.route("/register",methods=["GET","POST"])
def register():
    e=""
    if request.args.get("reg")=="registered":
        name=request.args.get("name")
        email=request.args.get("mail")
        mobno=request.args.get("mobno")
        pwd=request.args.get("pass")
        cur=conn.cursor()
        query=''' SELECT * FROM users WHERE email='{0}'; '''.format(email)
        cur.execute(query)
        checkEmail=cur.fetchone()
        if checkEmail:
            e="Email already exists...."
        else:
            query=''' INSERT INTO users(u_name,email,mobno,pass) 
             VALUES('{0}','{1}','{2}','{3}'); '''.format(name,email,mobno,pwd)
            cur.execute(query)
            conn.commit()
            return redirect("/login")
    return render_template("register212.html",err=e)




if __name__=="__main__":
    tour.run(debug=True)