from rest_framework.renderers import JSONRenderer




def get_msg(code):
    msgMap = {
        "200":u"请求成功",
        "403":u"认证失败",

    }

    if str(code) in msgMap.keys():
        return msgMap[str(code)]
    else:
        return "未知错误"

class CustomJsonRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        结构
        {
            'code':xxx,
            'msg':请求成功,
            'data':{返回数据}
        }
        """
        print()
        if renderer_context:
            if isinstance(data, dict):
                # 如果没有就创建一个
                # msg = data.pop('msg', '请求成功')
                code = data.pop('code', renderer_context['response'].status_code)
            else:
                # msg = '请求成功'
                code = renderer_context['response'].status_code
            # response = renderer_context['response']

            # response.status_code = 200
            res = {
                'code': code,
                'msg': get_msg(code),
                'data': data
            }
            return super().render(res, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)
