# tournadmin

from flask import Blueprint,request, render_template, redirect, abort, flash, url_for

tournadmin = Blueprint('tournadmin', __name__, template_folder='templates/tournadmin')