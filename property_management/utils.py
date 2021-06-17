from rest_framework.serializers import (IntegerField, )


# This field is able to receive an empty string for an integer field and turn it into a None number
class BlankableIntegerField(IntegerField):
    def to_internal_value(self, data):
        if data == '':
            return None
        return super(BlankableIntegerField, self).to_internal_value(data)


# Converts number of bytes to a human readable format.
def format_file_size(nbytes):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.
        i += 1
    num = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (num, suffixes[i])
