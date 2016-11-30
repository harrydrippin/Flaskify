# -*- coding: utf-8 -*-
# Flaskify.py
# @author harrydrippin (Seunghwan Hong)

import argparse, json, datetime, os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def flaskify(api_doc, apifile, comment):
    ret = []
    apifile = json.loads(apifile)

    print("[+] " + bcolors.BOLD + "File Name : " + bcolors.ENDC + api_doc)
    print("[+] " + bcolors.BOLD + "Name      : " + bcolors.ENDC + apifile['name'])
    print("[+] " + bcolors.BOLD + "Author    : " + bcolors.ENDC + apifile['author'])
    print("[+] " + bcolors.BOLD + "Comment   : " + bcolors.ENDC + apifile['doc_comment'] + "\n")
    if comment == True:
        print("[+] Compiling with " + bcolors.HEADER + "TODO " + bcolors.ENDC + "comment...")
    else:
        print("[+] Compiling...")

    # Add name, author, doc_comment
    ret.append("# -*- coding: utf-8 -*-")
    ret.append("# app.py")
    ret.append("# Name    : " + apifile['name'])
    ret.append("# Author  : " + apifile['author'])
    ret.append("# Comment : " + apifile['doc_comment'])
    ret.append("\nfrom flask import Flask, request, jsonify")
    ret.append("app = Flask(__name__)")

    ret.append('''
# Exception Region Start

@app.errorhandler(404)
def error_not_found(error):
    return "404"

@app.errorhandler(403)
def error_access_denied(error):
    return "403"

@app.errorhandler(405)
def error_bad_request(error):
    return "405"

@app.errorhandler(500)
def error_internal_error(error):
    return "500"

# Exception Region End
    ''')

    ret.append("# Front API Region Start\n")

    routes = apifile['routes']

    backend_defs = [];
    backend_defs_args = [];
    backend_defs_return = [];

    for route in routes.keys():
        method_save = ""
        if routes[route]['methods'] == None:
            ret.append("@app.route('" + route + "')")
        elif len(routes[route]['methods'].split(",")) >= 1:
            method_temp = "["
            for method in routes[route]['methods'].split(","):
                method_temp += "'" + method + "', "
                method_save += method
            method_temp = method_temp[0:len(method_temp) - 2] + "]"
            ret.append("@app.route('" + route + "', methods=" + method_temp + ")")
        route_code = route.split("/")
        def_name = ""
        for item in route_code:
            def_name += item + "_"
        def_name = def_name[1:len(def_name) - 1]
        backend_defs.append(def_name + "_backend")
        ret.append("def " + def_name + "():")
        if comment == True:
            ret.append("\t# TODO : " + routes[route]['comment'])

        input_dic = routes[route]['input']
        output_dic = routes[route]['output']
        backend_var = ""
        normal_var = ""
        for cursor in input_dic.keys():
            cursor_temp = ""
            normal_var += cursor + ", "
            if method_save.find("POST") != -1:
                cursor_temp = "\t" + cursor + " = request.form['" + cursor + "']"
            elif method_save.find("GET") != -1:
                cursor_temp = "\t" + cursor + " = request.args.get('" + cursor + "', '')"

            if comment == True:
                cursor_temp += " # " + input_dic[cursor]
            ret.append(cursor_temp)

        ret.append("")

        output_var = ""
        output_list = []
        for output in output_dic.keys():
            output_var += output + ", "
            output_list.append(output)

        ret.append("\t" + output_var[0:len(output_var) - 2] + " = " + def_name + "_backend(" + normal_var[0:len(normal_var) - 2] + ")")
        backend_defs_args.append(normal_var[0:len(normal_var) - 2])

        return_text = "\treturn jsonify("

        for txt in output_list:
            return_text += txt + "=" + txt + ", "
        ret.append(return_text[0:len(return_text) - 2] + ")")

        backend_defs_return.append(output_var[0:len(output_var) - 2])

        ret.append("")

    ret.append("# Front API Region End\n\n# Back API Region Start\n")

    for i in range(0, len(backend_defs)):
        ret.append("def " + backend_defs[i] + "(" + backend_defs_args[i] + "):\n\t# TODO : make " + backend_defs[i] + " function\n\treturn " + backend_defs_return[i] + "\n")

    ret.append("# Back API Region End")
    ret.append("\nif __name__ == '__main__':\n\tapp.run(debug=True)")
    return ret

