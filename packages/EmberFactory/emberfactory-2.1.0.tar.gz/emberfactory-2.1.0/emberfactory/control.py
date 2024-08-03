# -*- coding: utf-8 -*-
"""
EmberFactory / control: links the web UI to the drawing code

Written as a flask Blueprint; if revising the app structure is desired, consider reading
https://stackoverflow.com/questions/24420857/what-are-flask-blueprints-exactly

Copyright (C) 2020  philippe.marbaix@uclouvain.be
"""

from flask import Blueprint
from flask import render_template
from flask import request, url_for, redirect
from flask import current_app, session
from flask import send_from_directory
from werkzeug.utils import secure_filename
from os import path, makedirs
import sys
import uuid
import datetime
from time import time_ns
from embermaker import helpers as hlp
from emberfactory import makember as mke
import tempfile
import logging
from shutil import copyfile

bp = Blueprint("control", __name__)


# Process the received data (=> action when data is submitted from the start page)
@bp.route('/process', methods=['GET', 'POST'])
def process():
    # Avoid failure if this page is visited without providing data
    if request.method == 'GET':
        return redirect(url_for('sitenav.index'))

    # Default message to be returned within the template
    message = {"critical": "", "warning": "", "log": [], "uncaught-err": False, "begname": ""}
    session['result-msg'] = None
    session['outdirname'] = None

    # File upload and embermaker run
    # ------------------------------
    logger = hlp.Logger()
    try:
        # Get filename and check file
        fileitem = request.files['file']
        if not fileitem:
            message["critical"] = "No file provided or bad file."
        else:
            fnamesplit = path.splitext(path.basename(fileitem.filename))
            # Reject file if the extension does not suggest an Excel file
            # (wile devils can masquerade as angels, this protects against potential evils who look like evils)
            if fnamesplit[1] == '.xls':
                message["critical"] = "The EmberFactory cannot process .xls files, please convert it to .xlsx."
            elif fnamesplit[1] != '.xlsx':
                message["critical"] = "Unexpected file extension."
        if message["critical"]:
            session["result-msg"] = None
            return render_template("emberfactory/error.html", message=message)

        # Create a temporary folder to store files related to this request
        tmpdir = tempfile.TemporaryDirectory()
        # Create subdirectories for in and out so that we will never read from a folder to which the user can 'write'
        indirname = path.join(tmpdir.name, 'in')
        outdirname = path.join(tmpdir.name, 'out')
        makedirs(indirname)
        makedirs(outdirname)

        # Schedule timed deletion of the temporary folder
        current_app.scheduler.add_job(tmpdir.cleanup, 'date',
                                      run_date=(datetime.datetime.now() + datetime.timedelta(hours=2)))
        # Set pathname + upload file
        infile = path.join(indirname, secure_filename(path.basename(fileitem.filename)))
        fileitem.save(infile)

        # If user accepted to leave file
        if not request.form.get('delfile'):
            fnamesplit = path.splitext(path.basename(fileitem.filename))
            fname = secure_filename(str(uuid.uuid1()) + fnamesplit[1])  # replaces name by random unique name
            keptfile = path.join(current_app.instance_path, 'in/', fname)
            copyfile(infile, keptfile)

        session['infile'] = infile
        session['prefcsys'] = request.form['csys']

        # Execution of makember to produce the SVG file: CMYK is not allowed => force RGB
        # ("RGB-standard" means "from choice in file", which is what "standard" does, except if that gives CMYK)
        prefcsys = "RGB" if session['prefcsys'] == "RGB" else "RGB-standard"
        makeres = mke.makember(infile=infile, prefcsys=prefcsys, grformat='SVG', logger=logger)

        # An output file was generated (success!)
        if 'error' not in makeres:
            outfile = makeres['outfile']
            # Provide a url for the download, but without the extension, because we will have several ones:
            # (for details, see the download function below and the result.html template)
            begname = path.splitext(path.basename(outfile))[0]
            message["begname"] = begname  # inserts url for download
            warnings = logger.getlog("WARN", only=True, as_html=True)
            if len(warnings) > 0:
                message["warning"] = warnings
            critical = logger.getlog("ERROR", as_html=True)  # All messages beyond 'WARN' (may change in the future within EF)
            if len(critical) > 0:
                message["critical"] = critical
            message['img-width'] = makeres['width']
            message['img-ts'] = str(time_ns())
            result_msg_path = path.join(outdirname, "log.html")
            with open(result_msg_path, mode='x') as msg_file:
                msg_file.write("\n".join(logger.getlog("INFO", as_html=True)))
            session['outdirname'] = outdirname
            session['result-msg'] = message
            session['outfile_svg'] = outfile
            session['outfile_pdf'] = None
            return redirect(url_for('control.result'))

        # No file was generated: a fatal error occurred:
        else:
            message["critical"] = f"{makeres['error']}. After this message, the processing was stopped."
            session["result-msg"] = logger.getlog("INFO")
            return render_template("emberfactory/error.html", message=message)

    # An error occurred, and we did not handle it in any way:
    except Exception as exc:
        return render_template("emberfactory/error.html", message=get_errortrace(exc, logger))


