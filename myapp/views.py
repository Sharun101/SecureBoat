import qrcode
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from myapp.models import *
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import auth


def logout(request):
    auth.logout(request)
    return render(request,'index.html')


# Create your views here
def login(request):
    return render(request, 'index.html')

def login_post(request):
    username=request.POST['Username']
    password=request.POST['Password']

    ob=loginTbl.objects.filter(username=username,password=password)
    if ob.exists():
        ob1=loginTbl.objects.get(username=username,password=password)
        request.session['lid']=ob1.id
        if ob1.utype=='admin':
            ob2 = auth.authenticate(username='admin', password='admin')
            if ob2 is not None:
                auth.login(request, ob2)
            return HttpResponse('''<script>alert('admin login successfull');window.location='/adminhome';</script>''')
        elif ob1.utype == "owner":
            ob2 = auth.authenticate(username='admin', password='admin')
            if ob2 is not None:
                auth.login(request, ob2)
            return HttpResponse('''<script>alert('Owner login successfull');window.location='/owner_home';</script>''')

        else:
            return HttpResponse('''<script>alert('Invalid username or password');window.location='/';</script>''')
    else:
        return HttpResponse('''<script>alert('user not exist');window.location='/';</script>''')

def registration(request):
    return  render(request, 'regindex.html')


def registration_post(request):
    fn=request.POST['textfield']
    ln=request.POST['textfield2']
    dob=request.POST['textfield5']
    place=request.POST['textfield6']
    post=request.POST['textfield7']
    pin=request.POST['textfield4']
    phno=request.POST['textfield3']
    email=request.POST['textfield8']
    un=request.POST['textfield9']
    pwd=request.POST['textfield10']
    rpwd=request.POST['textfield11']
    gen=request.POST['radiobutton']

    img=request.FILES['file']

    ob=loginTbl()
    ob.username=un
    ob.password=pwd
    ob.utype="pending"
    ob.save()

    ob1=ownerTbl()
    ob1.LOGIN=ob
    ob1.image=img
    ob1.firstname=fn
    ob1.lastname=ln
    ob1.place=place
    ob1.post=post
    ob1.pin=pin
    ob1.phno=phno
    ob1.email=email
    ob1.gender=gen
    ob1.dob=dob
    ob1.save()


    return  HttpResponse('''<script>alert('Success');window.location='/'</script>''')





@login_required(login_url='/')
def adminhome(request):
    return render(request,'admin/adminindex.html')

@login_required(login_url='/')
def adminForgotPassword(request):
    return render(request,'admin/forgotpassword.html')

@login_required(login_url='/')
def view_rooute(request):
    ob=routeTbl.objects.all()
    return render(request,'admin/view_route.html',{'val':ob})

@login_required(login_url='/')
def manage_seats(request):
    return  render(request, 'admin/manageroute.html')

@login_required(login_url='/')
def manage_route_post(request):
    fromRoute=request.POST['textfield']
    to=request.POST['textfield1']
    ob=routeTbl()
    ob.fromRoute=fromRoute
    ob.to=to
    ob.save()
    return  HttpResponse('''<script>alert('added');window.location='/manage_seats'</script>''')

@login_required(login_url='/')
def manage_stop(request,id):
    request.session['rid']=id
    ob=routeTbl.objects.get(id=id)
    obb=stopTbl.objects.filter(ROUTE_id=id)
    return render(request,'admin/manage_stop.html',{'val':obb})

@login_required(login_url='/')
def dlete_stop(request,id):
    request.session['rid'] = id
    obb = stopTbl.objects.filter(id=id)
    obb.delete()
    return  HttpResponse('''<script>alert('deleted');window.location='/view_rooute'</script>''')

@login_required(login_url='/')
def dlete_route(request,id):
    request.session['rid'] = id
    obb = routeTbl.objects.filter(id=id)
    obb.delete()
    return  HttpResponse('''<script>alert('deleted');window.location='/view_rooute'</script>''')


@login_required(login_url='/')
def add_stop(request):
    return render(request,'admin/add_stop.html')

@login_required(login_url='/')
def add_stop_post(request):
    name=request.POST['textfield']
    ob=stopTbl()
    ob.name=name
    ob.ROUTE=routeTbl.objects.get(id=request.session['rid'])
    ob.save()
    return  HttpResponse('''<script>alert('added');window.location='/view_rooute'</script>''')