def markdownify(apifile):
    ret = []
    apifile = json.loads(apifile)

    ret.append("# " + apifile['name'])
    ret.append("> 이 파일은 Flaskify에 의하여 자동 생성된 API 문서입니다.")
    ret.append(apifile['doc_comment'])
    ret.append("*****")

    for route in apifile['routes'].keys():
        ret.append("### `" + route + "`")
        ret.append(str(apifile['routes'][route]['comment']))

        input_dic = apifile['routes'][route]['input']
        output_dic = apifile['routes'][route]['output']
        if len(input_dic.keys()) != 0:
            ret.append("#### 입력")
        for inp in input_dic.keys():
            ret.append("* `" + inp + "` — " + input_dic[inp])
        if len(output_dic.keys()) != 0:
            ret.append("#### 출력")
        for outp in output_dic.keys():
            ret.append("* `" + outp + "` — " + output_dic[outp])
        ret.append("*****")

    return ret[0:len(ret) - 1]

def main():
    p = argparse.ArgumentParser(description="ex) flaskify api.txt, flaskify api.txt --comment")
    p.add_argument("apidoc", help="API 문서로의 경로", metavar="[API Document]")
    p.add_argument("-c", "--comment", help="결과에 TODO 주석을 포함합니다.", action="store_true")
    p.add_argument("-m", "--markdown", help="마크다운 문법의 상세 설명 파일을 출력합니다.", action="store_true")

    args = p.parse_args()
    api_doc = args.apidoc
    comment = args.comment
    markdown = args.markdown

    try:
        f = open(api_doc, "rU", encoding="euc-kr")
        apifile = f.readlines()
    except UnicodeDecodeError as e:
        f.close()
        f = open(api_doc, "rU", encoding="utf-8")
        apifile = f.readlines()

    json_string = ""
    for i in apifile:
        json_string += i
    print("[+] " + bcolors.BOLD + "Flaskify 1.0.0" + bcolors.ENDC)
    print("[*] " + bcolors.BOLD + "Made by Seunghwan Hong(@harrydrippin on Github)" + bcolors.ENDC + "\n")
    flaskCode = flaskify(api_doc, json_string, comment)

    try:
        f = open("app.py", "w")
        for i in range(0, len(flaskCode)):
            f.write(flaskCode[i] + "\n")
        f.close()
    except Exception as e:
        print("[-] 예기치 못한 오류가 발생했습니다. 다시 시도하시거나, 에러 내용을 문의해주세요.")
        print("[-] 에러 명세 : " + str(e))
        sys.exit(5)

    print("[+] Your " + bcolors.BOLD + "app.py" + bcolors.ENDC + " was saved on " + bcolors.UNDERLINE + os.getcwd() + bcolors.ENDC + ".")

    if markdown == True:
        markdown_code = markdownify(json_string)
        try:
            f = open("API_DOC.md", "w")
            for i in range(0, len(markdown_code)):
                f.write(markdown_code[i] + "\n")
            f.close()
        except Exception as e:
            print("[-] 예기치 못한 오류가 발생했습니다. 다시 시도하시거나, 에러 내용을 문의해주세요.")
            print("[-] 에러 명세 : " + str(e))
            sys.exit(5)
        print("[+] Markdown API document(" + bcolors.BOLD + "API_DOC.md" + bcolors.ENDC + ") was saved. You can also find this on directory above.")

main()
