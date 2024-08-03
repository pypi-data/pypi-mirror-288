import uuid

from sqlalchemy import String


class ModelRepository:
    def __init__(self, model):
        self._model = model
        self._session = None
        self._logger = None

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, logger):
        self._logger = logger

    @property
    def model(self):
        return self._model

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, session):
        self._session = session

    def _filter(self, filter_json, page=1, limit=200):
        filters = self.dict_filters_to_model(self.model, filter_json)
        query = self.session.query(self.model)
        total_items = query.filter(*filters).count()
        total_pages = total_items // limit + (1 if total_items % limit > 0 else 0)
        query = query.filter(*filters).offset(limit * (page - 1)).limit(limit)
        items = query.all()
        return self._paginate(
            total_items=total_items,
            count=len(items),
            page=page,
            limit=limit,
            total_pages=total_pages,
            next_page=page + 1 if page < total_pages else None,
            previous_page=page - 1 if page > 1 else None,
            data=[item.to_dict() for item in items],
        )

    def _paginate(self, total_items, count, page, limit, total_pages, next_page, previous_page, data):
        return {
            'total_items': total_items,
            'count': count,
            'page': page,
            'limit': limit,
            'total_pages': total_pages,
            'next_page': next_page,
            'previous_page': previous_page,
            'data': data,
        }

    def _query(self, model, filter_by, serialize=True, fetch_all=False, related_entities=None, page=None, limit=None):
        query = self.session.query(model)

        if related_entities:
            query = query.options(related_entities)

        query = query.filter_by(**filter_by)

        if fetch_all:
            if page is not None and limit is not None:
                records, total_items, total_pages, next_page, previous_page = self._paginate_query(query, page, limit)
                if serialize:
                    records = [record.to_dict() for record in records]
                return self._paginate(
                    total_items=total_items,
                    count=len(records),
                    page=page,
                    limit=limit,
                    total_pages=total_pages,
                    next_page=next_page,
                    previous_page=previous_page,
                    data=records
                )

            records = query.order_by(model.last_updated_at.desc()).limit(500).all()
            if serialize:
                return [record.to_dict() for record in records]
            return records

        record = query.first()
        if serialize:
            return record.to_dict() if record else {}
        return record

    def _paginate_query(self, query, page, limit):
        total_items = query.count()
        total_pages = total_items // limit + (1 if total_items % limit > 0 else 0)
        query = query.offset((page - 1) * limit).limit(limit)
        items = query.all()
        return items, total_items, total_pages, page + 1 if page < total_pages else None, page - 1 if page > 1 else None

    @staticmethod
    def dict_filters_to_model(model, filters=None, default_filters=None):
        created_filters = default_filters or []

        if filters is None:
            return created_filters

        for key, value in filters.items():
            column = getattr(model, key)

            if isinstance(value, list):
                first_value = value[0] if len(value) > 0 else None
                second_value = value[1] if len(value) > 1 else None

                if first_value is None and second_value is None:
                    continue

                if first_value and not second_value:
                    created_filters.append(column >= first_value)
                elif not first_value and second_value:
                    created_filters.append(column <= second_value)
                elif first_value and second_value:
                    created_filters.append(column.between(first_value, second_value))
            else:
                if value is None or value == '':
                    continue
                if isinstance(column.type, String):
                    created_filters.append(column.ilike(f"%{value}%"))
                else:
                    created_filters.append(column == value)

        return created_filters

    def generate_id(self):
        return str(uuid.uuid4())
