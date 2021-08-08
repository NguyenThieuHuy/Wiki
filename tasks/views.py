import markdown2
import secrets

from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.shortcuts import render

from . import util
from markdown2 import Markdown


class NewTaskForm(forms.Form):
    subject = forms.CharField(label="Your title", widget=forms.TextInput(attrs={'class' : 'form-control col-md-8'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class' : "form-control col-md-10", 'rows' : 20}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

# Create your views here.

def index(request):
    return render(request, "tasks/index.html",{
        "entries": util.list_entries()
    })

def entry(request, entry):
    markdowner = Markdown()
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "tasks/none.html", {
            "entrySubject": entry    
        })
    else:
        return render(request, "tasks/subject.html", {
            "entry": markdowner.convert(entryPage),
            "entrySubject": entry
        })

def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            content = form.cleaned_data["content"]
            if(util.get_entry(subject) is None or form.cleaned_data["edit"] is True):
                util.save_entry(subject,content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': subject}))
            else:
                return render(request,"tasks/add.html",{
                "form": form,
                "existing": True,
                "entry": subject
            })
        else:
            return render(request,"tasks/add.html",{
            "form": form,
            "existing": False
        })
    return render(request,"tasks/add.html",{
        "form": NewTaskForm(),
        "existing": False
    })

def edit(request, entry):
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "tasks/none.html", {
            "entrySubject": entry    
        })
    else:
        form = NewTaskForm()
        form.fields["subject"].initial = entry     
        form.fields["content"].initial = entryPage
        form.fields["edit"].initial = True
        return render(request, "tasks/add.html", {
            "form": form,
            "edit": form.fields["edit"].initial,
            "entrySubject": form.fields["subject"].initial
        })    


def delete(request):
        form = NewTaskForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            if(form.cleaned_data["edit"] is True):
                util.delete_entry(subject)
                return render(request, "tasks/index.html",{
            "entries": util.list_entries()})
            
def random(request):
    entries = util.list_entries()
    if entries == []:
        return render(request, "tasks/none.html")
    else:
        entry = secrets.choice(entries)
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': entry}))



def search(request):
    value = request.GET.get('q')
    if(util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': value }))
    else:
        subStringEntries = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                subStringEntries.append(entry)

        return render(request, "tasks/index.html", {
        "entries": subStringEntries,
        "search": True,
        "value": value
    })    