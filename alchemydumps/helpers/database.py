# coding: utf-8
from sqlalchemy.ext.serializer import dumps, loads


class AlchemyDumpsDatabase(object):

    def __init__(self, base, db_session):
        self.base = base
        self.db_session = db_session
        self.do_not_backup = list()

    def get_mapped_classes(self):
        """Gets a list of SQLALchemy mapped tables"""
        return [
            model_class
            for model_class in self.base._decl_class_registry.values()
            if (
                model_class not in self.do_not_backup
                and hasattr(model_class, '__table__')
            )
        ]

    def get_data(self):
        """Go through every mapped table and dumps the data"""
        data = dict()
        for model_class in self.get_mapped_classes():
            query = self.db_session.query(model_class)
            data[model_class.__name__] = dumps(query.all())
        return data

    def parse_data(self, contents):
        """Loads a dump and convert it into rows """
        return loads(contents, self.base.metadata, self.db_session)
