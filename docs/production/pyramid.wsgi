from pyramid.paster import get_app
application = get_app(
	'/home/community/modwsgi/csdt-env/community_csdt/production.ini', 'main')
