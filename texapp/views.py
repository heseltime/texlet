from genericpath import exists
import mimetypes
from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import FileResponse
from django.http import QueryDict
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import LetterForm, ProfileUser, ProfileUserForm, AddresseeForm, ProfileAddressee
from django.contrib.auth.decorators import login_required

import subprocess, os
import datetime
import re

def write_letter(request): # aka order
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LetterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            #
            # db-archive, and get letter instance from form instance
            #
            letter = form.save()

            #
            # file writing prep
            #

            # remove problematic character ':' in iso format
            now = re.sub(':', '-', datetime.datetime.now().isoformat(timespec='seconds'))

            # problem characters in reference line
            ref_cleaner = re.sub('[#<$+%>!`&*\'|{?"=}/:\\@]', '', form.cleaned_data['reference'])

            # whitespaces in reference also problematic, so
            ref_arr = ref_cleaner.split(' ')

            # think about importable helper fn for the above
            # and or replace with std lib sol
            # TODO

            file_tag = ref_arr[0]
            # make file_tag from reference just a bit more expressive, if poss
            print(len(ref_arr))
            if len(ref_arr) > 1:
                file_tag = '%s-%s' % (file_tag, ref_arr[1])
            if len(ref_arr) > 2:
                file_tag = '%s-%s' % (file_tag, ref_arr[2])

            #
            # fill template and write to file
            #

            t_tex = get_template('letter.tex')

            data_for_tex = form.cleaned_data
            # data according to form/model

            # user profile metadata:
            try:
                metadata_ob = ProfileUser.objects.get(user_id=request.user.id)
                metadata = metadata_ob.__dict__
                data_for_tex = dict(data_for_tex, **metadata)
                # combine metadata and form data

            except ProfileUser.DoesNotExist:
                print('does not exist')
            except ProfileUser.MultipleObjectsReturned:
                print('multiple objects returned by query but one expected by get')
            except:
                print('something unexpected occurred')
                     
            doc_tex = t_tex.render(data_for_tex)

            with open('%s-%s.tex' % (file_tag, now), 'w') as file: 
                file.write(doc_tex)

            #
            # file processing, to static out dir
            #

            x = subprocess.call('pdflatex %s-%s.tex' % (file_tag, now))

            if x != 0:
                print('Exit code %s' % x)
                messages.error(request, 'Error creating document, error code %s' % x)
            else:
                #os.system('start %s-%s.pdf' % (file_tag, now))
                # this is done in root and requires aux and txt-log files
                os.remove('%s-%s.aux' % (file_tag, now))
                os.remove('%s-%s.log' % (file_tag, now))
                # and the original tex is also still here
                os.remove('%s-%s.tex' % (file_tag, now))
                # move to static dir, prefix with "textype"
                os.replace('%s-%s.pdf' % (file_tag, now), 'texlet/static/texapp/out/letter-%s-%s.pdf' % (file_tag, now))

                # redirect to a new URL
                # with query dict
                data = {
                    'texttype': 'letter',
                    'reference': '%s' % file_tag,
                    'timestamp': '%s' % now,
                }

                q_dict = QueryDict('', mutable=True)
                q_dict.update(data)

                return HttpResponseRedirect('/pickup?%s' % q_dict.urlencode())

    # if a GET (or any other method): blank form
    else:
        if not request.user.is_authenticated:
            messages.warning(request, 'Please sign in or sign up to use this web app.' )

        form = LetterForm()
        form_secondary = AddresseeForm()

        addressees = ProfileAddressee.objects.filter(user_id=request.user.id)

    return render(request, 'letter.html', {'form': form, 'form_secondary': form_secondary, 'addressees': addressees})

def add_addressee(request): 
    if request.method == 'POST':
        form = AddresseeForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()  
            messages.success(request, 'Addressee added.' )
            return HttpResponseRedirect('/')

    return HttpResponseRedirect('/')


def pickup(request):
    if request.method == 'GET':

        data = request.GET.dict()

        file = 'texlet/static/texapp/out/letter-%s-%s.pdf' % (data['reference'], data['timestamp']) # request.GET['ref'] etc.
        file_for_template = 'texapp/out/letter-%s-%s.pdf' % (data['reference'], data['timestamp']) # rel to static tag
        
        if exists(file):
            data = {
                'title': 'Document processed',
                'message': 'Here is your letter',
                'file': file_for_template,
                'direct_link': 'http://' + request.get_host() + re.sub('pickup', 'direct-pickup', request.get_full_path()),
                }
                    
        else:
            data = {
                'title': 'Sorry',
                'message': 'no letter',
                }
        
        return render(request, 'pickup.html', data)

    else:
        return HttpResponseRedirect('/')

def direct_pickup(request):
    if request.method == 'GET':

        data = request.GET.dict()
        file = 'texlet/static/texapp/out/letter-%s-%s.pdf' % (data['reference'], data['timestamp'])

        if exists(file):
            binary_stream = open(file, 'rb')

            return FileResponse(binary_stream, as_attachment=True, filename='letter-%s-%s.pdf' % (data['reference'], data['timestamp']))
                    
        else:
            data = {
                'title': 'Sorry',
                'message': 'no letter',
                }

            return render(request, 'pickup.html', data)

    else:
        return HttpResponseRedirect('/')

# user PROFILE management for texapp

@login_required
def manage_profile(request):
    if request.method == 'POST':
        form = ProfileUserForm(request.POST) # partial, without username

        if form.is_valid():
            # now set username
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            messages.success(request, 'Your user profile was updated successfully')
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Error updating your user profile')
    else:
        form = ProfileUserForm(instance=request.user)
    
    # fetch it from database then render it to the template
    profile = ProfileUser.objects.filter(user=request.user)

    if profile:
        profile = profile.values()[0]

    return render(request, 'profile.html', {'form': form, 'profile': profile})

@login_required
def delete_profile(request):
    ob = ProfileUser.objects.get(user_id=request.user.id)

    if ob:
        ob.delete()
        messages.success(request, 'Your user profile was updated successfully')
        return HttpResponseRedirect('/manage-profile')
    else:
        messages.error(request, 'Error updating your user profile')
