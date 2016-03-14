from django.shortcuts import render

def safe_text(text):
    text = text.replace("\r","")
    text = text.replace("\n","")
    text = text.replace('"',"'")
    text = text.replace("\\","\\\\")
    return text

# submit_url = url that the editor form submits to
# serialized_form_data = json-serialized data stored in "value" field of submission form
# header = title to display
# initial_text = intial text in the submission form
# editor.html itself submits a form with two POST variables:
#   form-text, the text of the form
#   serialized-form-data, a json serialized string
def editor(request,submit_url,serialized_form_data,header,initial_text):
    # Make sure we strip out all escape characters
    initial_text = safe_text(initial_text)
    context={'submit_url':submit_url, \
             'serialized_form_data':serialized_form_data, \
             'header':header, \
             'initial_text':initial_text, \
            }
    return render(request, 'MCEditor/editor.html', context)

# This is an example of how you might call the text editor
def example(request):
    html = editor(request,"/",{'a','b'},"Example editor form","initial text")
    return html
