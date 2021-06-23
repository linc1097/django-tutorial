from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views import generic
from .models import Question, Choice
from django.utils import timezone

class IndexView (generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # returns last five published questioins

        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        # returns last five published questioins

        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    try:
            selected_choice = question.choice_set.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        #display the question voting form again
        return render(request, 'polls/detail.html', {
            'question':question, 'error_message': 'You did not select a choice',
            })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        #Always return an HttpResponseRedirect after successfully dealing with POST data.
        #This prevents data from being posted twice if a user hits the BACK button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))



#The hard way vvvvvvvvv            The easy way ^^^^^^^^^^^^^




# def index(request):
#     #latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     #template = loader.get_template('polls/index.html')
#     #context = {
#     #    'latest_question_list':latest_question_list,
#     #}
#     #return HttpResponse(template.render(context, request))
#     # shortcut:

#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)

# def detail(request, question_id):
#     #try:
#     #    question = Questions.objects.get(id=question_id)
#     #except Question.DoesNotExist:
#     #    raise Http404("Question does not exist")
#     #return render(request, 'polls/detail.html', {'question':question})
#     # equivalently:

#     question = get_object_or_404(Question, id=question_id)
#     return render(request, 'polls/detail.html', {'question':question})

# def results(request, question_id):
#     question = get_object_or_404(Question, id=question_id)
#     return render(request, 'polls/results.html', {'question':question})

# def vote(request, question_id):
#     question = get_object_or_404(Question, id=question_id)
#     try:
#         selected_choice = question.choice_set.get(id=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         #display the question voting form again
#         return render(request, 'polls/detail.html', {
#             'question':question, 'error_message': 'You did not select a choice',
#             })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         #Always return an HttpResponseRedirect after successfully dealing with POST data.
#         #This prevents data from being posted twice if a user hits the BACK button.
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
