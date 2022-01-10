from sqlalchemy.sql.elements import Null
from App import app
from flask import render_template, session, request, redirect, url_for
from App import db
from models.models import*
import datetime
from werkzeug.security import generate_password_hash
from sqlalchemy import or_
from flask import flash
from sqlalchemy.exc import IntegrityError
from datetime import datetime

import time
from twilio.rest import Client

send_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


@app.route('/add_exit_time', methods=['POST', 'GET'])
def add_exit_time():
    casasn=dict()
    busqueda=[]
    casas=House.query.filter().all()
    filteredAnswer = Visit.query.filter(Visit.exit_time==None, Visit.visit_state!='RECHAZADO').all()
    filteredAnswerC = Visit.query.filter(or_(Visit.exit_time!=None, Visit.visit_state=='RECHAZADO')).all()
    for num in casas:
        casasn[num.house_id]=num.house_number
    for con in filteredAnswer:
        answerAdd=dict(id = con.visitor_ci,
        visit_id=con.visit_id,
        visitor_name = con.visitor_name,
        visit_type=con.visit_type,
        visit_car=con.visit_car,
        entrance_time=con.entrance_time,
        visit_state=con.visit_state,
        house_number=casasn[con.house_number])
        busqueda.append(answerAdd)
    if request.method == 'POST':
        id=request.form['idin']
        date=request.form[id]
        edate=request.form['entry']
        if(edate>=date):
            flash('La hora de entrada no puede ser mayor que la de salida')
        else:
            Visit.query.filter_by(visit_id=id).update(dict(exit_time=date))
            db.session.commit()
            flash('Registro guardado con éxito')
        return redirect(url_for('add_exit_time'))
    return render_template('addExitTime.html',filteredAnswer=filteredAnswer,filteredAnswerC=filteredAnswerC,casasn=casasn)


@app.route('/add_guard', methods=['POST', 'GET'])
def add_guard():
    users1=[]
    guardsCI=[]
    users=User.query.filter().all()
    guards=[]
    for u in users:
        users1.append(u.user_ci)
    for g in guards:
        guardsCI.append(g.ci)
    if request.method=='POST':
        guards=Guard.query.filter().all()
        fullname=request.form['guard_name']
        ci=request.form['guard_ci']
        phone=request.form['guard_phone']
        fecha_contrato=request.form['fecha_contrato']
        registro=Guard(ci=ci,name=fullname,phone=phone,fecha_contrato=fecha_contrato)
        password=generate_password_hash(ci, method='sha256')
        registroU=User(user_ci=ci,
                        user_type='G',
                        user_name=fullname,
                        password_hash=password)
        try:
            db.session.add(registro)
            db.session.commit()
            flash('Registro guardado con éxito!')
        except IntegrityError:
            db.session.rollback()
            # Don't stop the stream, just ignore the duplicate.
            flash('Registro Duplicado sin guardar')
        if ci not in users1:
            db.session.add(registroU)
            db.session.commit()
    return render_template('addGuard.html', msg='')


@app.route('/add_house', methods=['POST', 'GET'])
def add_house():
    casasn=[]
    casas=House.query.filter().all()
    for num in casas:
        casasn.append(str(num.house_number))
    if request.method=='POST':
        house_Number=request.form['house_id']
        house_description=request.form['house_description']
        registro=House(house_number=house_Number,
                        house_description=house_description,)
        try:
            db.session.add(registro)
            db.session.commit()
            flash('Registro guardado con éxito!')
        except IntegrityError:
            db.session.rollback()
            flash('Registro Duplicado sin guardar')

    return render_template('addHouse.html', casasn=casasn)

@app.route('/add_lesse', methods=['POST', 'GET'])
def add_lesse():
    casasn=[]
    users1=[]
    if session.get('id'):
        casas=House.query.filter(House.owner_ci==session["id"]).all()
        for num in casas:
            if num.lesse_ci=='':
                casasn.append((num.house_id,str(num.house_number)))
        users=User.query.filter().all()
        for u in users:
            users1.append(u.user_ci)
        if request.method=='POST':
            house_Number=request.form['house_id']
            lesse_ci=request.form['lesse_ci']
            lesse_name=request.form['lesse_name']
            lesse_phone=request.form['lesse_phone']
            fecha_contrato=request.form['fecha_contrato']
            registro=Lesse(house_number=house_Number,
                            lesse_ci=lesse_ci,
                            lesse_name=lesse_name,
                            lesse_phone=lesse_phone,
                            start_date=fecha_contrato)
            password=generate_password_hash(lesse_ci, method='sha256')
            registroU=User(user_ci=lesse_ci,
                            user_type='L',
                            user_name=lesse_name,
                            password_hash=password)
            db.session.query(Lesse).filter(Lesse.lesse_state=='ACTIVO', Lesse.house_number==house_Number).update(dict(lesse_state='ELIMINADO',end_date=datetime.today().strftime('%Y-%m-%d')))
            db.session.commit()
            try:
                db.session.add(registro)
                db.session.commit()
                flash('Registro guardado con éxito!')
            except IntegrityError:
                db.session.rollback()
                flash('Registro duplicado, sin guardar')
            if lesse_ci not in users1:
                db.session.add(registroU)
                db.session.commit()
            House.query.filter_by(house_id=house_Number).update(dict(lesse_ci=lesse_ci))
            db.session.commit()
    else:
        flash('Debe iniciar sesion')
    return render_template('addLesse.html', casasn=casasn)


