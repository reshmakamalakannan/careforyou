from django.http import HttpResponseRedirect
def my_login_required(function):
	def wraper(request, *args, **kwargs):
		#Check if the Session exists the login key.Here the user_id
		if 'u_id' not in request.session.keys():
			return HttpResponseRedirect("/userlogin")
		else:
			return function(request, *args, **kwargs)
        
	wraper.__doc__=function.__doc__
	wraper.__name__=function.__name__
	return wraper
def email_required(function):
	def wraper(request, *args, **kwargs):
		if 'useremail' not in request.session.keys():
			return HttpResponseRedirect("/onlyonce")
		else:
			return function(request, *args, **kwargs)
        
	wraper.__doc__=function.__doc__
	wraper.__name__=function.__name__
	return wraper
def admin_login_required(function):
	def wraper(request, *args, **kwargs):
		if 'admin_log' not in request.session.keys():
			return HttpResponseRedirect("/adminlogin")
		else:
			return function(request, *args, **kwargs)
        
	wraper.__doc__=function.__doc__
	wraper.__name__=function.__name__
	return wraper