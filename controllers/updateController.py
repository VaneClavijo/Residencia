from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import null
from App import app
from flask import render_template, session, request, redirect, url_for
from App import db
from models.models import*
from flask import flash
from sqlalchemy.exc import IntegrityError

@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        ciupdate=request.form.get('ciupdate')
        owner_id=request.form.get('owner_id')
        owner_ci=request.form.get('owner_ci')
        owner_name=request.form.get('owner_name')
        owner_phone=request.form.get('owner_phone')
        Owner.query.filter_by(owner_id=owner_id).update(dict(owner_ci=owner_ci,
                                                            owner_name=owner_name,
                                                            owner_phone=owner_phone))
        db.session.commit()

        User.query.filter_by(user_ci=ciupdate).update(dict(user_ci=owner_ci))
        db.session.commit()
        flash("Se ha actualizado correctamente")
    return redirect(url_for('owner_report'))

@app.route('/update_guard', methods = ['GET', 'POST'])
def update_guard():
    if request.method == 'POST':
        ciupdate=request.form.get('ciupdate')
        owner_id=request.form.get('owner_id')
        owner_ci=request.form.get('owner_ci')
        owner_name=request.form.get('owner_name')
        owner_phone=request.form.get('owner_phone')
        fecha_contrato=request.form.get('fecha_contrato')
        Guard.query.filter_by(guard_id=owner_id).update(dict(ci=owner_ci,
                                                            name=owner_name,
                                                            phone=owner_phone,
                                                            fecha_contrato=fecha_contrato))
        db.session.commit()

        User.query.filter_by(user_ci=ciupdate).update(dict(user_ci=owner_ci))
        db.session.commit()
        flash("Se ha actualizado correctamente")
    return redirect(url_for('guard_report'))


@app.route('/update_lesse', methods = ['GET', 'POST'])
def update_lesse():
    if request.method == 'POST':
        ciupdate=request.form.get('ciupdate')
        lesse_id=request.form.get('lesse_id')
        lesse_ci=request.form.get('lesse_ci')
        lesse_name=request.form.get('lesse_name')
        lesse_phone=request.form.get('lesse_phone')
        Lesse.query.filter_by(lesse_id=lesse_id).update(dict(lesse_ci=lesse_ci,
                                                            lesse_name=lesse_name,
                                                            lesse_phone=lesse_phone))
        db.session.commit()

        User.query.filter_by(user_ci=ciupdate).update(dict(user_ci=lesse_ci))
        db.session.commit()
        flash("Se ha actualizado correctamente")
    return redirect(url_for('lesse_report'))

@app.route('/update_schedule', methods = ['GET', 'POST'])
def update_schedule():

    if request.method == 'POST':
        schedule_id=request.form['schedule_id']
        guard=request.form['guard_ci']
        location=request.form['location']
        if guard=='':
            Turnos.query.filter_by(turno_id=schedule_id).update(dict(
                                                                location=location))
            db.session.commit()
        elif location=='':
            Turnos.query.filter_by(turno_id=schedule_id).update(dict(
                                                                guardia_ci=guard))
            db.session.commit()
        elif guard!='' and location!='':
            Turnos.query.filter_by(turno_id=schedule_id).update(dict(
                                                                guardia_ci=guard,
                                                                location=location))
            db.session.commit()


        flash("Se ha actualizado correctamente")
    return redirect(url_for('schedule_report'))

@app.route('/update_house', methods = ['GET', 'POST'])
def update_house():
    if request.method == 'POST':
        house_id=request.form['house_id']
        house_number=request.form['house_number']
        house_description=request.form['house_description']
        try:
            House.query.filter_by(house_id=house_id).update(dict(
                                                                house_number=house_number,
                                                                house_description=house_description))
            db.session.commit()
            flash("Se ha actualizado correctamente")
        except IntegrityError:
            db.session.rollback()
            flash('Registro Duplicado sin guardar')


    return redirect(url_for('house_report'))