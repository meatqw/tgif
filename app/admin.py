from app import db, manager, admin_, config, models
from datetime import datetime, timedelta
from flask_admin.contrib.sqla import ModelView
from flask_admin import form
import random
import os

# admin models init
# admin.add_view(ModelView(News, db.session))

class StorageAdminModel(ModelView):
    form_extra_fields = {
        'img': form.FileUploadField('Img', base_path=config.media_path)
    }

    def _change_path_data(self, _form):
        try:
            storage_file = _form.file.data

            if storage_file is not None:
                hash = random.getrandbits(128)
                ext = storage_file.filename.split('.')[-1]
                path = '%s.%s' % (hash, ext)

                storage_file.save(
                    os.path.join(config.media_path, path)
                )

                _form.img.data = path
                # _form.path.img = path
                # _form.type.img = ext

                del _form.file

        except Exception as ex:
            pass

        return _form

    def edit_form(self, obj=None):
        return self._change_path_data(
            super(StorageAdminModel, self).edit_form(obj)
        )

    def create_form(self, obj=None):
        return self._change_path_data(
            super(StorageAdminModel, self).create_form(obj)
        )


admin_.add_view(StorageAdminModel(models.News, db.session))