from django.shortcuts import render, redirect
import openai
from .models import Past
from django.contrib import messages
from django.core.paginator import Paginator

def home(request):

    #check for for submission
    if request.method == "POST":
        question = request.POST['question']
        past_responses = request.POST['past_responses']

        # API
        # set api key
        openai.api_key = "PASTE YOUR KEY"
        # create openai instance
        openai.Model.list()
        try: 
            # make a completion (= request)
            response = openai.Completion.create(
                model = "text-davinci-003",
                prompt = question,
                temperature = 0, # accuracy
                max_tokens = 300,
                top_p = 1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )

            # parse response
            response = (response["choices"][0]["text"]).strip()

            # Logic for past responses
            if "3123sjkdahsjd" in past_responses:
                past_responses = response
            else:
                past_responses = f"{past_responses}<br/><br/>{response}"

            # save to database
            record = Past(question=question, answer=response)
            record.save()

            return render(request, 'home.html', {"question":question, "response":response, "past_responses":past_responses})
        except Exception as e:
            return render(request, 'home.html', {"question":question, "response":e, "past_responses":past_responses})
    return render(request, 'home.html', {})

def past(request):
    # set up pagination
    p = Paginator(Past.objects.all(), 8)
    page = request.GET.get('page')
    pages = p.get_page(page) 

    # query the database
    past = Past.objects.all()
    
    # get nb of pages
    nums = "a" * pages.paginator.num_pages
    
    return render(request, 'past.html', {"past":past, "pages":pages, "nums":nums})

def delete_past(request, Past_id):
    past = Past.objects.get(pk=Past_id)
    past.delete()
    messages.success(request, ("The question and answer deleted"))
    return redirect('past')
