from django.http import HttpResponse
from django.http import HttpResponseForbidden, HttpResponseNotFound
from properties.models import Photo, Property

# This view is NOT a part of the REST API. It is used for
#  serving and access management of property media files.
def media_access(request, media_type='photo', filename=None):
    user = request.user

    if user.is_anonymous:
        return HttpResponseForbidden()

    if user.is_staff:
        access = True
    else:
        access = False
        # For photos, find the related Photo object and then the Property object. If property is not none and it
        # belongs to the same user, grant access
        if media_type == 'photo':
            photo = Photo.objects.filter(image=filename).first()
            if photo is not None and photo.property.user == user:
                access = True
        # For thumbnails, find the related property, if it's not none and belongs to the same user, grant access
        elif media_type == 'thumbs':
            property_obj = Property.objects.filter(thumbnail_image=filename).first()
            if property_obj is not None and property_obj.user == user:
                access = True
        else:
            return HttpResponseNotFound()

    # If access is granted redirect to the proper internal url, otherwise return forbidden response.
    # Photos are stored directly in the media folder, but thumbnails are in thumbs sub folder
    if access:
        if media_type == 'photo':
            redirect_path = '/protected/media/' + filename
        else:
            redirect_path = f'/protected/media/{media_type}/' + filename

        response = HttpResponse()
        del response['Content-Type']
        response['X-Accel-Redirect'] = redirect_path
        return response
    else:
        return HttpResponseForbidden()
