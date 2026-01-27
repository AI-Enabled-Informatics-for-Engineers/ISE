import os, requests

CANVAS_BASE_URL='https://rutgers.instructure.com'
COURSE_ID=os.environ.get('CANVAS_COURSE_ID','385339')
TOKEN=os.environ['CANVAS_TOKEN']
headers={'Authorization': f'Bearer {TOKEN}'}

def post(path,payload):
    r=requests.post(f"{CANVAS_BASE_URL}/api/v1{path}",headers=headers,data=payload)
    r.raise_for_status(); return r.json()

if __name__=='__main__':
    m=post(f"/courses/{COURSE_ID}/modules",{'module[name]':'Week 1 — Informatics Foundations & Industry 5.0 (Jan 20–26)'})
    print('Created module',m.get('id'))
