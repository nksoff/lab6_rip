from django.shortcuts import render
from django.views import View

from lab.models import Tutor, Course
from django.db.models import Count

import random

def main(request):
    tutors = Tutor.objects.all()

    if len(tutors) == 0:
        for i in range(0, 10):
            t = Tutor.objects.create(lastname="Lastname " + str(i),
                                 firstname="Firstname " + str(i),
                                 middlename="Middlename " + str(i),
                                 birthday=str(random.randint(1950, 2000)) + "-09-01",
                                 sex=random.randint(1,10) > 5)
            t.save()

            for j in range(0, random.randint(1,6)):
                c = Course.objects.create(name="Course # {} of tutor {}".format(j, t.id),
                                          full_name="Course fullname",
                                          tutor=t)
                c.save()

    tutors = Tutor.objects.all()

    return render(request, 'main.html', {
        'tutors': tutors
    })


class TutorView(View):
    def get(self, request, id):
        tutor = Tutor.objects.get(id=int(id))

        courses = Course.objects.filter(tutor=tutor).all()

        return render(request, 'tutor.html', {
            'tutor': tutor,
            'courses': courses
        })