@login_required(login_url='/')
def reply(request,id):
    ob=complaintTbl.objects.get(id=id)
    return  render(request,'admin/reply.html',{"val":ob})

@login_required(login_url='/')
def reply_post(request):
    reply1= request.POST["textfield"]
    id= request.POST["id"]

    ob=complaintTbl.objects.get(id = id)
    ob.reply = reply1
    ob.save()
    return  HttpResponse('''<script>alert('replied');window.location='/view_complaint'</script>''')



@login_required(login_url='/')
def track_boat(request):
    ob=boatTbl.objects.filter(status='accepted')
    return  render(request,'admin/track_boat.html',{"val":ob})





from django.shortcuts import render
from .models import assign_table, locationTbl

def admin_view_assign_and_track(request):
    assigned_boats = assign_table.objects.select_related('BOAT', 'DRIVER').all()

    # Fetch locations of drivers
    driver_locations = {loc.DRIVER.id: loc for loc in locationTbl.objects.all()}

    # Combine boat details with location
    boat_data = []
    for assign in assigned_boats:
        location = driver_locations.get(assign.DRIVER.id)  # Get location by driver ID
        boat_data.append({
            "boat_name": assign.BOAT.name,
            "boat_image": assign.BOAT.image.url if assign.BOAT.image else None,
            "boat_regno": assign.BOAT.regno,
            "driver_name": assign.DRIVER.firstname,  # Assuming DRIVER model has a 'name' field
            "status": assign.status,
            "latitude": location.latitude if location else "Not Available",
            "longitude": location.longitude if location else "Not Available"
        })
    print()
    return render(request, 'admin/view assign and track.html', {"boats": boat_data})


@login_required(login_url='/')
def verify_boat(request):
    ob=boatTbl.objects.filter(status='pending')
    print(ob)
    return  render(request,'admin/verify_boat.html',{'value':ob})

@login_required(login_url='/')
def verify_boat_search(request):
    name=request.POST['textfield']
    ob = boatTbl.objects.filter(name__istartswith=name)
    return render(request, 'admin/verify_boat.html',{'value':ob})

@login_required(login_url='/')
def view_complaint(request):
    ob=complaintTbl.objects.all()
    return  render(request,'admin/view_complaint.html',{'value':ob})

@login_required(login_url='/')
def view_drivers(request):
    ob=driverTbl.objects.all()
    return  render(request,'admin/view_drivers.html',{'value':ob})

@login_required(login_url='/')
def view_drivers_search(request):
    firstname=request.POST['Input']
    ob = driverTbl.objects.filter(firstname__istartswith=firstname)
    return render(request, 'admin/view_drivers.html',{'value':ob})

@login_required(login_url='/')
def view_emergency(request):
    ob = emergencyTbl.objects.all()
    return  render(request,'admin/view_emergency.html',{'value':ob})

@login_required(login_url='/')
def view_owner(request):
    ob=ownerTbl.objects.all()
    return  render(request,'admin/view_owner.html',{'val':ob})

@login_required(login_url='/')
def admin_search_owner(request):
    firstname=request.POST['Input']
    ob=ownerTbl.objects.filter(firstname__istartswith=firstname)
    return render(request,'admin/view_owner.html',{'val':ob,"n":firstname})


@login_required(login_url='/')
def view_timeschedule(request,id):
    ob = timescheudle.objects.filter(BOAT_id=id)
    return  render(request,'admin/view_timeschedule.html', {'value': ob})

# def view_timeschedule_card(request,id):
#     ob = timescheudle_details.objects.filter(id=id)
#     return  render(request,'admin/view_timeschedule_card.html',{'data':ob})

@login_required(login_url='/')
def view_timeschedule_card(request,id):
    request.session['rid']=id
    print(id,"hhhhhhhhhhhhhh")
    obb=routeTbl.objects.get(id=request.session['rid'])
    ob = stopTbl.objects.filter(ROUTE_id=obb)
    print(ob,"jjjjjjjjj")
    return  render(request,'admin/view_timeschedule_card.html',{'data':ob})


@login_required(login_url='/')
def accept_owner(request,id):
    ob=loginTbl.objects.get(id=id)
    ob.utype='owner'
    ob.save()
    return  HttpResponse('''<script>alert('accepted');window.location='/view_owner';</script>''')

@login_required(login_url='/')
def reject_owner(request,id):
    ob=loginTbl.objects.get(id=id)
    ob.utype='rejected'
    ob.save()
    return HttpResponse('''<script>alert('rejected');window.location='/view_owner'</script>''')

