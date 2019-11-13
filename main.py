#!/usr/bin/env python3

# Russell Felts
# Flask Mailroom Assignment 01

""" Main """

import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

APP = Flask(__name__)


@APP.route('/')
def home():
    return redirect(url_for('all'))


@APP.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@APP.route('/create', methods=['GET', 'POST'])
def create():
    """
    Adds a new donation.
    For a Post request submit the donation info otherwise display the create donation page.
    Based on the donor info validity display and error with the create page or the all donations page.
    :return: The created donation or the all donations page
    """
    if request.method == 'POST':
        try:
            donor = Donor.select().where(Donor.name == request.form['donor_name']).get()
            print(donor.name, donor.id)
            donation = Donation(value=request.form['donation_amount'], donor_id=donor.id)
            print(donation.value, donation.donor_id)
            donation.save()
            return redirect(url_for('home'))
        except Donor.DoesNotExist:
            return render_template('create.jinja2', error="Donor does not exist.")

    return render_template('create.jinja2')
    

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 6738))
    APP.run(host='0.0.0.0', port=PORT)
