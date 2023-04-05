import csv

from django.core.management.base import BaseCommand

from reviews.models import Title, Genre, Category, GenreTitle, Review, Comment
from users.models import User

class Command(BaseCommand):
    help = 'Import data from CSV to db.sqlite3'
    file_dict = {
        'category': Category,
        'genre': Genre,
        'title': Title,
        'genre_title': GenreTitle,
        'users': User,
        'review': Review,
        'comments': Comment
    }
    
    def handle(self, *args, **options):
        for current_file, model in self.file_dict.items():
            current_file = 'static/data/' + current_file + '.csv'
            with open(current_file, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                total = 0
                for row in reader:
                    if 'genre_title' in current_file:
                        self.id_to_object(row, 'title_id')
                        self.id_to_object(row, 'genre_id')
                    elif 'title' in current_file:
                        self.id_to_object(row, 'category')
                    elif 'review' in current_file:
                        self.id_to_object(row, 'author')
                    elif 'comments' in current_file:
                        self.id_to_object(row, 'author')
                    obj, status = model.objects.get_or_create(**row)
                    if status:
                        total += 1
            print(current_file, ': загружено ', total, ' записей.')
        return 'Operation complete!'

    def id_to_object(self, current_row, field_name):
        id_value = current_row.get(field_name)
        if '_id' in field_name:
            model_name = field_name[:-3]
        elif 'author' in field_name:
            model_name = 'users'
        else:
            model_name = field_name
        model = self.file_dict.get(model_name)
        obj = model.objects.get(id=id_value)
        current_row[field_name] = obj