# This function shows the results of processing the submitted data.
@bp.route('/result', methods=['GET', 'POST'])
def result():
    # If no result is available, go back to the start page (msg and file may disappear separately and are both needed)
    if "result-msg" not in session or session["result-msg"] is None or not path.isfile(session["outfile_svg"]):
        return redirect(url_for('sitenav.index'))

    return render_template("emberfactory/result.html", message=session["result-msg"])


# Raster image filenames and production recipes (used by the download method below):
# The dict contains: file-suffix: (img-type, width, dpi, quality)
# This mechanism provides flexibility; settings might be improved by learning about pdf2image and Poppler
imrecipes = {
    '-sc.png': ('png', 750, 200, None),
    '-re.png': ('png', 1500, 200, None),
    '-mr.png': ('png', None, 200, None),
    '-mr.jpg': ('jpeg', None, 300, {"quality": 70, "optimize": True, "progressive": False})
}


# Enable downloading the resulting files:
@bp.route('/out/<filename>', methods=['GET', 'POST'])
def download(filename):
    """
    If filename is available in the filesystem, return the file; otherwise,
    try to get it from converting the PDF on the basis on indications in the filename's suffix (last 7 char),
    using data from dict 'imrecipes'; return converted file when successful.
    :param filename:
    :return:
    """
    if 'outfile_svg' not in session or not path.isfile(session['outfile_svg']):
        # As the SVG file is the primary output of the processing, any request made while there is no SVG is blocked
        logging.warning("Bad file request")
        return render_template("emberfactory/error.html",
                               message={"critical": "No resulting diagram available. "
                                                    "Please note that files are deleted after 2 hours."})

    if filename == "log.html":  # Read log from file
        logfpath = path.join(session['outdirname'], 'log.html')
        if path.isfile(logfpath):
            return send_from_directory(session['outdirname'], "log.html")
        else:
            return "No log available"

    filepath = path.join(session['outdirname'], filename)
    logger = hlp.Logger()
    if not path.isfile(filepath):
        if not session['outfile_pdf'] or not path.isfile(session['outfile_pdf']):
            # The ouptut file is either the PDF itself or the result of a later conversion from it => generate the PDF
            try:
                makeres = mke.makember(infile=session['infile'], prefcsys=session['prefcsys'], grformat='PDF',
                                       logger=logger)
            except Exception as exc:
                return render_template("emberfactory/error.html", message=get_errortrace(exc, logger))

            if 'error' not in makeres:
                session['outfile_pdf'] = makeres['outfile']
            else:
                message = {"critical": f"Execution stopped after the following error: {makeres['error']}"}
                return render_template("emberfactory/error.html", message=message)

        if path.splitext(filename)[1] != ".pdf":
            # The file is not available yet; check imrecipes to see if we can generate it from the PDF:
            if len(filename) < 8 or filename[-7:] not in imrecipes:
                return render_template("emberfactory/error.html", message={"critical": "Could not handle request"})
            recipe = imrecipes[filename[-7:]]
            # Generate the image file from the PDF according to information from the recipe:
            pdfpath = filepath[:-7] + ".pdf"
            outpath = hlp.rasterize(pdfpath, filename, *recipe)
            if not outpath:
                return render_template("emberfactory/error.html", message={"critical": "File conversion failed"})

    response = send_from_directory(session['outdirname'], filename)
    # This added the header, but Safari still did not get the SVG file after several successful requests:
    # response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    if request.args.get('preview') == "1":
        response.headers['Content-Disposition'] = 'inline'
        # response.headers['Content-Type'] = 'image/svg+xml'  # Not needed - done already by default?
    else:
        response.headers['Content-Disposition'] = 'attachment; filename=' + path.basename(filepath)

    return response


def get_errortrace(exc, logger):
    message = {"critical": "An error for which there is no handling has occurred. We apologise. "
                           "The details provided below may help to understand the problem. "
                           "It might relate to an issue in your input file. We are interested in "
                           "receiving this information to improve the Ember Factory (see contact at the bottom)."}
    exc_tb = sys.exc_info()[2]
    errtrace = ""
    errtype = ""
    while exc_tb.tb_next is not None:
        if errtrace != "":
            errtrace += ">> "
        exc_tb = exc_tb.tb_next
        try:
            finame = exc_tb.tb_frame.f_globals['__name__']
            lineno = str(exc_tb.tb_frame.f_lineno)
            errtype = type(exc).__name__
            errtrace += "[" + finame + ":" + lineno + "] "
            errtrace += "[" + finame + ":" + lineno + "] "
        except KeyError:
            pass
    errtrace += errtype + " (" + str(exc) + ")"
    logger.addfail(errtrace)
    message["log"] = logger.getlog("INFO", as_html=True)
    message["uncaught-err"] = True
    session["result-msg"] = None  # This might move to an error function to avoid duplication?
    return message
