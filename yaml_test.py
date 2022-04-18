import yaml

with open('/home/pi/webapp/data.yaml') as fr : 
    data = yaml.load(fr, Loader=yaml.FullLoader)
print(data)
line = data['line']
print(line)    
print(type(line))  

data['location'] = 0

print(data)
with open('/home/pi/webapp/data.yaml', 'w') as fw:
    yaml.dump(data, fw)