@app.route('/add_owner', methods=['POST', 'GET'])
def add_owner():
    casasn=[]
    casas=House.query.filter(House.owner_ci=='').all()
    for num in casas:
        casasn.append((num.house_id,str(num.house_number)))
    users1=[]
    users=User.query.filter().all()
    for u in users:
        users1.append(u.user_ci)
    if request.method=='POST':
        house_Number=request.form['house_number']
        owner_ci=request.form['owner_ci']
        owner_name=request.form['owner_name']
        owner_phone=request.form['owner_phone']
        registro=Owner(house_number=house_Number,
                        owner_ci=owner_ci,
                        owner_name=owner_name,
                        owner_phone=owner_phone)
        password=generate_password_hash(owner_ci, method='sha256')
        registroU=User(user_ci=owner_ci,
                        user_type='O',
                        user_name=owner_name,
                        password_hash=password)
        try:
            db.session.add(registro)
            db.session.commit()
            flash('Registro guardado con éxito!')
        except IntegrityError:
            db.session.rollback()
            # Don't stop the stream, just ignore the duplicate.
            flash('Registro Duplicado sin guardar')
        if owner_ci not in users1:
            db.session.add(registroU)
            db.session.commit()
        House.query.filter_by(house_id=house_Number).update(dict(owner_ci=owner_ci))
        db.session.commit()
    return render_template('addowner.html', casasn=casasn)

@app.route('/add_schedule', methods=['POST', 'GET'])
def add_schedule():
    msg=''
    guards=[]
    guards1=Guard.query.filter(Guard.guard_state=='ACTIVO').all()
    guardsS=dict()
    ls=Location.query.filter().all()
    locations=[]
    for g in guards1:
        guards.append(g.ci)
    for gl in guards1:
        guardsS[gl.guard_id]=(gl.ci+'-'+gl.name)
    for l in ls:
        locations.append((l.location_id,l.location_name))
    if request.method=='POST':
        guardia_ci=request.form['guard_ci']
        entry_time=request.form['entry_time']
        out_time=request.form['out_time']
        location=request.form['local']
        registro=Turnos(guardia_ci=guardia_ci,
                        entry_time=entry_time,
                        out_time=out_time,
                        location=location,
                        state='ACTIVO')
        if(entry_time>=out_time):
            flash('No se guardó. La hora de entrada no puede ser mayor que la de salida')
        else:
            try:
                db.session.add(registro)
                db.session.commit()
                flash('Registro guardado con éxito!')
            except IntegrityError:
                db.session.rollback()
                flash('Registro Duplicado sin guardar')
    return render_template('addSchedule.html',msg=msg,guardsS=guardsS,locations=locations)

@app.route('/add_visit', methods=['POST', 'GET'])
def add_visit():
    validacion=Null
    casasn=[]

    casas=House.query.filter().all()
    entrance_time=datetime.now()
    formato1 = "%a %d %b %Y %H:%M"
    for num in casas:
        c=''
        if num.owner_ci=='' and num.lesse_ci=='':
            c=str(num.house_number)+' - '+'No tiene habitantes'
        elif num.lesse_ci!='':
            l=Lesse.query.filter(Lesse.lesse_ci==num.lesse_ci).first()
            c=str(num.house_number)+' - '+l.lesse_name
        elif num.owner_ci!='' and num.lesse_ci=='':
            o=Owner.query.filter(Owner.owner_ci==num.owner_ci).first()
            c=str(num.house_number)+' - '+o.owner_name
        casasn.append((num.house_id,c))
    if request.method=='POST':
        visitor_ci=request.form['visitor_ci']
        visitor_name=request.form['visitor_name']
        visit_type=request.form['visit_type']
        house_id=request.form['house_id']
        if request.form['visit_type']=='Vehiculo':
            visit_car=request.form['car']
        else:
            visit_car=''
        print(house_id)
        casaV=House.query.filter(House.house_id==house_id).first()
        registro=Visit(visitor_ci=visitor_ci,
                        visitor_name=visitor_name,
                        entrance_time=entrance_time,
                        house_number=house_id,
                        visit_type=visit_type,
                        visit_car=visit_car,
                        guard_name=session['id']+'-'+session['username'])
        if casaV.lesse_ci=='':
            responsable=Owner.query.filter(Owner.owner_ci==casaV.owner_ci, Owner.owner_state=='ACTIVO' ).first()
            phone='+593'+responsable.owner_phone
        else:
            responsable=Lesse.query.filter(Lesse.lesse_ci==casaV.lesse_ci,Lesse.lesse_state=='ACTIVO').first()
            phone='+593'+responsable.lesse_phone
        try:
            db.session.add(registro)
            db.session.commit()
            flash('Registro guardado con éxito!')
            account_sid = 'ACf6d804e9068adea41d79a70fb367ad9b'
            auth_token = 'a6e9c185119c098acaf5efaa3ea78bc5'
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                to=phone,
                from_="+14405306899",
                body="NUEVA VISITA-Autorizar en APP:\nVisitante: "+
                    visitor_name+
                    "\nHora: "+str(entrance_time)+
                    "\nGuardia: "+session['id']+'-'+session['username'])
        except IntegrityError:
            db.session.rollback()
            flash('Registro Duplicado sin guardar')
    return render_template('addVisit.html', message=validacion, datetime=entrance_time.strftime(formato1),casasn=casasn)








