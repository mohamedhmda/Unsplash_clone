from django.shortcuts import redirect 


class OwnerRequiredMixin(object):
    def dispatch(self,request, *args, **kwargs):
        """ making sure only owner can edit image """
        obj = self.get_object()
        if obj.user != self.request.user:
            return redirect(obj)
        return super(OwnerRequiredMixin, self).dispatch(request, *args, **kwargs)

class UserEditMixin(object):
    def dispatch(self,request, *args, **kwargs):
        """ making sure only owner can edit image """
        obj = self.get_object()
        if obj != self.request.user:
            return redirect(obj)
        return super(UserEditMixin, self).dispatch(request, *args, **kwargs)
