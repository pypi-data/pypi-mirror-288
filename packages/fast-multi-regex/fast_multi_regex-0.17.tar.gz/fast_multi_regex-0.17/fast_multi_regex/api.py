import logging
from fastapi import FastAPI, HTTPException, Depends
from typing import Literal, Optional
import pickle
import os
import time
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .matcher import (
    MultiRegexMatcher,
)
from .utils import (
    load_matchers_and_metadata,
    DelayedFilesHandler,
    model_to_dict,
)
from .api_types import (
    BodyMatch,
    RespMatch,
    RespInfo,
    BodyTargets,
    RespTargets,
    BodyFindExpression,
    RespFindExpression,
)
matcher_logger = logging.getLogger('matcher')


def pkl_file_processor(
    path: str, 
    opt: Literal['modified', 'created', 'deleted'],
    context: dict,
    *args,
    **kwargs,
):
    if not path or os.path.basename(path)[0] == '.':
        return
    file_extension = os.path.splitext(path)[1]
    if file_extension == '.pkl':
        name_info: dict[str, MultiRegexMatcher] = context['matchers']
        name_type = 'matcher'
    elif file_extension == '.meta_pkl':
        name_info: dict[str, dict[str, Optional[dict]]] = context['metadata']
        name_type = 'metadata'
    else:
        return
    
    matchers_folder: str = context['matchers_folder']
    name = os.path.splitext(os.path.relpath(path, matchers_folder))[0]
    if opt == 'modified' or opt == 'created':
        with open(path, 'rb') as f:
            name_info[name] = pickle.load(f)
    elif opt == 'deleted':
        name_info.pop(name, None)
        
    matcher_logger.info(f'update {name_type} "{name}" {opt}')


matchers_folder = os.getenv('FAST_MULTI_REGEX_MATCHERS_FOLDER', 'data/matchers')
api_tokens = set(os.getenv('FAST_MULTI_REGEX_API_TOKENS', 'test').split(','))
matchers_api_update_delay = int(os.getenv('FAST_MULTI_REGEX_MATCHERS_API_UPDATE_DELAY', 3))
global_matchers: dict[str, MultiRegexMatcher] = {}
global_metadata: dict[str, dict[str, Optional[dict]]] = {}


async def startup():
    global global_matchers, global_metadata
    global_matchers, global_metadata = load_matchers_and_metadata(matchers_folder)
    matcher_logger.info(f"init global_matchers: {list(global_matchers)}")
    DelayedFilesHandler(
        matchers_folder,
        file_handler=pkl_file_processor,
        delay=matchers_api_update_delay,
        context={
            'matchers_folder': matchers_folder,
            'matchers': global_matchers,
            'metadata': global_metadata,
        },
    )


app = FastAPI(
    title='fast-multi-regex',
    summary='A fast multi regex matcher',
    description='快速多正则和布尔表达式匹配，支持热更新正则库',
)
app.add_event_handler("startup", startup)
security = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token not in api_tokens:
        raise HTTPException(status_code=403, detail="Invalid or expired token")


@app.post(
    "/match",
    response_model=RespMatch,
    dependencies=[Depends(verify_token)],
    summary="使用 query 去快速匹配相应的正则库",
    description="使用 query 去快速匹配相应的正则库",
)
async def post_match(body: BodyMatch):
    start = time.time()
    result = []
    qs = body.qs if isinstance(body.qs, list) else [body.qs]
    
    for i, q in enumerate(qs):
        if q.db not in global_matchers:
            return RespMatch(message=f"qs{i}: db '{q.db}' not found", status=1)
        one_result: list[dict] = []  # list[OneMatchMark]
                        
        if q.method == 'first':
            try:
                match = global_matchers[q.db].match_first(q.query)
            except BaseException as e:
                return RespMatch(message=f"qs{i}.first: {e}", status=2)
            if match:
                one_result.append({'mark': match[0], 'matches': [match[1]], 'match_count': 1})
        
        elif q.method == 'all':
            try:
                matches = global_matchers[q.db].match_all(q.query, q.is_sort, q.detailed_level, q.match_top_n)
            except BaseException as e:
                return RespMatch(message=f"qs{i}.all: {e}", status=3)
            if isinstance(matches, list):
                one_result += [{'mark': m} for m in matches]
            else:
                for mark, v in matches.items():
                    if isinstance(v, int):
                        one_result.append({'mark': mark, 'match_count': v})
                    else:
                        one_result.append({'mark': mark, 'matches': v, 'match_count': len(v)})
                
        elif q.method == 'strict':
            try:
                matches = global_matchers[q.db].match_strict(q.query, q.is_sort)
            except BaseException as e:
                return RespMatch(message=f"qs{i}.strict: {e}", status=4)
            for mark, v in matches.items():
                one_result.append({'mark': mark, 'matches': v, 'match_count': len(v)})
                
        else:
            return RespMatch(message=f"qs{i}: method '{q.method}' not found", status=5)
        
        db_metadata = global_metadata.get(q.db) or {}
        for om in one_result:
            om['meta'] = db_metadata.get(om['mark'])
            if om['meta'] and q.allowed_return_meta_keys:
                om['meta'] = {k: om['meta'][k] for k in q.allowed_return_meta_keys if k in om['meta']}
            if q.detailed_level == 1:
                om['matches'] = None
                om['match_count'] = None
            elif q.detailed_level == 2:
                om['matches'] = None
        result.append(one_result)
    return RespMatch(result=result, milliseconds=(time.time() - start) * 1000)


@app.get(
    "/info",
    response_model=RespInfo,
    dependencies=[Depends(verify_token)],
    summary="获取正则库信息",
    description="用于分析正则库是否正常，包括最近什么时候编译更新过",
)
async def get_info(db: str = 'default'):
    if db in global_matchers:
        info = global_matchers[db].info
        return RespInfo(result=info)
    else:
        return RespInfo(message=f"db '{db}' not found", status=1)


@app.post(
    "/get_targets",
    response_model=RespTargets,
    dependencies=[Depends(verify_token)],
    summary="获取正则组信息",
    description="可用于查询 match 返回的 mark 对应的具体正则组信息",
)
async def post_targets(body: BodyTargets):
    if body.db in global_matchers:
        matcher = global_matchers[body.db]
        db_metadata = global_metadata.get(body.db) or {}
        ext_targets = []
        for mark in body.marks:
            target = matcher.get_target(mark)
            if target is None:
                ext_targets.append(None)
            else:
                ext_targets.append({
                    **model_to_dict(target),
                    'meta': db_metadata.get(mark),
                })
        return RespTargets(result=ext_targets)
    else:
        return RespTargets(message=f"db '{body.db}' not found", status=1)


@app.post(
    "/find_expression",
    response_model=RespFindExpression,
    dependencies=[Depends(verify_token)],
    summary="从正则库中查找正则表达式",
    description="可用于查找一些正则是否存在，帮助增删改相关正则",
)
async def post_find_expression(body: BodyFindExpression):
    if body.db in global_matchers:
        result = global_matchers[body.db].find_expression(
            s=body.s, 
            exact_match=body.exact_match, 
            top_n=body.top_n,
            allow_flag=body.allow_flag,
            prohibited_flag=body.prohibited_flag,
        )
        return RespFindExpression(result=result)
    else:
        return RespFindExpression(message=f"db '{body.db}' not found", status=1)
