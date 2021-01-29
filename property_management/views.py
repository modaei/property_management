from django.http import HttpResponse
from django.http import HttpResponseForbidden


def media_access(request, path):
    user = request.user

    if user.is_anonymous:
        return HttpResponseForbidden()

    if user.is_staff:
        access = True
    else:
        access = False
        # # For simple user, only their documents can be accessed
        # user_documents = [
        #     user.identity_document,
        #     # add here more allowed documents
        # ]
        #
        # for doc in user_documents:
        #     if path == doc.name:
        #         access_granted = True

    if access:
        response = HttpResponse()
        del response['Content-Type']
        response['X-Accel-Redirect'] = '/protected/media/' + path
        return response
    else:
        return HttpResponseForbidden()
