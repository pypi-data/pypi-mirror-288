import base64, json
import config
from ntpath import join
# from .config import Config
from robot.libraries.BuiltIn import BuiltIn
from bs4 import BeautifulSoup
from dateutil import parser

class Report:
    def cucumber(report_json):        
        cucumber = []

        for suite_index, suite in enumerate(report_json):
            cucumber.append({
                "keyword": "Feature",
                "name": suite.get('longname'),
                "line": 1,
                "description": suite.get('doc'),
                "tags": [],
                "id": suite.get('id'),
                "uri": suite.get('source'),
                "elements": [],
            })

            for test_index, test in enumerate(suite.get('tests')):
                if test.get('template') != "":
                    cucumber[suite_index]['elements'].append({
                        "keyword": "Scenario Outline",
                        "name": test.get('originalname'),
                        "line": test.get('lineno'),
                        "description": test.get('doc'),
                        "tags": [],
                        "id": test.get('id'),
                        "type": "scenario",
                        "steps": [],
                    })
                else:
                    cucumber[suite_index]['elements'].append({
                        "keyword": "Scenario",
                        "name": test.get('originalname'),
                        "line": test.get('lineno'),
                        "description": test.get('doc'),
                        "tags": [],
                        "id": test.get('id'),
                        "type": "scenario",
                        "steps": [],
                    })

                for tag_index, tag in enumerate(test.get('tags')):
                    cucumber[suite_index]['elements'][test_index]['tags'].append({
                        "name": "@{}".format(tag),
                        "line": test.get('lineno'),
                    })
               
                screenshots = []

                for step_index, step in enumerate(test.get('keywords')):
                    for message_index, message in enumerate(step.get('messages')):
                        if message.get('message').__contains__('data:image/png;base64,'):
                            soup = BeautifulSoup(message.get('message'), 'html.parser')
                            imageBase64 = soup.img.get('src').replace('data:image/png;base64,', '')
                            screenshots.append({ "mime_type": "image/png", "data": "{}".format(imageBase64) })

                        # if message.get('message').__contains__('<a href=') and not message.get('message').__contains__('log_message'):
                        #     soup = BeautifulSoup(message.get('message'), 'html.parser')
                        #     image_src = soup.a.get_text()

                        #     if image_src.__contains__('.jpg'):
                        #         if config.Config.debug():
                        #             print(BuiltIn().get_variable_value('${OUTPUT_DIR}'))
                        #             print(image_src)
                                
                        #         with open(image_src, 'rb') as img_file:
                        #             b64_string = base64.b64encode(img_file.read())
                        #             screenshots.append({ "mime_type": "image/jpeg", "data": "{}".format(b64_string.decode('utf-8')) })
                        
                        # if message.get('message').__contains__('<img') and not message.get('message').__contains__('log_message'):
                        #     soup = BeautifulSoup(message.get('message'), 'html.parser')
                        #     image_src = soup.img.get('src')

                        #     if not image_src.__contains__('data:image/png;base64,'):
                        #         if config.Config.debug():
                        #             print(BuiltIn().get_variable_value('${OUTPUT_DIR}'))
                        #             print(image_src)
                                
                        #         with open(join(BuiltIn().get_variable_value('${OUTPUT_DIR}'), image_src), 'rb') as img_file:
                        #             b64_string = base64.b64encode(img_file.read())
                        #             screenshots.append({ "mime_type": "image/png", "data": "{}".format(b64_string.decode('utf-8')) })
                        #     else:
                        #         screenshots.append({ "mime_type": "image/png", "data": "{}".format(image_src.replace('data:image/png;base64,', '')) })
                    
                    if step.get('kwname').split()[0].lower() in ['given', 'when', 'then', 'and', 'but', '*']:
                        date1 = parser.parse(step.get('starttime'))
                        date2 = parser.parse(step.get('endtime'))
                        diff = date2 - date1

                        cucumber[suite_index]['elements'][test_index]['steps'].append({
                            "embeddings": screenshots,
                            "keyword": step.get('kwname').split()[0].capitalize(),
                            "name": step.get('kwname').replace(step.get('kwname').split()[0], '').strip(),
                            "line": step.get('lineno'),
                            "match": {
                                "arguments": [],
                                "location": "{}:{}".format(step.get('source'), step.get('lineno'))
                            },
                            "result": {
                                "status": ("passed" if step.get('status').lower() == "pass" else ("failed" if step.get('status').lower() == "fail" else "skipped")),
                                "duration": diff.microseconds*1000,
                            }
                        })
                        
                        screenshots = []
                        
        with open(config.Config.cucumber_path() + '/report.json', 'w') as report_file:
            json.dump(report_json, report_file, indent=4)

        with open(config.Config.cucumber_path() + '/cucumber.json', 'w') as report_file:
            json.dump(cucumber, report_file, indent=4)