from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CreateCourse, AddVideos, AddNotes, AddCourseOverview
from django.contrib.auth.decorators import login_required
from .models import *
from accounts.models import NewslettersSubscribers
from django.views.decorators.csrf import csrf_exempt

from Paytm import Checksum
from accounts.models import Account

MERCHANT_KEY = '15Oo@vdvanPfefG!'


def room(request):
    pass


def index(request):
    context = {
        'categories': Category.objects.all(),
        'courses': Course.objects.all(),
        'frequently_ask_questions': FrequentlyAskQuestion.objects.all(),
        'latest_course': Course.objects.all().order_by('date_of_created')
    }

    if request.method == "POST":
        email = request.POST.get('news_email')
        user = NewslettersSubscribers.objects.create(email=email)
        return redirect('home')

    return render(request, 'main/index.html', context)


def courseListView(request):
    context = {
        'objects': Course.objects.all()
    }
    return render(request, 'main/course_list.html', context)

@login_required
def user_courseListView(request):
    user = request.user
    context = {
        'objects': Course.objects.filter(member=user)
    }
    return render(request, 'main/purchase_course.html', context)


def courseDetailView(request, slug):
    course = Course.objects.get(slug=slug)

    related_cat = course.category
    related_courses = Course.objects.filter(category=related_cat)
    demo_video = course.video_lectures.get(index=0)

    context = {
        'related_courses': related_courses,
        'course': course,
        'videos': course.video_lectures.all(),
        # 'notes':course.notes.all(),
        'demo_video': demo_video.video_url,
    }
    print(demo_video, 222222222)
    return render(request, 'main/course-details.html', context)


