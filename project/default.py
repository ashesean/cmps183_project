# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

from gluon import utils as gluon_utils
from gluon.tools import Mail
import json
import time
from gluon.tools import geocode
import math


def index():
    """
    # insert John Doe
    db.t_stylists.insert(full_name='John Doe', email='sashe@ucsc.edu',
                     street_address='1201 Barbara Jordan Blvd', city='Austin', state_acronym='TX',
                     bio='My name is John and I do not know how to cut hair.', salon='Great Clips',
                     phone_num='408-564-1527', user_id=999)

    # insert Cameron
    db.t_stylists.insert(full_name='Cameron Tooyserkani', email='sashe@ucsc.edu',
                     street_address='513 E Hamilton Ave', city='Campbell', state_acronym='CA',
                     bio='My name is Cameron and I know how to cut hair.', salon="18|8 Fine Men's Salon",
                     phone_num='408-775-5336', user_id=888)

    # insert Amelia
    db.t_stylists.insert(full_name='Amelia Marques', email='sashe@ucsc.edu',
                     street_address='821 Union Ave', city='Campbell', state_acronym='CA',
                     bio='My name is Amelia and I know how to cut hair.', salon="Diverse Salon",
                     phone_num='408-775-5336', user_id=777)

    # insert me
    db.t_stylists.insert(full_name='Sean Ashe', email='sashe@ucsc.edu',
                     street_address='19797 Merribrook Drive', city='Saratoga', state_acronym='CA',
                     bio='My name is Amelia and I do not know how to cut hair.',
                     phone_num='408-564-1527', user_id=555)
    """
    #db.t_stylists.drop()
    #db.t_profile_pics.drop()
    #db.t_business_hours.drop()
    #db.t_gallery_photos.drop()
    #db.t_reviews.drop()
    #db.commit()

    if auth.user_id is not None:
        in_db = db(db.t_stylists.user_id == auth.user_id).select()
        if not in_db:
            redirect(URL('default', 'profile_setup'))
        else:
            return dict()

    return dict()


def profile_setup():
    db.t_stylists.user_id.readable = db.t_stylists.user_id.writable = False

    form = SQLFORM(db.t_stylists)
    form.vars.user_id = auth.user_id
    if form.process().accepted:
        db.t_business_hours.insert(stylist_id=int(auth.user_id))
        redirect(URL('default', 'upload_profile_pic'))

    return dict(form=form)


def upload_profile_pic():
    db.t_profile_pics.post_date.readable = db.t_profile_pics.post_date.writable = False
    db.t_profile_pics.stylist_id.readable = db.t_profile_pics.stylist_id.writable = False

    form = SQLFORM(db.t_profile_pics)
    form.vars.stylist_id = auth.user_id
    if form.process().accepted:
        redirect(URL('default', 'index'))

    return dict(form=form)


def upload_gallery_photo():
    db.t_gallery_photos.post_date.readable = db.t_gallery_photos.post_date.writable = False
    db.t_gallery_photos.stylist_id.readable = db.t_gallery_photos.stylist_id.writable = False

    form = SQLFORM(db.t_gallery_photos)
    form.vars.stylist_id = int(request.args[0])

    if form.process().accepted:
        redirect(URL('default', 'gallery_page', args=[request.args[0]]))

    return dict(form=form)


def write_review():
    db.t_reviews.post_date.readable = db.t_reviews.post_date.writable = False;
    db.t_reviews.stylist_id.readable = db.t_reviews.stylist_id.writable = False

    form = SQLFORM(db.t_reviews)
    form.vars.stylist_id = int(request.args[0])

    if form.process().accepted:
        redirect(URL('default', 'stylist_page', args=[request.args[0]]))

    return dict(form=form)


