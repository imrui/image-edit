# -*- coding: utf-8 -*-
import os
import uuid
import tornado.web
from tornado.httputil import HTTPHeaders, _parse_header
from handlers.base_handler import BaseHandler
from werkzeug.utils import secure_filename


class SiteHandler(tornado.web.StaticFileHandler):

    def data_received(self, chunk):
        pass

    def initialize(self, path, default_filename=None):
        self.dirname, self.filename = os.path.split(path)
        super(SiteHandler, self).initialize(self.dirname)

    def get_modified_time(self):
        return None

    def get(self, path=None, include_body=True):
        super(SiteHandler, self).get(self.filename, include_body)


@tornado.web.stream_request_body
class UploadHandler(BaseHandler):
    """
    only one file can upload
    """
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.filename = ''
        self.temp_file_path = ''
        self.file = None
        self.last = None
        self.boundary = None
        self.final_boundary_index = None
        self.len_final = 0

    def prepare(self):
        content_type = self.request.headers['Content-Type']
        fields = content_type.split(";")
        for field in fields:
            k, sep, v = field.strip().partition("=")
            if k == "boundary" and v:
                self.boundary = b'--' + v.encode('utf-8') + b'\r\n'
                self.final_boundary_index = b'\r\n--' + v.encode('utf-8') + b'--\r\n'
                break
        self.temp_file_path = None
        self.last = b''
        self.len_final = len(self.final_boundary_index)

    def post(self, category):
        pass

    def data_received(self, chunk):
        b = 0
        if chunk.startswith(self.boundary):
            i = chunk.find(b'\r\n\r\n')
            if i != -1:
                b = i + 4
                headers = HTTPHeaders.parse(chunk[len(self.boundary):i].decode("utf-8"))
                disp_header = headers.get("Content-Disposition", "")
                _, disp_params = _parse_header(disp_header)
                filename = disp_params["filename"]
                ext = filename.split('.')[-1]
                self.filename = filename
                self.temp_file_path = os.path.join(self.tmp_path, 'uploading_file_%s.%s' % (str(uuid.uuid4()), ext))
                self.file = open(self.temp_file_path, 'wb')
        e = chunk.rfind(self.final_boundary_index)
        if e == -1:
            e = len(chunk)
            if e > (self.len_final - 1):
                temp = self.last + chunk[:self.len_final - 1]
            else:
                temp = self.last + chunk[:e]
            last_index = temp.find(self.final_boundary_index)
            if last_index != -1:
                e = last_index - self.len_final + 1
        if len(chunk) > self.len_final:
            self.last = chunk[-self.len_final + 1:]
        else:
            self.last = chunk
        if self.file:
            self.file.write(chunk[b:e])
            if e < len(chunk):
                self.file.close()
                self.uploaded_done()

    def uploaded_done(self):
        category = self.path_kwargs.get('category')
        directory = str(uuid.uuid4())
        to = os.path.join(self.media_path, 'upload', category, directory)
        if not os.path.exists(to):
            os.makedirs(to)
        filename = secure_filename(self.filename)
        real = os.path.join(to, filename)
        os.rename(self.temp_file_path, real)
        self.write({'filename': filename, 'directory': directory, 'category': category})

    def on_finish(self):
        if self.file:
            self.file.close()
        if self.temp_file_path and os.path.exists(self.temp_file_path):
            os.remove(self.temp_file_path)
