import requests
import json
import base64
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--server", help="Dependency Track server URL")
parser.add_argument("--project", help="Dependency Track project")
parser.add_argument("--api_key", help="Dependency Track API key")
parser.add_argument("--path", help="PATH file to upload")
args = parser.parse_args()

file = open(args.path).read()

def main():
    data = {'bom':base64.b64encode(file) , "project":args.project}
    headers = {'Content-Type': 'application/json', 'X-API-Key': args.api_key}
    r = requests.put("http://"+args.server+"/api/v1/bom", data=json.dumps(data), headers=headers)
    print(r)

if __name__ == '__main__':
    main()
