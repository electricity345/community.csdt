import json
import logging
import math

from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden, HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config

from community_csdt.src.models.galleries import *

class GalleriesView(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    # Resource url = "/galleries" - Shows a table of all classrooms that are viewable to the public
    @view_config(context='community_csdt.src.models.galleries.gallery.Gallery', name='', renderer='galleries.mako')
    def getGalleries(self):
        log = logging.getLogger('csdt')
        log.info("galleries_view.getGalleries()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        return {'path_url':self.request.path_url, 'session':session}

    # Resource url = "/galleries/all-tables" - Returns all of the classrooms that are viewable to the public
    @view_config(context='community_csdt.src.models.galleries.gallery.Gallery', name='all-tables', renderer='json', xhr=True)
    def getGalleriesTable(self):
        log = logging.getLogger('csdt')
        log.debug("galleries_view.getGalleriesTable()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))
    
        # JqGrid initialization of the table
        if "rows" not in self.request.params or "sidx" not in self.request.params or "sord" not in self.request.params or "page" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()
    
        rows = int(self.request.params['rows'])
        log.debug("rows = %d" % rows)
        num_records = int(self.context.getNumOfAllActiveClasses())
        log.debug("num_records = %d" % num_records)

        total_pages = int(math.ceil((num_records / float(rows))))
        log.debug("total - number of pages = %d" % total_pages)

        sort_name = self.request.params['sidx']
        sort_order = self.request.params['sord']
    
        page_loc = int(self.request.params['page'])
        begin_index = (page_loc - 1) * rows
        end_index = begin_index + rows
        log.debug("begin index value = %d" % begin_index)
        log.debug("end index value = %d" % end_index)
    
        if end_index > num_records:
            end_index = num_records

        class_list = self.context.getAllActiveClasses(sort_name, sort_order)
        class_list = class_list[begin_index:end_index]

        class_list_hash = {}
        class_list_hash['page'] = page_loc
        class_list_hash['total'] = total_pages
        class_list_hash['records'] = num_records
        class_list_hash['results'] = class_list

        for k, v in class_list_hash.iteritems():
            log.debug("key = %s value = %s" % (k, v))
  
        json_dump = json.dumps(class_list_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)


