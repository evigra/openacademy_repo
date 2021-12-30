# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class openacademy(models.Model):
#     _name = 'openacademy.openacademy'
#     _description = 'openacademy.openacademy'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


from odoo import models, fields, api, time

def get_uid(self, *a):
    return self.env.uid

class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Model to store course'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    responsible_id = fields.Many2one('res.users', ondelete='set null', string="Responsible", index=True,
        default=lambda self, *a: self.env.uid,
        #default=get_uid
        )

class Session(models.Model):    
    _name = 'openacademy.session'
    _description = 'Model to store session'

    name = fields.Char(required=True)
    #start_date = fields.Date(default=fields.Date.today)
    start_date = fields.Date(default=lambda *a:time.strftime('%Y-%m-%d %H:%M:%S'))
    datetime_test = fields.Datetime(default=fields.Datetime.now)
    duration = fields.Float(digits=(6, 2), help="Duration in days")    
    seats = fields.Integer(string="Number of seats")
    instructor_id = fields.Many2one('res.partner', string="Instructor", domain=['|', ('instructor', '=', True),                      ('category_id.name', 'ilike', "Teacher")])
    course_id = fields.Many2one('openacademy.course',   ondelete='cascade', string="Course", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")    
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    active = fields.Boolean(default=True) 
    
    
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        #import pdb; pdb.set_trace()
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats
    
    
    
