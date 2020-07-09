from django.shortcuts import render
from django.http import HttpResponse
import paramiko

def Homepage(request):
	context = {}
	if request.method=='POST':
		server = request.POST.get('server')
		username = request.POST.get('username')
		password = request.POST.get('password')
		port = request.POST.get('port')
		command = request.POST.get('command')
		context['server'] = server
		context['username'] = username
		context['password'] = password
		context['port'] = port
		print('------------request after-----------',server,username,password,port,command)
		try:
			p = paramiko.SSHClient()
			p.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			p.connect(server, port=22, username=username, password=password)
			stdin, stdout, stderr = p.exec_command(command)
			opt = stdout.readlines()
			opt = "".join(opt)
			context['shell_output'] = opt
		except Exception as e:
			context['shell_output'] = f"Error :- {e}"

	return render(request, 'servertool/homepage.html', context)