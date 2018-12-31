# encoding: utf-8
import os
import requests



new_header = 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0'

class MG_handler(object):

    def __init__(self):
        self.enabled = True
        self.name = 'Megalodon.jp'
        self.api_required = False

    def push(self, uri_org, p_args=[]):


        pre_defined_errors = [     
            {
                "We could not acquire this web page because it exceeded the maximum available size ( 30 MB ).":
                [u"こちらのウェブページはご利用できる最大サイズ", u"を超えたため取得出来ませんでした"]
            },
            {
                "Acquisition under Cookie invalid state is prohibited.":
                [u"Cookieが無効な状態」での取得は禁止されています。取得確認ページを再読み込み(更新)すると取得できる場"]
            },
            {   
                "Acquisition error occurred.":
                [u"申し訳ございません、取得エラーが発生しました"]
            },
            {
                "The same URL is acquired within 10 minutes. Please wait at least 10 minutes.":
                [u"同一のURLが10分以内に取得されています"]
            },
            {
                "We could not acquire it because of unknown error: 503":
                [u"のため取得出来ませんでした",u"max file size over.",u"申し訳ございません"]
            }
        ]

        if not uri_org.startswith('http'):
            uri_org = 'http://' + uri_org

        msg = ''

        try:

            headers = {
                'User-Agent': new_header,
            }

            try:

                r = requests.get('http://megalodon.jp/?url=' + uri_org,
                                 headers=headers)
                token = r.text.split('"token" value="',
                                             1)[1].split('"',1)[0]

                phpsessid = r.headers['Set-Cookie'].split('PHPSESSID=', 1)[1]
                cookies = dict(PHPSESSID=phpsessid)

            except Exception as e:
                msg = "Error ({0}): {1}".format(self.name, str(e))
                pass;

            if msg == '':
                try:
                    r2 = requests.post('https://megalodon.jp/pc/get_simple/decide',
                                    data={"url":uri_org, "token":token},
                                    cookies=cookies, headers=headers,
                                    )
                except Exception as e:
                    msg = "Error ({0}): {1}".format(self.name, str(e))
                    pass;

                cont = r2.text

                if msg == '':
                    try:
                        msg = cont.split('location.href = "',
                                                    1)[1].split('"', 1)[0]
                    except Exception as e:
                        # try to identify the error from the returned content
                        err_found = False
                        for err in pre_defined_errors:
                            error_key = list(err)[0]
                            error_descs = err[error_key]
                            matched = 0
                            for e_d in error_descs:
                                if e_d in cont:
                                    matched = matched + 1
                                else:
                                    break;
                            if matched == len(error_descs):
                                err_found = True
                                msg = "Error (" + self.name+ "): "+error_key
                                break;
                        if not err_found:
                            msg = "Error (" + self.name+ "): " + str(e)

        except Exception as e:
            if not msg:
                msg = "Error (" + self.name+ "): " + str(e)
            pass;
        if ('list index out of range' in msg) or ('referenced before assignment' in msg):
            msg = "Error (" + self.name+ "): " + "We can not obtain this page because the time limit has been reached or for technical ... "
        return msg
