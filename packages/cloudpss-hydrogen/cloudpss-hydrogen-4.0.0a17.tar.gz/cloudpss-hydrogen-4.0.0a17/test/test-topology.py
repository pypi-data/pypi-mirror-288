import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..\\'))
import cloudpss
import time
import numpy as np
import pandas as pd
import json

if __name__ == '__main__':
    os.environ['CLOUDPSS_API_URL'] = 'http://10.101.10.34/'
    print('CLOUDPSS connected')
    cloudpss.setToken(
        'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTEsInVzZXJuYW1lIjoiemhvdXFpYW5nIiwic2NvcGVzIjpbImJyb3dzZXIiXSwicm9sZXMiOlsiKiJdLCJ0eXBlIjoiYnJvd3NlciIsImV4cCI6MTcyNTUyNjkxNywiaWF0IjoxNzIyODQ4NTE3fQ.WjTa_hQg6nhtXjpNY7pcgGHgjv9NE1YDDPepL5Xjg_Xms-HT9LUw5MBngBLvlXQtajnwAOkNVnVv49hxHcOzRQ')
    print('Token done')
    project = cloudpss.Model.fetch('model/zhouqiang/7380b767-e594-5397-970c-959ab2c8e134')
    print(project.revision.hash)
    t = time.time()
    # topology = cloudpss.ModelTopology.fetch("hlbBPYIyQHWzgPxdjp9lV9a92twyxA2zETzrqz4Q0fou7mfOemX-pr9OfO9eUfq4","emtp",{'args':{}})
    # topology = cloudpss.ModelTopology.fetch("JwHbZdjco9eC0nZw3fY7Iz9rqsQ4HFGJObiBW3bFuYLPCd0Vqb2vb8zNY28D1AXV","emtp",{'args':{}})
    # print(time.time()-t)
    
    # runner = project.run()
    # while not runner.status():
    #     logs = runner.result.getLogs()
    #     for log in logs:
    #         print(log)
    # logs = runner.result.getLogs()
    # for log in logs:
    #     print(log)     

    topology= project.fetchTopology(config={'args':{}},maximumDepth=10,xToken="eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6OSwidXNlcm5hbWUiOiJJRVNMYWJPcHQiLCJzY29wZXMiOlsibW9kZWw6OTgzNjciLCJmdW5jdGlvbjo5ODM2NyIsImFwcGxpY2F0aW9uOjMyODMxIl0sInJvbGVzIjpbIklFU0xhYk9wdCJdLCJ0eXBlIjoiYXBwbHkiLCJleHAiOjE3NTI5MDcxMzMsIm5vdGUiOiLlhYPku7YiLCJpYXQiOjE3MjE4MDMxMzN9.gShFsJH8R4N8sWY1k3VwJ6skxo3lIP0lxXJXogZcbbP-4pa8lIdi-q1PVtywiPFlYexcvBbVeuTo5UymfmQecg")

    topology.dump(topology,'test.json')
    
    
    