@login_required(login_url='/')
def accept_boat(request,id):
    ob=boatTbl.objects.get(id=id)
    ob.status='accepted'
    ob.save()
    return  HttpResponse('''<script>alert('accepted');window.location='/verify_boat';</script>''')

@login_required(login_url='/')
def reject_boat(request,id):
    ob=boatTbl.objects.get(id=id)
    ob.status='rejected'
    ob.save()
    return HttpResponse('''<script>alert('rejected');window.location='/verify_boat'</script>''')

#-------------------------owner--------
@login_required(login_url='/')
def owner_add_and_manage_driver(request):
    kk=ownerTbl.objects.get(LOGIN__id=request.session['lid'])
    ob=driverTbl.objects.filter(OWNER__id=kk.id)
    return render(request,'owner/add&managedriverincludinglicense.html',{"val":ob})


def owner_search_driver(request):
    firstname=request.POST['textfield']
    ob=driverTbl.objects.filter(firstname__istartswith=firstname)
    return render(request,'owner/add&managedriverincludinglicense.html',{"val":ob,'firstname':firstname})



from playsound import playsound


def count(request, co, id):
    ob = boatTbl.objects.get(id=id)
    print(ob,"======")
    print(ob.no_of_passengers,"======")
    if ob.no_of_passengers < co:
        print("[ALERT] Overloaded! Playing alarm...")
        import winsound

        # Frequency (Hz) and duration (milliseconds)
        frequency = 1000  # 1000 Hz
        duration = 500  # 500 ms

        # Play the sound
        winsound.Beep(frequency, duration)
    return HttpResponse("ok")  # ✅ Returning a proper HTTP response


@login_required(login_url='/')
def owner_send_notification_driver(request,id):
    request.session['bid'] = id
    obb = driverTbl.objects.get(id=id)
    return render(request,'owner/sendnotification_driver.html',{'val':obb})

@login_required(login_url='/')
def owner_send_notification_driver_post(request):
    notification=request.POST['textfield']

    ob=notificationTbl()
    ob.notification=notification
    ob.DRIVER=driverTbl.objects.get(id=request.session['bid'])
    ob.OWNER=ownerTbl.objects.get(LOGIN__id=request.session['lid'])
    import datetime
    ob.date=datetime.datetime.today().now()
    ob.save()
    return HttpResponse('''<script>alert('send successfully');window.location='/owner_add_and_manage_driver'</script>''')

@login_required(login_url='/')
def assign_boat(request,id):
    request.session['bid']=id
    ob=boatTbl.objects.filter(OWNER__LOGIN_id=request.session['lid'])
    obb=driverTbl.objects.get(id=id)
    return render(request,'owner/assign_boat.html',{"val":ob,'vall':obb})

@login_required(login_url='/')
def assign_boat_post(request):
    boat=request.POST['select']

    ob=assign_table()
    ob.BOAT=boatTbl.objects.get(id=boat)
    ob.DRIVER=driverTbl.objects.get(id=request.session['bid'])
    ob.status='assigned'
    ob.save()
    return HttpResponse('''<script>alert('assigned');window.location='/owner_add_and_manage_driver'</script>''')


@login_required(login_url='/')
def owner_add_new(request):
    return render(request,'owner/AddNew.html')

