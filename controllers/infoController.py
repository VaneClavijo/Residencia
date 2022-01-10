from App import app
from flask import render_template, session, request, redirect, url_for
from App import db
from models.models import*
from flask import flash
from datetime import datetime
import time


@app.route('/lesse_report', methods=['POST', 'GET'])
def lesse_report():
    busqueda=[]
    busquedaE=[]
    lesses=[]
    l=[]
    casasn=dict()
    if 'id' in session.keys():
        casas=House.query.filter(House.owner_ci==session["id"]).all()
    else:
        casas=[]
    for num in casas:
        casasn[num.house_id]=(num.house_number)
    lesses=Lesse.query.filter().all()
    for l in lesses:
        if l.house_number in casasn.keys()and l.lesse_state=='ACTIVO':
            busqueda.append((l.lesse_id,
                            l.lesse_ci,
                            l.lesse_name,
                            l.lesse_phone,
                            l.start_date,
                            casasn[l.house_number],
                            l.house_number))
        if l.house_number in casasn.keys() and l.lesse_state=='ELIMINADO':
            busquedaE.append((l.lesse_id,
                            l.lesse_ci,
                            l.lesse_name,
                            l.lesse_phone,
                            l.start_date,
                            casasn[l.house_number],
                            l.end_date,
                            l.house_number))
    if request.method == 'POST':
        id=request.form['idin']
        ci=request.form['delci']
        delHo=request.form['delHo']
        db.session.query(House).filter(House.house_id==delHo).update(dict(lesse_ci=''))
        db.session.commit()
        db.session.query(Lesse).filter(Lesse.lesse_id==id).update(dict(lesse_state='ELIMINADO',end_date=datetime.today().strftime('%Y-%m-%d')))
        db.session.commit()
        db.session.query(User).filter(User.user_ci==ci).delete(synchronize_session=False)
        db.session.commit()
        flash('Registro borrado con éxito')
        return redirect(url_for('lesse_report'))
    return render_template('reportLesse.html', busqueda = busqueda,busquedaE=busquedaE)

@app.route('/guard_report', methods=['POST', 'GET'])
def guard_report():
    busqueda=[]
    busquedaE=[]
    filteredAnswer = Guard.query.filter().all()
    for con in filteredAnswer:
        if con.guard_state=='ACTIVO':
            busqueda.append((con.guard_id,
                            con.ci,
                            con.name,
                            con.phone,
                            con.fecha_contrato))
        elif con.guard_state=='ELIMINADO':
            busquedaE.append((con.guard_id,
                            con.ci,
                            con.name,
                            con.phone,
                            con.fecha_contrato))
    if request.method == 'POST':
        id=request.form['idin']
        ci=request.form['delci']
        db.session.query(Guard).filter(Guard.guard_id==id).update(dict(guard_state='ELIMINADO'))
        db.session.commit()
        db.session.query(User).filter(User.user_ci==ci).delete(synchronize_session=False)
        db.session.commit()
        flash('Registro borrado con éxito')
        return redirect(url_for('guard_report'))
    return render_template('reportGuard.html', busqueda = busqueda,busquedaE=busquedaE)


@app.route('/house_report', methods=['POST', 'GET'])
def house_report():
    owners1=Owner.query.filter().all()
    owners=dict()
    lesses1=Lesse.query.filter().all()
    lesses=dict()
    for o in owners1:
        owners[o.owner_ci]=o.owner_name
    for l in lesses1:
        lesses[l.lesse_ci]=l.lesse_name
    filteredAnswer = House.query.filter().all()

    if request.method == 'POST':
        id=request.form['idin']
        db.session.query(Turnos).filter(Turnos.turno_id==id).delete(synchronize_session=False)
        db.session.commit()

        flash('Registro borrado con éxito')
    return render_template('reportHouse.html', filteredAnswer = filteredAnswer,owners=owners,lesses=lesses)

@app.route('/owner_report', methods=['POST', 'GET'])
def owner_report():
    busqueda=[]
    busquedaE=[]
    casasn1=dict()
    casas=House.query.filter().all()
    for num in casas:
        casasn1[num.house_id]=(num.house_number,num.house_description)
    filteredAnswer = Owner.query.filter().all()
    for con in filteredAnswer:
        if con.owner_state=='ACTIVO':
            busqueda.append((con.owner_id,
                            con.owner_ci,
                            con.owner_name,
                            con.owner_phone,
                            con.house_number,
                            casasn1[con.house_number][0],
                            casasn1[con.house_number][1]))
        elif con.owner_state=='ELIMINADO':
            busquedaE.append((con.owner_id,
                            con.owner_ci,
                            con.owner_name,
                            con.owner_phone,
                            con.house_number,
                            casasn1[con.house_number][0],
                            casasn1[con.house_number][1]))


    if request.method == 'POST':
        id=request.form['idin']
        houseid=request.form['entry']
        ci=request.form['delci']
        db.session.query(Owner).filter(Owner.owner_id==id).update(dict(owner_state='ELIMINADO'))
        db.session.commit()
        db.session.query(User).filter(User.user_ci==ci).delete(synchronize_session=False)
        db.session.commit()
        House.query.filter_by(house_id=houseid).update(dict(owner_ci=''))
        db.session.commit()
        flash('Registro borrado con éxito')
        return redirect(url_for('owner_report'))
    return render_template('reportOwner.html', busqueda = busqueda,casasn=casasn1,busquedaE=busquedaE)


