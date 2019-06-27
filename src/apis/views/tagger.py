from flask import render_template, request, Markup
from urllib import parse
from scalpl import Cut
import re, math

from common.conf import config

from services import JobDescriptionService, SentenceTaggedService
from forms.tag_form import TagEntryForm, SentenceTag
from errors import ServiceException


srv = JobDescriptionService()
tag_srv = SentenceTaggedService()
RESULTS_PER_PAGE = config.get('RESULTS_PER_PAGE')


def jd():
    page = int(request.args.get('page', 1))
    tagged = bool(int(request.args.get('st', 0)))

    query = request.args.get('query')

    if not query:
        paginated_jds, jd_len = srv.get_job_descriptions_for_page(page, tagged)
    else:
        paginated_jds, jd_len = srv.get_job_descriptions_for_search(query, page, tagged)

    def edit_query_params(url,new_params,b):
        parts = list(parse.urlsplit(url))
        query_param = dict(parse.parse_qsl(parts[3]))
        query_param['page'] = new_params
        if('st' in query_param.keys() and b==1): 
            del query_param['st'] 
        parts[3] = parse.urlencode(query_param)
        f_url = parse.urlunsplit(parts)
        
        return f_url 

    base_url = request.url
    if '?' not in base_url:
            base_url += '?'
    next_url = edit_query_params(base_url, page + 1, b = 0)
    previous_url = edit_query_params(base_url, page - 1, b = 0)
    page_num = math.ceil(jd_len/RESULTS_PER_PAGE)
    numbers = [f'{edit_query_params(base_url, i, b = 0)}' for i in range(page,page+10) if page<=page_num-9]
    url_for_tagged_untagged = edit_query_params(base_url, page, b = 1)

    return render_template('jd.html', l=len(paginated_jds),
        com=paginated_jds, page_num=page_num, previous_url=previous_url,
        next_url=next_url, numbers=numbers,
        base_url=url_for_tagged_untagged, page = page
    )


def sent(jd_id):
    details = srv.get_jd_details(jd_id)
    html = details.get('jd_html')

    if request.method == 'GET':
        form = TagEntryForm()
        present_tags = tag_srv.get_tagged_sentences_for_jd(jd_id).get('taggings')

        if not present_tags:
            present_tags = [
                {'sentence': sent, 'tag': 'Tags'} for sent in details.get('jd_sentences')
            ]

        for ptag in present_tags:
            st = SentenceTag()
            st.sentence = ptag.get('sentence')
            st.tag = ptag.get('tag')

            form.tag_list.append_entry(st)

        return render_template(
            'sent.html', form=form, jd_html=Markup(html))
    else:
        out = Cut({}, sep='-')

        for key, value in request.form.to_dict().items():
            out.setdefault(key, value)

        out = dict(out)
        tags = list(out['tag_list'].values())

        tag_srv.perform_sentence_tagging(jd_id, tags)

        return render_template('sent.html', tagged=True, jd_html=Markup(html))