@login_required(login_url='/')
def  owner_add_new_post(request):
    name=request.POST['textfield']
    image=request.FILES['file']
    regno=request.POST['textfield2']
    fitness=request.FILES['file2']
    noofpassengers=request.POST['textfield3']
    type=request.POST['textfield4']
    brand=request.POST['textfield5']
    discription=request.POST['textarea']
    certificate=request.FILES['file3']

    fs=FileSystemStorage()
    fsave=fs.save(image.name,image)
    fs1=FileSystemStorage()
    fs1save=fs1.save(fitness.name,fitness)
    fs2=FileSystemStorage()
    fs2save=fs2.save(certificate.name,certificate)

    ob=boatTbl()
    ob.OWNER=ownerTbl.objects.get(LOGIN=request.session["lid"])
    ob.name=name
    ob.image = fsave
    ob.regno=regno
    ob.status='pending'
    ob.fitness=fs1save
    ob.no_of_passengers=noofpassengers
    ob.type=type
    ob.brand=brand
    ob.discription=discription
    ob.certificate=fs2save
    ob.save()

    qr = "media/qr/" + str(ob.id) + ".png"
    # Data to encode in the QR code

    # o.qr = "media/qr/" + str(o.id) + ".png"
    # o.save()  # You can change this to your desired data
    data = str(ob.id)
    # Generate a QR code instance
    ob1 = qrcode.QRCode(
        version=1,  # The QR code version (1-40), higher is a larger code.
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level (L, M, Q, H).
        box_size=10,  # The size of each box in the QR code.
        border=4,  # The border size around the QR code.
    )

    # Add data to the QR code
    ob1.add_data(data)
    ob1.make(fit=True)

    # Create a PIL (Python Imaging Library) image from the QR code data
    ob1 = ob1.make_image(fill_color="black", back_color="white")
    # Save the image to a file or display it
    ob1.save("media/qr/" + str(ob.id) + ".png")  # Save
    # o.save()

    obx=boatTbl.objects.get(id=ob.id)
    obx.qryt=qr
    obx.save()
    return HttpResponse('''<script>alert('addedd');window.location='/owner_view_boat'</script>''')


@login_required(login_url='/')
def owner_edit_new(request,id):
    request.session["bid"]=id
    kk=boatTbl.objects.get(id=id)
    return render(request,'owner/edit_boatdetails.html',{"val":kk})

@login_required(login_url='/')
def  owner_edit_new_post(request):
    name=request.POST['textfield']
    regno=request.POST['textfield2']
    noofpassengers=request.POST['textfield3']
    type=request.POST['textfield4']
    brand=request.POST['textfield5']
    discription=request.POST['textarea']
    ob = boatTbl.objects.get(id=request.session["bid"])
    if 'file' in request.FILES:
        image = request.FILES['file']
        fs = FileSystemStorage()
        fsave = fs.save(image.name, image)
        ob.image = fsave
    elif 'file2' in request.FILES:
        fitness = request.FILES['file2']
        fs1 = FileSystemStorage()
        fs1save = fs1.save(fitness.name, fitness)
        ob.fitness = fs1save
    elif 'file3' in request.FILES:
        certificate = request.FILES['file3']
        fs2 = FileSystemStorage()
        fs2save = fs2.save(certificate.name, certificate)
        ob.certificate = fs2save
    ob.OWNER=ownerTbl.objects.get(LOGIN=request.session["lid"])
    ob.name=name
    ob.regno=regno

    ob.no_of_passengers=noofpassengers
    ob.type=type
    ob.brand=brand
    ob.discription=discription
    ob.save()
    return HttpResponse('''<script>alert('Edit');window.location='/owner_view_boat'</script>''')



@login_required(login_url='/')
def owner_addnew_add_and_managedriver(request):
    return render(request,'owner/addnew_add&managedriver.html')

@login_required(login_url='/')
def owner_addnew_add_and_managedriver_post(request):
    firstname=request.POST['textfield']
    lastname=request.POST['textfield2']
    place=request.POST['textfield3']
    post=request.POST['textfield4']
    pin=request.POST['textfield5']
    phno=request.POST['textfield6']
    license=request.POST['textfield7']
    email=request.POST['textfield8']
    gender=request.POST['radiobutton']
    dob=request.POST['textfield10']
    username=request.POST['textfield11']
    password=request.POST['textfield12']
    image=request.FILES['file']
    fs=FileSystemStorage()
    fp=fs.save(image.name,image)



    ob=loginTbl()
    ob.username=username
    ob.password=password
    ob.utype="driver"
    ob.save()

    ob1=driverTbl()
    ob1.LOGIN=ob
    ob1.firstname=firstname
    ob1.lastname=lastname
    ob1.place=place
    ob1.post=post
    ob1.pin = pin
    ob1.phno = phno
    ob1.license = license
    ob1.email = email
    ob1.gender = gender
    ob1.dob = dob
    ob1.image=fp
    ob1.OWNER=ownerTbl.objects.get(LOGIN_id=request.session['lid'])
    ob1.save()
    return  HttpResponse('''<script>alert('Driver Added');window.location='/owner_add_and_manage_driver';</script>''')




@login_required(login_url='/')
def owner_Addnew_insurance(request):
    ob=boatTbl.objects.filter(OWNER__LOGIN=request.session["lid"])
    return render(request,'owner/Addnew_insurance.html',{"data":ob})

