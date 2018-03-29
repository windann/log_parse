import re
log = 'https://www.sys.mail.ru/calendar/config/254/40255/'
pattern = r':\/\/www\.'

match = re.search(pattern, log)
#print(log if match else 'Not found')
r = ''

#print(re.findall(pattern, log))
#log.replace('://www.','://')
#new_log =
#print(new_log)
