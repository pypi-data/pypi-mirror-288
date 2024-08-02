from loguru import logger
from datetime import datetime
import matplotlib.pyplot as plt
import os

class Singleton(type):
	_instance = None

	def __new__(cls, name, based, dct):
		return super().__new__(cls, name, based, dct)
		
	def __call__(cls, *args, **kwargs):
		if cls._instance is None:
			cls._instance = super().__call__(*args, **kwargs)

		return cls._instance
		
class LogScribe(metaclass=Singleton):
	def __init__(self, logfile_dir):
		self.logfile_dir = logfile_dir

	def __current_time(self):
		now = datetime.now()
		date = now.strftime('%d.%m.%Y, %H:%M:%S')

		return date 

	def __if_file_exists(self, logfile_dir):
		if not os.path.exists(logfile_dir):
			logger.error('Logfile directory not exists!')
			return False

		return True

	def __record_title(self, log_level):
		if log_level == 5:
			return 'DEBUG'

		elif log_level == 4:
			return 'INFO'

		elif log_level == 3:
			return 'WARNIGN'

		elif log_level == 2:
			return 'ERROR'

		elif log_level == 1:
			return 'FATAL'

		else:
			return '-'

	def graph(self):
		try:
			logfile_dir = self.logfile_dir
			if not self.__if_file_exists(logfile_dir):
				return {}

			with open(logfile_dir, 'r') as logfile:
				records = logfile.readlines()

			levels = [
				{
					'title': 'DEBUG',
					'values': 0,
					'color': 'blue'
				},
				{
					'title': 'INFO',
					'values': 0,
					'color': 'navy'
				},
				{
					'title': 'WARNIGN',
					'values': 0,
					'color': 'orange'
				},
				{
					'title': 'ERROR',
					'values': 0,
					'color': 'red'
				},
				{
					'title': 'FATAL',
					'values': 0,
					'color': 'grey'
				},
			]

			for index, level in enumerate(levels):
				title = level['title']
				levels[index]['values'] = sum(record.count(title) for record in records)

			titles = [level['title'] for level in levels]
			values = [level['values'] for level in levels]
			colors = [level['color'] for level in levels]

			plt.bar(titles, values, color=colors)
			plt.xlabel('Log Levels')
			plt.ylabel('Level count')
			plt.title('Log Levels Distribution')

			plt.show()
			plt.savefig('statistics.png')

		except Exception as e:
			logger.error(str(e))

		return {}

	def clear(self): 
		try:
			logfile_dir = self.logfile_dir
			if not self.__if_file_exists(logfile_dir):
				return {}

			with open(logfile_dir, 'w') as logfile:
				logfile.write('')

		except Exception as e:
			logger.error(str(e))

		return {}

	def __call__(self, **kwargs):
		try:
			logfile_dir = self.logfile_dir
			if not self.__if_file_exists(logfile_dir):
				return {}

			description = kwargs.get('description', 'Without description.') 
			log_level = kwargs.get('log_level', 5)
			current_time = self.__current_time()
			record_title = self.__record_title(log_level)

			record = f'{record_title}: {description} ({current_time})\n'

			with open(logfile_dir, 'a') as logfile:
				logfile.write(record)

		except Exception as e:
			logger.error(str(e))

		return {}

