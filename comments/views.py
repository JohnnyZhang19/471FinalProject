from django.shortcuts import render, get_object_or_404, redirect

from project.models import Bloginfo
from .forms import CommentForm


def do_comments(request, blogid):
    project = get_object_or_404(Bloginfo, pk=blogid)

    if request.method == 'POST':
        formobj = CommentForm(request.POST)
        if formobj.is_valid():
            #object cannot commit
            comment = formobj.save(commit=False)
            comment.name = request.user.nickname
            comment.email = request.user.email
            comment.blog = project

            #commit to database
            comment.save()

            return redirect(project)
        else:
            context = {
                "project": project,
                'form': formobj,
            }
            return render(request, 'project/blogDetail.html', context=context)
    else:
        return redirect(project)