@login_required(login_url='/')
def owner_edit_insurence(request,id):
    request.session['iid']=id
    ob=insuranceTbl.objects.get(id=id)
    obb=boatTbl.objects.all()
    return render(request,'owner/Editnew_insurance.html',{"val":ob,'data':obb})

@login_required(login_url='/')
def owner_Addnew_insurance_post(request):
    boat=request.POST['textfield']
    policy_no=request.POST['textfield2']
    provider=request.POST['textfield3']
    date=request.POST['textfield4']
    validity=request.POST['textfield5']
    type=request.POST['textfield6']

    ob=insuranceTbl()
    ob.BOAT_id=boat
    ob.policy_no=policy_no
    ob.provider=provider
    ob.date=date
    ob.validity=validity
    ob.type=type
    ob.save()
    return HttpResponse('''<script>alert(' Added');window.location='/owner_add_or_manage_insurance';</script>''')


@login_required(login_url='/')
def owner_edit_insurance_post(request):
    boat=request.POST['textfield']
    policy_no=request.POST['textfield2']
    provider=request.POST['textfield3']
    date=request.POST['textfield4']
    validity=request.POST['textfield5']
    type=request.POST['textfield6']

    ob=insuranceTbl.objects.get(id=request.session['iid'])
    ob.BOAT_id=boat
    ob.policy_no=policy_no
    ob.provider=provider
    ob.date=date
    ob.validity=validity
    ob.type=type
    ob.save()
    return HttpResponse('''<script>alert(' edited');window.location='/owner_add_or_manage_insurance';</script>''')




@login_required(login_url='/')
def owner_add_or_manage_insurance(request):
    ob = insuranceTbl.objects.filter(BOAT__OWNER__LOGIN=request.session["lid"])
    return render(request,'owner/addormanageinsurence.html',{"data":ob})

@login_required(login_url='/')
def owner_search_insuranceboat(request):
    name=request.POST['textfield']
    ob = insuranceTbl.objects.filter(BOAT__name__istartswith=name)
    return render(request,'owner/addormanageinsurence.html',{"data":ob})

def owner_delete_insurencedetails(request,id):
    request.session['iid']=id
    ob=insuranceTbl.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('delete successfully');window.location='/owner_add_or_manage_insurance'</script>''')



@login_required(login_url='/')
def owner_assign_add_and_manage(request):
    return render(request,'owner/assign_add&managedriver.html')

@login_required(login_url='/')
def owner_edit_add_and_manage_driver(request,id):
    request.session['did']=id
    ob=driverTbl.objects.get(id=id)
    return render(request,'owner/edit_add&managedriver.html',{'val':ob})

@login_required(login_url='/')
def owner_delete_driver(request,id):
    request.session['did']=id
    ob=driverTbl.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('Driver deletd');window.location='/owner_add_and_manage_driver';</script>''')

@login_required(login_url='/')
def owner_edit_add_and_manage_driver_post(request):
    firstname=request.POST['textfield']
    lastname=request.POST['textfield2']
    place=request.POST['textfield3']
    post=request.POST['textfield4']
    pin=request.POST['textfield5']
    phno=request.POST['textfield6']
    license=request.POST['textfield7']
    email=request.POST['textfield8']
    gender=request.POST['radiobutton']
    dob=request.POST['textfield10']


    if 'file' in request.FILES:
        image = request.FILES['file']
        fs = FileSystemStorage()
        fp = fs.save(image.name, image)
        ob1 = driverTbl.objects.get(id=request.session['did'])
        ob1.firstname = firstname
        ob1.lastname = lastname
        ob1.place = place
        ob1.post = post
        ob1.pin = pin
        ob1.phno = phno
        ob1.license = license
        ob1.email = email
        ob1.gender = gender
        ob1.dob = dob
        ob1.image = fp
        ob1.OWNER = ownerTbl.objects.get(LOGIN_id=request.session['lid'])
        ob1.save()

        return HttpResponse(
            '''<script>alert('Driver Added');window.location='/owner_add_and_manage_driver';</script>''')
    else:
        ob1 = driverTbl.objects.get(id=request.session['did'])
        ob1.firstname = firstname
        ob1.lastname = lastname
        ob1.place = place
        ob1.post = post
        ob1.pin = pin
        ob1.phno = phno
        ob1.license = license
        ob1.email = email
        ob1.gender = gender
        ob1.dob = dob
        ob1.OWNER = ownerTbl.objects.get(LOGIN_id=request.session['lid'])
        ob1.save()

        return HttpResponse(
            '''<script>alert('Driver Added');window.location='/owner_add_and_manage_driver';</script>''')