def nearby_stylists():
    city = request.args(0)
    state = request.args(1)
    stylists = db(db.t_stylists.state_acronym == str(state)).select()
    near_stylists = []
    pics = []

    address = str(city) + ', ' + str(state) + ", " + 'USA'
    (lat, long) = geocode(address)

    # function that computes distance between two (lat, long) points
    def distance_on_unit_sphere(lat1, long1, lat2, long2):
        degrees_to_radians = math.pi/180.0
        phi1 = (90.0 - lat1)*degrees_to_radians
        phi2 = (90.0 - lat2)*degrees_to_radians
        theta1 = long1*degrees_to_radians
        theta2 = long2*degrees_to_radians
        cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
            math.cos(phi1)*math.cos(phi2))
        arc = math.acos( cos )
        return arc * 3960

    # get all stylists that are within 10 miles
    for stylist in stylists:
        stylist_address = str(stylist.city) + ', ' + str(stylist.state_acronym) + ", " + 'USA'
        (lat_stylist, long_stylist) = geocode(stylist_address)
        distance = distance_on_unit_sphere(lat, long, lat_stylist, long_stylist)
        if distance < 15.0:
            near_stylists.append(stylist)

    # get profile pic of each stylist in near_stylists
    for stylist in near_stylists:
        images = db(db.t_profile_pics.stylist_id == stylist.user_id).select(orderby=~db.t_profile_pics.post_date)
        image = images[0]
        pics.append(image)

    return dict(stylists=near_stylists, pics=pics)


def stylist_page():
    user_id = request.args(0)

    business_hours = db(db.t_business_hours.stylist_id == user_id).select().first()
    stylist = db(db.t_stylists.user_id == user_id).select().first()
    profile_pics = db(db.t_profile_pics.stylist_id == user_id).select(orderby=~db.t_profile_pics.post_date)
    profile_pic = profile_pics[0]
    reviews = db(db.t_reviews.stylist_id == user_id).select(orderby=~db.t_reviews.post_date)

    has_reviews = True
    if not reviews:
        has_reviews = False

    return dict(business_hours=business_hours, stylist=stylist, profile_pic=profile_pic, reviews=reviews, has_reviews=has_reviews)


def gallery_page():
    user_id = request.args(0)
    gallery_images = db(db.t_gallery_photos.stylist_id == user_id).select(orderby=~db.t_gallery_photos.post_date)
    stylist = db(db.t_stylists.user_id == user_id).select().first()

    has_images = True
    if not gallery_images:
        has_images = False

    return dict(images=gallery_images, stylist=stylist, has_images=has_images)

def update_time():
    db.t_business_hours.update_or_insert((db.t_business_hours.stylist_id == request.vars.stylist_id),
                                         mon_start=request.vars.mon_start,
                                         mon_finish=request.vars.mon_finish,
                                         tues_start=request.vars.tues_start,
                                         tues_finish=request.vars.tues_finish,
                                         wed_start=request.vars.wed_start,
                                         wed_finish=request.vars.wed_finish,
                                         thurs_start=request.vars.thurs_start,
                                         thurs_finish=request.vars.thurs_finish,
                                         fri_start=request.vars.fri_start,
                                         fri_finish=request.vars.fri_finish,
                                         sat_start=request.vars.sat_start,
                                         sat_finish=request.vars.sat_finish,
                                         sun_start=request.vars.sun_start,
                                         sun_finish=request.vars.sun_finish,
                                         stylist_id=request.vars.stylist_id)
    return "ok"


def prepare_an_email():
    stylist = db(db.t_stylists.user_id == int(request.args[0])).select().first()

    return dict(stylist=stylist)


def send_an_email():

    stylist = db(db.t_stylists.user_id == int(request.vars.user_id)).select().first()
    email = stylist.email

    mail = Mail()
    mail.settings.server = 'smtp.gmail.com:587'
    mail.settings.sender = 'stylisterinc@gmail.com'
    mail.settings.login = 'stylisterinc@gmail.com:seanashe'

    mail.send(email,
              'Message from ' + str(request.vars.sender_name),
               str(request.vars.email_stuff))

    return "ok"


def update_stylist():
    db.t_stylists.update_or_insert((db.t_stylists.user_id == request.vars.stylist_id),
                                   full_name=request.vars.full_name,
                                   salon=request.vars.salon,
                                   address=request.vars.address,
                                   city=request.vars.city,
                                   state=request.vars.state,
                                   phone_num=request.vars.phone_num,
                                   bio=request.vars.bio,
                                   deals=request.vars.deals)
    return "ok"


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    db.auth_user.first_name.writable=False
    db.auth_user.first_name.readable=False
    db.auth_user.last_name.writable=False
    db.auth_user.last_name.readable=False
    db.auth_user.email.writable=False
    db.auth_user.email.readable=False

    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


