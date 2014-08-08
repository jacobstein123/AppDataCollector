import time
import clicker
from getGooglePlayData import execute_command, execute_query

db = {'host'  : 'localhost',
      'user'  : 'root',
      'passwd': '',
      'db'    : 'mysql'}

apps_to_download = execute_query(db,'select * from apps where apk_file is NULL;')
for app in apps_to_download:
    clicker.download_app(app['package_name'])
    execute_command(db,'update apps set apk_file = "googleplay/{0}.apk" where package_name="{0}";'.format(app['package_name']))
    time.sleep(3)