@app.route('/schedule_report', methods=['POST', 'GET'])
def schedule_report():
    guards1=Guard.query.filter(Guard.guard_state=='ACTIVO').all()
    guardsS=dict()
    for gl in guards1:
        guardsS[gl.guard_id]=(gl.ci+'-'+gl.name)
    l1=dict()
    locations=Location.query.filter().all()
    for l in locations:
        l1[l.location_id]=l.location_name

    filteredAnswerA=Turnos.query.filter().all()
    for f in filteredAnswerA:
        if f.out_time<datetime.now():
            db.session.query(Turnos).filter(Turnos.turno_id==f.turno_id).update(dict(state='FINALIZADO'))
            db.session.commit()
    filteredAnswer = Turnos.query.filter(Turnos.state=='ACTIVO').all()
    filteredAnswerF = Turnos.query.filter(Turnos.state=='FINALIZADO').all()
    if request.method == 'POST':
        id=request.form['idin']
        db.session.query(Turnos).filter(Turnos.turno_id==id).delete(synchronize_session=False)
        db.session.commit()
        '''db.session.query(Turnos).filter(Turnos.turno_id==id).update(dict(state='ELIMINADO'))
        db.session.commit()'''
        flash('Registro borrado con éxito')
        return redirect(url_for('schedule_report'))
    return render_template('reportSchedules.html', busqueda = filteredAnswer,guardsS=guardsS,locations=locations,l1=l1,guards1=guards1,filteredAnswerF=filteredAnswerF)

@app.route('/visits_report', methods=['POST', 'GET'])
def visits_report():
    busqueda=[]
    busquedaA=[]
    b=[]
    casasn=dict()
    casas=House.query.filter().all()
    filtro=Visit.query.filter().all()
    for num in casas:
        casasn[num.house_id]=(num.house_number)
    if session["type"] in ['A','G']:
        for f in filtro:
            if f.visit_state=='ESPERA':
                    busqueda.append((casasn[f.house_number],
                                f.visitor_ci,
                                f.visitor_name,
                                f.visit_type,
                                f.visit_car,
                                f.entrance_time,
                                f.exit_time,
                                f.visit_state,
                                f.visit_id,
                                f.guard_name))
            elif f.visit_state=='ACEPTADO' or f.visit_state=='RECHAZADO' :
                busquedaA.append((casasn[f.house_number],
                            f.visitor_ci,
                            f.visitor_name,
                            f.visit_type,
                            f.visit_car,
                            f.entrance_time,
                            f.exit_time,
                            f.visit_state,
                            f.visit_id,
                            f.guard_name))
    elif session["type"] in['O']:
        owners= Owner.query.filter(Owner.owner_ci==session["id"])
        casasO=[]
        casas=House.query.filter_by().all()
        c=dict()
        for o in owners:
            casasO.append(o.house_number)
        for ca in casas:
            c[ca.house_id]=ca.lesse_ci
        for f in filtro:
            if f.house_number in casasO and c[f.house_number]=='':
                if f.visit_state=='ESPERA':
                    busqueda.append((casasn[f.house_number],
                                f.visitor_ci,
                                f.visitor_name,
                                f.visit_type,
                                f.visit_car,
                                f.entrance_time,
                                f.exit_time,
                                f.visit_state,
                                f.visit_id,
                                f.guard_name))
                elif f.visit_state=='ACEPTADO' or f.visit_state=='RECHAZADO' :
                    busquedaA.append((casasn[f.house_number],
                                f.visitor_ci,
                                f.visitor_name,
                                f.visit_type,
                                f.visit_car,
                                f.entrance_time,
                                f.exit_time,
                                f.visit_state,
                                f.visit_id,
                                f.guard_name))

    elif session["type"] in['L']:
        leesses= Lesse.query.filter(Lesse.lesse_ci==session["id"])
        casasO=[]
        for l in leesses:
            casasO.append(l.house_number)
        for f in filtro:
            if f.house_number in casasO:
                if f.visit_state=='ESPERA':
                    busqueda.append((casasn[f.house_number],
                                f.visitor_ci,
                                f.visitor_name,
                                f.visit_type,
                                f.visit_car,
                                f.entrance_time,
                                f.exit_time,
                                f.visit_state,
                                f.visit_id,
                                f.guard_name))
                elif f.visit_state=='ACEPTADO' or f.visit_state=='RECHAZADO':
                    busquedaA.append((casasn[f.house_number],
                                f.visitor_ci,
                                f.visitor_name,
                                f.visit_type,
                                f.visit_car,
                                f.entrance_time,
                                f.exit_time,
                                f.visit_state,
                                f.visit_id,
                                f.guard_name))

    return render_template('reportVisits.html', busqueda = busqueda,busquedaA=busquedaA)


@app.route('/accept_visit', methods=['POST', 'GET'])
def accept_visit():
     if request.method == 'POST':
        id=request.form['visit_id']
        Visit.query.filter_by(visit_id=id).update(dict(visit_state='ACEPTADO'))
        db.session.commit()
        return redirect(url_for('visits_report'))

@app.route('/reject_visit', methods=['POST', 'GET'])
def reject_visit():
    if request.method == 'POST':
        id=request.form['visit_id']
        Visit.query.filter_by(visit_id=id).update(dict(visit_state='RECHAZADO'))
        db.session.commit()
        return redirect(url_for('visits_report'))