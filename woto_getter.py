# @Author: JupiterZ

from urllib import request
import PyPDF2
# import base64
# from IPython import embed
import os


from datetime import datetime, timedelta

switcher = {
        1: "january",
        2: "february",
        3: "march",
        4: "april",
        5: "may",
        6: "june",
        7: "july",
        8: "august",
        9: "september",
        10: "october",
        11: "november",
        12: "december"
}


def char_count(string, char):
    cnt = 0
    for ch in string:
        if ch == char:
            cnt += 1
    return cnt


def pdf_text_analysis(text):

    urls = list()

    texts = text.split("\n")
    # print(texts)
    for i in range(len(texts) - 1):
        if texts[i].__contains__("http://bit.ly/") and texts[i - 1][-4:] == "WOTO":
            tmp_ls = []

            base = texts[i]
            for j in range(1, 4):
                base += texts[i + j]

                if not base.__contains__("201fall18-"):
                    continue

                if base[10:].__contains__("http"):
                    urls.append("http://" + base[7:].split("http")[0])
                    break

                if char_count(base[16:], "/") == 2 and char_count(base[16:], "-") == 2:
                    splitted = base.split("-")[-1]
                    front = ''.join(base.split("-")[:-1])
                    try:
                        if int(splitted.split("/")[0]) > 12 and int(splitted.split("/")[0][0]) <= 3:
                            urls.append("{}-{}".format(front, splitted[0]))
                            break
                    except:
                        break
                if char_count(base[16:], "/") == 2 and char_count(base[16:], "-") == 1:
                    urls.append(tmp_ls[-1])
                    break

                tmp_ls.append(base)
    return urls


def get_pdf(url):

    a = request.Request(url)
    pdf_downloaded = request.urlopen(a).read()
    name = "." + url.split("/")[-1]

    fl_new = open(name, "wb")
    fl_new.write(pdf_downloaded)
    fl_new.close()

    fl_base = open(name, "rb")
    pdf_opened = PyPDF2.PdfFileReader(fl_base)
    # print(pdf_opened.numPages)

    os.system("rm {}".format(name))

    text = str()

    for i in range(pdf_opened.numPages):
        page_opened = pdf_opened.getPage(i)
        text += page_opened.extractText()

    result = pdf_text_analysis(text)

    return result


def get_html(url):

    b = request.Request(url)
    c = request.urlopen(b)
    d = html_parser(str(c.read()))

    return d


def html_parser(string):

    l = []
    write = 1
    for x in string:
        if x == "<":
            write = 0
        if x == ">":
            x = '\t'
            write = 1
        if write:
            l.append(x)

    l = ("".join(l)).split("\t")

    return l


def woto_file_getter(time):

    base_dir = "https://www2.cs.duke.edu/courses/fall18/compsci201/notes/"
    base_result = get_html(base_dir)

    date_partial = switcher[time[0]][:3] + str(time[1]) + "/"

    if date_partial not in base_result:
        return None

    pendings = []

    date_dir = base_dir + date_partial
    date_result = get_html(date_dir)
    for fl in date_result:
        if fl.__contains__("4up.pdf"):
            pendings.append(date_dir + fl)

    if len(pendings) == 0:
        return None

    return pendings


def woto_getter(day_range):

    times = [[int(j) for j in str(datetime.date(datetime.now() + timedelta(i))).split("-")[1:]] for i in range(-int(day_range / 2), int(day_range / 2))]
    urls = []

    # embed()

    for time in times:
        pending = woto_file_getter(time)
        # print(time)
        if pending is None:
            continue

        for link in pending:
            # print(link)
            result = get_pdf(link)
            if result is not None:
                for url in result:
                    urls.append(url)

    return list(set(urls))


# print(woto_getter(20))
