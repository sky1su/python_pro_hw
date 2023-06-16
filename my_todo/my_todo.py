#!/usr/bin/env python3
import argparse
import json
import os
from dataclasses import dataclass


@dataclass
class task_db:
    db_workdir: str
    db_file_path: str
    db_file: str
    task_data: json

    def __init__(self, file_name: str='task_db.json') -> None:
        self.db_file = file_name
        self.db_workdir = os.getcwdb().decode()
        self.db_file_path = os.path.join(self.db_workdir,self.db_file)
        self.task_data = self.read_data()

    def get_db_path(self) -> str:
        return self.db_file_path

    def read_data(self) -> list:
        mode = 'r' if os.path.exists(self.get_db_path()) else 'w'
        with open(self.get_db_path(), mode, encoding='utf8') as data_file:
            try:
                return (json.load(data_file))
            except:
                return ([])

    def sort_data(self) -> None:
        self.task_data.sort(key=lambda x: x['id'], reverse=True)

    def get_next_index(self) -> int:
        if (len(self.task_data) == 0):
            return(1)
        else:
            return(self.task_data[0]['id']+1)

    def write_data(self) -> None:
        self.sort_data()
        json_data=json.dumps(self.task_data, indent=4, ensure_ascii=False)
        with open(self.get_db_path(), 'w', encoding='utf8') as data_file:
            data_file.write(json_data)
        return None

    def task_add(self, title: str, description: str) -> None:
        task_data = {'title': title,
                     'description': description,
                     'id': self.get_next_index()
                     }
        self.task_data.append(task_data)
        self.write_data()
        return None

    def task_query(self,query: str) -> list:
        task_list = []
        for item in self.task_data:
            if (query in item['title'] + item['description']):
                task_list.append(item)
        return (task_list)

    def task_done(self, task_id: int) -> None:
        count = 0
        for item in self.task_data:
            if (item['id'] == task_id):
                self.task_data.pop(count)
                self.write_data()
            else:
                count += 1
        return None

    def task_count_get(self,count: int) -> list:
        return_data= []
        for i in range(count):
            return_data.append(self.task_data[i])
        return return_data

def print_pretty (data: list):
    """
    Принимает на вход список элементов, выводит в виде отформатированного json
    """
    data_json = json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False)
    print (data_json)

def add_task(args) -> None:
    """
    Добаляет задачу в файл базы данных
    """
    tasks = task_db()
    tasks.task_add(args.title,args.description)
    return None

def show_task(args) -> None:
    """
    выводит на экран последние args.count задач
    """
    tasks = task_db()
    tasks_list = tasks.task_count_get(int(args.count))
    print_pretty(tasks_list)
    return None

def complete_task(args) -> None:
    """
    помечает задачу task_id как выполненную (удаляет из БД)
    :param task_id: номер задачи
    """
    tasks = task_db()
    tasks.task_done(int(args.task_id))
    return None

def find_task(args) -> None:
    """
    Возвращает перечень задач в title или description найдено вхождение query
    :param query: строка, вхождение которой будет проверяться
    """
    tasks = task_db()
    task_list = tasks.task_query(args.query)
    print_pretty(task_list)
    return None

def main():
    """
    Проводит разбор переданных аргументов и вызов соотвествующей функции
     """
    parser = argparse.ArgumentParser(description='my_todo', prog='task manager')
    subparsers = parser.add_subparsers(title='subcommands', help='description')

    parser_add_task=subparsers.add_parser('add', help='add new task')
    parser_add_task.add_argument('title', help='title for new task')
    parser_add_task.add_argument('description', help='description for task')
    parser_add_task.set_defaults(func=add_task)

    parser_find_task=subparsers.add_parser('find', help='find task by substring')
    parser_find_task.add_argument('query', help='substring for query to task db')
    parser_find_task.set_defaults(func=find_task)

    parser_show_task=subparsers.add_parser('show', help='show task')
    parser_show_task.add_argument('count', help='count numbers task for dispaly')
    parser_show_task.set_defaults(func=show_task)

    parser_complete_task=subparsers.add_parser('done', help='mark task as complete and remove from db')
    parser_complete_task.add_argument('task_id', help='id for completed task')
    parser_complete_task.set_defaults(func=complete_task)

    args = parser.parse_args()

    if vars(args):
        args.func(args)
    else:
        parser.print_usage()

if __name__ == '__main__':
    main()