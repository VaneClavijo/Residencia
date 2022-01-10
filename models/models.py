from App import db

class User(db.Model):
    user_id=db.Column(db.Integer, primary_key=True,autoincrement=True,unique=True)
    user_ci=db.Column(db.String(10),unique=True)
    user_name=db.Column(db.String(100),nullable=False)
    user_type=db.Column(db.String(1))
    password_hash = db.Column(db.String(200))
    def __init__(self,user_ci,user_name,password_hash,user_type ):
        self.user_ci=user_ci
        self.user_name=user_name
        self.password_hash=password_hash
        self.user_type=user_type

class Guard(db.Model):
    __tablename__='guard'
    guard_id= db.Column(db.Integer, primary_key=True,autoincrement=True)
    ci=db.Column(db.String(13),nullable=False, unique=True)
    name= db.Column(db.String(100),nullable=False)
    phone=db.Column(db.String(10),nullable=False)
    fecha_contrato=db.Column(db.Date,nullable=False)
    guard_state=db.Column(db.String(10))
    def __init__(self,ci,name,phone,fecha_contrato):
        self.ci=ci
        self.name=name
        self.phone=phone
        self.fecha_contrato=fecha_contrato
        self.guard_state='ACTIVO'

class Owner(db.Model):
    __tablename__='owner'
    owner_id= db.Column(db.Integer, primary_key=True,autoincrement=True,unique=True)
    house_number=db.Column(db.Integer, nullable=False)
    owner_ci=db.Column(db.String(13),nullable=False)
    owner_name= db.Column(db.String(100),nullable=False)
    owner_phone=db.Column(db.String(10),nullable=False)
    owner_state=db.Column(db.String(10))
    def __init__(self,house_number,owner_ci,owner_name,owner_phone ):
        self.house_number=house_number
        self.owner_ci=owner_ci
        self.owner_name=owner_name
        self.owner_phone=owner_phone
        self.owner_state='ACTIVO'


class Lesse(db.Model):
    __tablename__='lesse'
    lesse_id= db.Column(db.Integer, primary_key=True,autoincrement=True,unique=True)
    house_number=db.Column(db.Integer, nullable=False)
    lesse_ci=db.Column(db.String(10),nullable=False)
    lesse_name= db.Column(db.String(100),nullable=False)
    lesse_phone=db.Column(db.String(10),nullable=False)
    start_date=db.Column(db.Date,nullable=False)
    end_date=db.Column(db.Date)
    lesse_state=db.Column(db.String(10))
    def __init__(self,house_number,lesse_ci,lesse_name,lesse_phone,start_date):
        self.house_number=house_number
        self.lesse_ci=lesse_ci
        self.lesse_name=lesse_name
        self.lesse_phone=lesse_phone
        self.start_date=start_date
        self.lesse_state='ACTIVO'


class House(db.Model):
    __tablename__='house'
    house_id=db.Column(db.Integer, primary_key=True,autoincrement=True,unique=True)
    house_number=db.Column(db.Integer, nullable=False,unique=True)
    house_description=db.Column(db.String(200), nullable=False)
    owner_ci=db.Column(db.String(10))
    lesse_ci=db.Column(db.String(10))

    def __init__(self,house_number,house_description ):
        self.house_number=house_number
        self.house_description=house_description
        self.owner_ci=''
        self.lesse_ci=''

class Visit(db.Model):
    __tablename__='visit'

    visit_id= db.Column(db.Integer, primary_key=True,autoincrement=True)
    visitor_ci=db.Column(db.String(13),nullable=False)
    visitor_name= db.Column(db.String(100),nullable=False)
    entrance_time=db.Column(db.DateTime,nullable=False)
    visit_type=db.Column(db.String(8),nullable=False)
    visit_car=db.Column(db.String(7))
    house_number=db.Column(db.Integer,nullable=False )
    exit_time=db.Column(db.DateTime)
    visit_state=db.Column(db.String(10))
    guard_name=db.Column(db.String(150))

    def __init__(self,visitor_ci,visitor_name,entrance_time,visit_type,visit_car,house_number,guard_name):
        self.visitor_ci=visitor_ci
        self.visitor_name=visitor_name
        self.entrance_time=entrance_time
        self.visit_type=visit_type
        self.visit_car=visit_car
        self.house_number=house_number
        self.visit_state='ESPERA'
        self.guard_name=guard_name

class Turnos(db.Model):
    __tablename__='turnos'
    turno_id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    entry_time=db.Column(db.DateTime,nullable=False)
    out_time=db.Column(db.DateTime,nullable=False)
    guardia_ci= db.Column(db.Integer,nullable=False)
    location=db.Column(db.Integer,nullable=False)
    state=db.Column(db.String(10),nullable=False)

class Location(db.Model):
    __tablename__='location'
    location_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    location_name=db.Column(db.String(100),nullable=False)



db.create_all()