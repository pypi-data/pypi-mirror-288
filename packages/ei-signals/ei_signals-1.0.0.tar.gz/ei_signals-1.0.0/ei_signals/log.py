from django.views.debug import ExceptionReporter
import json
class CustomExceptionReporter(ExceptionReporter):
    def get_traceback_data(self):
        data = super().get_traceback_data()
        
        #remove settings
        del data['settings']
        del data['filtered_POST_items']
        # print(data['filtered_POST_items'])
        #add body if it exists
        if self.request is not None:
            if self.request.method == "POST":
                try:
                    data['filtered_POST_items'] = [("post_body", json.loads(self.request.body)), ("post_data", self.request.POST)]
                except:
                    data['filtered_POST_items'] = None
        return data