@login_required
def course_detail_view_for_purchase_user(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    current_user = request.user
    member_of_course = course.member.all()
    if (current_user not in member_of_course):
        """redirect with error message and tell user to purchase the course"""
        return redirect('checkout', course_slug)

    context = {
        'course': course,
        # 'videos': Video_Lecture.objects.filter(course__slug=course_slug),
        # 'notes':Notes.objects.filter(course__slug=course_slug),
    }
    return render(request, 'main/purchase_user_course.html', context)


@login_required
def course_videos_for_purchase_user(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    current_user = request.user
    member_of_course = course.member.all()
    if (current_user not in member_of_course):
        """redirect with error message and tell user to purchase the course"""
        return redirect('checkout', course_slug)

    context = {
        'course': course,
        'videos': Video_Lecture.objects.filter(course__slug=course_slug).order_by('index'),
        # 'notes':Notes.objects.filter(course__slug=course_slug),
    }
    return render(request, 'main/purchase_user_course-videos.html', context)


@login_required
def course_notes_for_purchase_user(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    current_user = request.user
    member_of_course = course.member.all()
    if (current_user not in member_of_course):
        """redirect with error message and tell user to purchase the course"""
        return redirect('checkout', course_slug)

    context = {
        'course': course,
        # 'videos': Video_Lecture.objects.filter(course__slug=course_slug).order_by('index'),
        'notes': Notes.objects.filter(course__slug=course_slug).order_by('index'),
    }
    return render(request, 'main/purchase_user_course-notes.html', context)


@login_required
def createCourse(request):
    form = CreateCourse()
    slug = ""
    current_faculty_user = Faculty.objects.get(user=request.user)
    if current_faculty_user is None:
        messages.warning(request, "Sorry You are not allow to create course")
        return redirect('login')

    if request.method == "POST":
        form = CreateCourse(request.POST or None, request.FILES or None)
        if form.is_valid():
            course = form.save(commit=False)
            course.faculty = current_faculty_user
            course.save()
            slug = course.slug
            # redirect('course_detail',course_.slug)
            return redirect('add_videos_to_course', slug)

    context = {
        'form': form,
    }
    return render(request, 'classroom/course_create.html', context)


@login_required
def addVideosToCourse(request, course_slug):
    current_course = Course.objects.get(slug=course_slug)
    current_faculty_user = Faculty.objects.get(user=request.user)
    if current_faculty_user is None:
        messages.warning(request, "Sorry You are not allow to make any changes")
        return redirect('login')

    if current_course.faculty != current_faculty_user:
        messages.warning(request, "Sorry You Can't Make nay changes")
        return redirect('home')

    form = AddVideos()
    if request.method == "POST":
        form = AddVideos(request.POST or None, request.FILES or None)
        if form.is_valid():
            video = form.save(commit=False)
            video.save()
            current_course.video_lectures.add(video)
            current_course.save()
            messages.info(request, "Videos are successfully added to course")
            return redirect('course_detail', course_slug)
    context = {
        'form': form,
        'course': current_course,
    }
    return render(request, 'classroom/course_add_videos.html', context)


@login_required
def addNotesToCourse(request, course_slug):
    current_course = Course.objects.get(slug=course_slug)
    current_faculty_user = Faculty.objects.get(user=request.user)
    if current_faculty_user is None:
        messages.warning(request, "Sorry You are not allow to make any changes")
        return redirect('login')

    if current_course.faculty != current_faculty_user:
        messages.warning(request, "Sorry You Can't Make nay changes")
        return redirect('home')

    form = AddNotes()
    if request.method == "POST":
        form = AddNotes(request.POST or None, request.FILES or None)
        if form.is_valid():
            notes = form.save(commit=False)
            notes.save()
            current_course.notes_un.add(notes)
            current_course.save()
            messages.info(request, "Notes are successfully added to course")
            return redirect('course_detail', course_slug)
    context = {
        'form': form,
        'course': current_course,
    }
    return render(request, 'classroom/course_add_notes.html', context)


@login_required
def addCourseOverviewToCourse(request, course_slug):
    current_course = Course.objects.get(slug=course_slug)
    current_faculty_user = Faculty.objects.get(user=request.user)
    if current_faculty_user is None:
        messages.warning(request, "Sorry You are not allow to make any changes")
        return redirect('login')

    if current_course.faculty != current_faculty_user:
        messages.warning(request, "Sorry You Can't Make nay changes")
        return redirect('home')

    form = AddCourseOverview()
    if request.method == "POST":
        form = AddCourseOverview(request.POST or None, request.FILES or None)
        if form.is_valid():
            lines = form.save(commit=False)
            lines.save()
            current_course.course_overview.add(lines)
            current_course.save()
            messages.info(request, "Course Overview are successfully added to course")
            return redirect('course_detail', course_slug)
    context = {
        'form': form,
        'course': current_course,
    }
    return render(request, 'classroom/course_add_course_overview.html', context)




def contactUs(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        message = request.POST.get('message')
        print([name, email, phone_number, message])
        curr_form = ContactForm.objects.create(name=name, email=email, phone_number=phone_number, message=message)
        curr_form.save()

        """Add redirect message"""
        messages.success(request,"Message send successfully")
        return redirect('contact_us')
    return render(request, 'main/contact.html')


def aboutUs(request):
    context={
        'frequently_ask_questions':FrequentlyAskQuestion.objects.all()
    }
    return render(request, 'main/about.html',context)


def internships(request):
    context = {
        'objects': InternshipForm.objects.all()
    }
    return render(request, 'main/internships.html', context)


def internshipDetail(request, id):
    current_object = InternshipForm.objects.get(id=id)
    context = {
        'object': current_object
    }
    return render(request, 'main/internship-detail.html', context)


def checkoutPage(request,course_slug):
	course=Course.objects.get(slug=course_slug)
	context={
		'course':course
	}
	return render(request,'main/checkout.html',context)


@login_required
def checkout(request,course_slug):
    course = Course.objects.get(slug=course_slug)
    context = {
        'course': course
    }
    if request.method == 'POST':
        user=request.user

        # amount = request.POST.get('amount')
        amount = float(course.price)




        orderid = random.randrange(11111, 99999)
        param_dict = {
            'MID': 'XouRsh60629205732669',
            'ORDER_ID': str(orderid),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': user.email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': f'http://127.0.0.1:8000/course/handlerequest/{course_slug}/{user.username}',
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'paytm/paytm.html', {'param_dict': param_dict})

    # return render(request, 'paytm/checkout.html')

    return render(request, 'main/checkout.html', context)


@csrf_exempt
def handlerequest(request,course_slug,username):
    user=Account.objects.get(username=username)
    for _ in range(10):
        print("hello")
        print(user.email)
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            course = Course.objects.get(slug=course_slug)
            # user=request.user
            name = 'name'
            email = user.email
            mobile = user.phone_number
            amount = float(course.price)
            order = Transaction.objects.create(user=user, item_json=course.name, course=course, name=name,
                                               email=email, mobile=mobile, amount=float(amount))
            order.save()
            course.member.add(user)
            course.save()
            messages.success(request,"Course is successfully purchase")
            return redirect("purchase_course")
            # print('order successful')
            # print('order successful')
            # print('order successful')
            # print('order successful')
            # print('order successful')
            # print('order successful')
            # print('order successful')

        else:
            messages.error(request, "Something Went Wrong")
            return redirect("checkout",course_slug)
            # print('Something went wrong' + response_dict['RESPMSG'])
    return render(request, 'paytm/paytm_payment_status.html', {'response_dict': response_dict})
