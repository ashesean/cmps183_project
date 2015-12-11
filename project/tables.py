#########################################################################
## Define your tables below; for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
from datetime import datetime

db.define_table('t_stylists',
                Field('full_name', required=True, requires=IS_NOT_EMPTY()),
                Field('email', 'string', required=True, requires=IS_NOT_EMPTY()),
                Field('street_address', 'string', required=True, requires=IS_NOT_EMPTY()),
                Field('city', 'string', required=True, requires=IS_NOT_EMPTY()),
                Field('state_acronym', 'string', length=2, required=True, requires=IS_NOT_EMPTY()),
                Field('bio', 'text', required=True, requires=IS_NOT_EMPTY()),
                Field('salon', 'string'),   # if this is empty, then the stylist is Independent
                Field('phone_num', 'string', required=True, requires=IS_NOT_EMPTY()),
                Field('deals', 'text'),
                Field('user_id', 'integer')
               )

db.define_table('t_profile_pics',
                Field('profile_pic', 'upload', required=True, requires=IS_NOT_EMPTY()),
                Field('post_date', 'datetime', default=datetime.utcnow()),
                Field('stylist_id', 'integer') #reference t_stylists.user_id
               )

db.define_table('t_gallery_photos',
                Field('photo', 'upload'),
                Field('post_date', 'datetime', default=datetime.utcnow()),
                Field('stylist_id', 'integer') #reference t_stylists.user_id
               )

db.define_table('t_reviews',
                Field('review', 'text', required=True, requires=IS_NOT_EMPTY()),
                Field('author', 'string', required=True, requires=IS_NOT_EMPTY()),
                Field('post_date', 'datetime', default=datetime.utcnow()),
                Field('stylist_id', 'integer') #reference t_stylists.user_id
               )

db.define_table('t_business_hours',
                Field('mon_start', 'time', default=''),
                Field('mon_finish', 'time', default=''),
                Field('tues_start', 'time', default=''),
                Field('tues_finish', 'time', default=''),
                Field('wed_start', 'time', default=''),
                Field('wed_finish', 'time', default=''),
                Field('thurs_start', 'time', default=''),
                Field('thurs_finish', 'time', default=''),
                Field('fri_start', 'time', default=''),
                Field('fri_finish', 'time', default=''),
                Field('sat_start', 'time', default=''),
                Field('sat_finish', 'time', default=''),
                Field('sun_start', 'time', default=''),
                Field('sun_finish', 'time', default=''),
                Field('stylist_id', 'integer') #reference t_stylists.user_id
               )