@login_required(login_url='/')
def owner_edit_add_or_manage_insurance(request):
    return render(request,'owner/edit_addormanageinsurance.html')

@login_required(login_url='/')
def owner_edit_boat_details(request):
    return render(request,'owner/edit_boatdetails.html')

@login_required(login_url='/')
def owner_home(request):
    return render(request,'owner/ownerindex.html')


@login_required(login_url='/')
def owner_track_driver(request):
    return render(request,'owner/Trackdriver.html')

@login_required(login_url='/')
def owner_view_more(request):
    return render(request,'owner/View more.html')

@login_required(login_url='/')
def owner_view_boat(request):
    ob=boatTbl.objects.filter(OWNER__LOGIN=request.session["lid"])
    return render(request,'owner/view_boat.html',{"data":ob})

@login_required(login_url='/')
def delete_owner_view_boat(request,id):
    ob=boatTbl.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('Removed');window.location='/owner_view_boat';</script>''')




@login_required(login_url='/')
def owner_view_emergency_notification(request):
    ob=emergencyTbl.objects.filter(DRIVER__OWNER__LOGIN_id=request.session['lid'])
    return render(request,'owner/View_emergencynotification.html',{'val':ob})


@login_required(login_url='/')
def owner_view_feedback(request):
    ob=feedbackTbl.objects.filter(BOAT__OWNER__LOGIN_id=request.session['lid'])
    return render(request,'owner/View_feedback.html',{'val':ob})

@login_required(login_url='/')
def owner_view_complaints_and_send_reply(request):
    ob=complaintTbl.objects.filter(BOAT__OWNER__LOGIN_id=request.session['lid'])
    return render(request,'owner/Viewcomplaints&sendreply.html',{"val":ob})

@login_required(login_url='/')
def owner_sendreply(request,id):
    request.session['cid']=id
    ob=complaintTbl.objects.get(id=id)
    return render(request,'owner/send_reply.html')

@login_required(login_url='/')
def owner_sendreply_post(request):
    reply=request.POST['textfield']
    ob = complaintTbl.objects.get(id=request.session['cid'])
    ob.reply=reply
    ob.save()
    return HttpResponse('''<script>alert('reply send successfully');window.location='/owner_view_complaints_and_send_reply';</script>''')

@login_required(login_url='/')
def owner_view_tripdetails(request,id):
    a=timescheudle.objects.filter(BOAT_id=id)
    print(a)
    return render(request,'owner/owner_view_tripdetails.html',{'data':a})

@login_required(login_url='/')
def owner_add_tripdetails(request,id):
    a=boatTbl.objects.get(id=id)
    b=routeTbl.objects.all()
    return render(request,'owner/owner_add_trip.html',{'data':a,'route':b})

@login_required(login_url='/')
def owner_add_tripdetails_post(request):
    tripname=request.POST['textfield']
    route=request.POST['select']
    id=request.POST['id']
    starttime=request.POST['textfield4']
    endtime=request.POST['textfield3']

    a=timescheudle()
    a.tripname =  tripname
    a.start_time =  starttime
    a.end_time =  endtime
    a.ROUTE= routeTbl.objects.get(id=route)
    a.BOAT= boatTbl.objects.get(id=id)
    a.save()
    return HttpResponse('''<script>alert('Success');window.location='/owner_view_boat';</script>''')

@login_required(login_url='/')
def owner_delete_triptime(request,id):
    a=timescheudle.objects.get(id=id)
    a.delete()
    return HttpResponse('''<script>alert('deleted');window.location='/owner_view_boat';</script>''')

    



# ====================================
def logincode(request):
    print(request.POST,'jhjhjjhhjhjghjgjhfjhhj')
    un = request.POST['username']
    pwd = request.POST['password']
    print(un, pwd)
    try:
        ob = loginTbl.objects.get(username=un, password=pwd)

        if ob is None:
            data = {"task": "invalid"}
        else:
            print("in user function")
            data = {"task": "valid", "lid": ob.id,"type":ob.utype}

        return JsonResponse(data)
    except:
        data = {"task": "invalid"}
        return JsonResponse(data)


def driver_view_profile(request):
    lid = request.POST.get('lid')
    print(lid,'======================++++++++++++++++++====================')
    print('Received Login ID: {}'.format(lid))

    if not lid:
        return JsonResponse({'status': 'error', 'message': 'Login ID not provided'})

    try:
        ob = driverTbl.objects.get(LOGIN_id=lid)
        print('Client record found: {}, Email: {}'.format(ob.firstname, ob.email))

        data = {
            'id':ob.id,
            "Name": ob.firstname,
            "lastName": ob.lastname,
            "Place": ob.place,
            "Post": ob.post,
            "pin": ob.pin,
            "Phone": ob.phno,
            "license": ob.license,
            "gender": ob.gender,
            "Email": ob.email,
            'Image': request.build_absolute_uri(ob.image.url),  # Ensures the image URL is absolute
              # Ensures the image URL is absolute
        }

        return JsonResponse({"status": "ok", "data": data})

    except driverTbl.DoesNotExist:  # Fixed: replaced ob.DoesNotExist with correct model
        print('Client with LOGIN ID={} not found'.format(lid))
        return JsonResponse({"status": "error", "message": "Client not found"})
    except Exception as e:
        print('An error occurred: {}'.format(str(e)))
        return JsonResponse({"status": "error", "message": "An error occurred: {}".format(str(e))})


def view_notification(request):
    lid=request.POST["lid"]
    ob=notificationTbl.objects.filter(DRIVER__LOGIN_id=lid)
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    for i in ob:
        data={'OWNER':i.OWNER.firstname,'notification':i.notification,'date':str(i.date),'id':i.id}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status":"ok","data":mdata})



def view_myassignedboat(request):
    lid=request.POST["lid"]
    ob=assign_table.objects.filter(DRIVER__LOGIN_id=lid)
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    for i in ob:
        data={'BOAT':i.BOAT.name,'regno':str(i.BOAT.regno),'no_of_passengers':i.BOAT.no_of_passengers,'image':str(i.BOAT.image.url),'id':i.id}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status":"ok","data":mdata})


def sendemergency(request):
    comp = request.POST['feedback']
    lid = request.POST['lid']
    lob = emergencyTbl()
    lob.DRIVER = driverTbl.objects.get(LOGIN_id=lid)
    lob.details = comp
    lob.status = 'pending'
    from datetime import datetime
    lob.date = datetime.today().date()  # Fix: Use .date() to store only the date
    lob.time = datetime.today().time()
    lob.save()
    return JsonResponse({'task': 'ok'})

def registrationcode(request):
    print(request.POST,'hgggggggggg')
    name = request.POST['name']
    lname = request.POST['lname']
    place = request.POST['place']
    post = request.POST['post']
    pin = request.POST['pin']
    gender = request.POST['gender']
    phone = request.POST['phone']
    email = request.POST['email']
    dob = request.POST['dob']
    un = request.POST['username']
    pwd = request.POST['password']
    if loginTbl.objects.filter(username=email).exists():
        return JsonResponse({'status': 'no'})

    lob1 = loginTbl()
    lob1.username = un
    lob1.password = pwd
    lob1.utype = 'user'
    lob1.save()

    lob = userTbl()
    lob.firstname = name
    lob.lastname = lname
    lob.place = place
    lob.gender = gender
    lob.post = post
    lob.pin = pin
    lob.dob = dob
    lob.phno = phone
    lob.email = email
    lob.LOGIN = lob1

    lob.save()
    return JsonResponse({'status': 'ok'})


def show_boat(request):
    boats = boatTbl.objects.all()
    boat_info = []

    for boat in boats:
        boat_info.append({
            'id': boat.id,
            'owner': boat.OWNER.id if boat.OWNER else None,
            'name': boat.name,
            'image': request.build_absolute_uri(boat.image.url) if boat.image else None,
            'regno': boat.regno,
            'fitness': boat.fitness.url if boat.fitness else None,
            'no_of_passengers': boat.no_of_passengers,
            'type': boat.type,
            'brand': boat.brand,
            'description': boat.discription,  # Assuming "discription" is a typo of "description"
            'certificate': boat.certificate.url if boat.certificate else None,
            'status': boat.status
        })

    return JsonResponse({'task': 'ok', 'data': boat_info})

def sendrating2(request):
    print(request.POST)
    rating = request.POST['rating']
    review = request.POST['review']
    did = request.POST['bid']
    lid = request.POST['lid']
    lob = feedbackTbl()
    lob.USER = userTbl.objects.get(LOGIN_id=lid)
    lob.BOAT = boatTbl.objects.get(id=did)
    lob.rating = rating
    lob.feedback = review
    import datetime
    lob.date = str(datetime.datetime.now().date().today())
    lob.save()
    return JsonResponse({'status': 'ok'})


def sendcomplaint(request):
    print(request.POST)
    complaint_description = request.POST['complaint']
    did = request.POST['bid']
    lid = request.POST['lid']
    complaint = complaintTbl()
    complaint.USER = userTbl.objects.get(LOGIN_id=lid)
    complaint.BOAT = boatTbl.objects.get(id=did)
    complaint.complaint = complaint_description
    complaint.reply = 'pending'
    import datetime
    complaint.date = str(datetime.datetime.now().date())
    complaint.save()
    return JsonResponse({'status': 'ok'})


def delete_complaint(request):
    comp_id = request.POST.get('comp_id')

    try:
        complaint = complaintTbl.objects.get(id=comp_id)
        complaint.delete()
        return JsonResponse({'status': 'ok', 'message': 'Complaint deleted successfully.'})
    except complaintTbl.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Complaint not found.'})




def viewreply(request):
    lid=request.POST["lid"]
    ob=complaintTbl.objects.filter(USER__LOGIN_id=lid)
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    for i in ob:
        data={ 'reply': i.reply,
            'uname': i.USER.firstname,
            'boat_name': i.BOAT.name,  # Assuming the boat name is stored in the 'name' field of boatTbl
            'date': str(i.date),
            'id': i.id,
            'complaints': i.complaint}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status":"ok","data":mdata})

def and_view_profile(request):
    lid = request.POST.get('lid')
    print(lid, '======================++++++++++++++++++====================')
    print('Received Login ID: {}'.format(lid))

    if not lid:
        return JsonResponse({'status': 'error', 'message': 'Login ID not provided'})

    try:
        # Fetch the user record based on the LOGIN_id
        ob = userTbl.objects.get(LOGIN_id=lid)
        print('Client record found: {} {}'.format(ob.firstname, ob.lastname))

        # Prepare the data dictionary with the required fields
        data = {
            'id': ob.id,
            "First Name": ob.firstname,
            "Last Name": ob.lastname,
            "Gender": ob.gender,
            "DOB": ob.dob,
            "Place": ob.place,
            "Post": ob.post,
            "Pin": ob.pin,
            "Phone": ob.phno,
            "Email": ob.email,
        }

        return JsonResponse({"status": "ok", "data": data})

    except userTbl.DoesNotExist:
        print('Client with LOGIN ID={} not found'.format(lid))
        return JsonResponse({"status": "error", "message": "Client not found"})
    except Exception as e:
        print('An error occurred: {}'.format(str(e)))
        return JsonResponse({"status": "error", "message": "An error occurred: {}".format(str(e))})




def qrscanandview(request):
    print(request.POST,"jjjjjjjjjjjjj")
    code=request.POST['code']
    boats = boatTbl.objects.filter(id=code)
    boat_info = []

    for boat in boats:
        boat_info.append({
            'id': boat.id,
            'owner': boat.OWNER.id if boat.OWNER else None,
            'name': boat.name,
            'image': request.build_absolute_uri(boat.image.url) if boat.image else None,
            'regno': boat.regno,
            'fitness': boat.fitness.url if boat.fitness else None,
            'no_of_passengers': boat.no_of_passengers,
            'type': boat.type,
            'brand': boat.brand,
            'description': boat.discription,  # Assuming "discription" is a typo of "description"
            'certificate': boat.certificate.url if boat.certificate else None,
            'status': boat.status
        })

    return JsonResponse({'task': 'ok', 'data': boat_info})



def updatelocation(request):
    print(request.POST,"jjj")
    lid=request.POST['lid']
    tid=request.POST['lat']
    com=request.POST['lon']
    res = locationTbl.objects.filter(DRIVER__LOGIN__id=lid)
    if len(res) == 0:
        qry=locationTbl()
        qry.DRIVER=driverTbl.objects.get(LOGIN__id=lid)
        qry.longitude=com
        qry.latitude=tid
        qry.save()
        return JsonResponse({'task': 'success'})
    else:
        on = locationTbl.objects.get(DRIVER__LOGIN__id=lid)
        on.longitude = com
        on.latitude = tid
        on.save()
        return JsonResponse({'task': 'success'})
