#!/usr/bin/env python
'''Forms code of api_flat app'''
# -*- coding: utf-8 -*-

from app import functions
from db import req

def add_user(form):
    response=0
    if form['flat_name']:
        try:
            name_exist = req.select('name', 'flats', name=form['flat_name'])[0][0]
            pwd = req.select('password', 'flats', name=form['flat_name'])[0][0]
            flat_id = req.select('flat_id', 'flats', name=form['flat_name'])[0][0]
            if functions.crypted_string(form['flat_password']) != pwd:
                response=1
            else:
                req.insert('users', 'first_name,last_name,email,password',\
                                    form['first_name'],\
                                    form['last_name'],\
                                    form['email'],\
                                    functions.crypted_string(form['password']))
                req.update('users', flat_id=flat_id, email=form['email'])
                response=4
        except:
            response=2
    else:
        req.insert('users', 'first_name,last_name,email,password',\
                            form['first_name'],\
                            form['last_name'],\
                            form['email'],\
                            functions.crypted_string(form['password']))
        response=4
    return response

def add_invoice(form, user_id):
    file_name = functions.file_date()+form['title']
    req.insert('invoices', 'title,price,prorata,date,details,file_name,user_id',\
                form['title'],\
                functions.str_to_float(form['price']),\
                bool(form.get('yes')),\
                functions.str_to_date(form['date']),\
                form['details'],\
                file_name,\
                user_id)

def add_meal(form, user_id):
    req.insert('meals','date,number,user_id',\
                        functions.str_to_date(form['mdate']),\
                        form['quantity'],\
                        user_id)

def add_flat(form, user_id):
    req.insert('flats', 'name,address,password',\
                        form['new_name'],\
                        form['new_address'],\
                        functions.crypted_string(form['new_password']))
    flat_id = req.select('flat_id', 'flats', name=form['new_name'])[0][0]
    req.update('users', flat_id=flat_id, user_id=user_id)

def add_flatmate(form, user_id):
    name_exist = req.select('name', 'flats', name=flat_name)[0][0]
    if name_exist:
        pwd = req.select('password', 'flats', name=form['flat_name'])[0][0]
        flat_id = req.select('flat_id', 'flats', name=form['flat_name'])[0][0]
        if functions.crypted_string(form['flat_password']) == pwd:
            req.update('users', flat_id=flat_id, user_id=user_id)
