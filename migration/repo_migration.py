# -*- coding: utf-8 -*-
# !env python
import json
import logging
import os
import threading
import time
from multiprocessing.pool import ThreadPool
from urllib.parse import urlparse

import click
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from tqdm import tqdm

from .github_auth import BASIC_TOKEN_FILE_NAME
from .helper import making_soup, get_version
from config import PROCESS, WAIT_TIME

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Make thread pool
pool = ThreadPool(processes=PROCESS)


class RepoMigrationError(Exception):
    def __init__(self, json_text):
        os.remove(BASIC_TOKEN_FILE_NAME)
        self.json = json_text

    def __str__(self):
        return repr(self.json)


def get_downloads(**kwargs):
    project = kwargs.get('project')
    # 기본 상수 값 정의
    board_type = 'download'
    tag_name = 'release_id'

    # URL 및 project_name 불러오기
    url = project.urls[board_type]
    project_name = str(project)
    project_url = project.project_url

    thread_msg = '{0}가 {1}의 다운로드 파싱 시작'.format(threading.current_thread().name, project_name)
    logging.debug(thread_msg)
    print(thread_msg)

    # 다운로드 게시판 XML 요청
    board_xml = requests.request("GET", url)
    soup = making_soup(board_xml.content, 'xml')
    release_id_list = soup.findAll(tag_name)

    downloads = list()
    files = list()

    for tag in tqdm(release_id_list):
        release_id = tag.get_text()
        request_url = '{0}/{1}/{2}.xml'.format(project_url, board_type, release_id)

        each_xml = requests.request("GET", request_url).content

        if not each_xml:
            log_msg = 'BLANK_XML_BUG NAME: {0}, ID: {1}, TYPE: {2}'.format(project_name,
                                                                           release_id,
                                                                           board_type)
            logging.debug(log_msg)
            continue

        dl_soup = making_soup(each_xml, 'xml')
        name = dl_soup.find('name').get_text()
        description = dl_soup.find('description').get_text()
        version = str(get_version(project_name, name))

        for file in dl_soup.files.findAll('file'):
            file_id = file.find('id').get_text()
            file_name = file.find('name').get_text()
            file_ext = file_name.split('.')[-1]
            file_down_url = '{0}/frs/download.php/{1}/{2}'.format(project.api_url,
                                                                  file_id, file_name)

            file_raw = requests.request('GET', file_down_url, stream=True).content
            files.append(dict(
                id_=file_id,
                name=file_name,
                ext=file_ext,
                raw=file_raw
            ))

            downloads.append(dict(
                tag_name=version,
                target_commitish='master',
                name=name,
                body=description,
                prerelease=False,
                draft=False
            ))

    return downloads, files


def repo_migration(**kwargs):
    project = kwargs.get('project')

    get_download_result = pool.apply_async(get_downloads, kwds=dict(project=project))

    downloads, files = get_download_result.get()

    thread_msg = '{0}가 {1}의 소스 코드 마이그레이션 시작'.format(threading.current_thread().name, project.project_name)
    logging.debug(thread_msg)

    gh = kwargs.get('github_session')
    repo = kwargs.get('github_repository')

    base_url = '{0}/repos/{1}/{2}/'.format(gh._github_url, gh.user().login, repo.name)

    with open(BASIC_TOKEN_FILE_NAME) as f:
        token = f.read()

    netloc = urlparse(project.api_url)[1]

    # staging. 으로 시작하면 migration 이 되지 않음..
    if project.vcs is 'git':
        username = click.prompt('NAVER 아이디를 입력하세요')
        password = click.prompt('NAVER 비밀번호를 입력하세요', hide_input=True, confirmation_prompt=True)
        vcs = 'git'
        # git 은 반드시 https 프로토콜로 넘기기!!
        url = 'https://{0}@{3}/{1}/{2}.{1}'.format(username, project.vcs, project.project_name,
                                                  netloc.replace('staging.', ''))

        print(url)
    else:
        username = 'anonsvn'
        password = 'anonsvn'
        vcs = 'subversion'
        url = 'https://{2}/{0}/{1}'.format(project.vcs, project.project_name,
                                           netloc.replace('staging.', ''))

    migration_request_url = base_url + 'import'

    import_headers = {
            'Accept': "application/vnd.github.barred-rock-preview",
            'authorization': "token " + token,
            'content-type': "application/json",
        }

    request_data = json.dumps(
        dict(
            vcs=vcs,
            vcs_url=url,
            vcs_username=username,
            vcs_password=password
        )
    )

    r = requests.request("PUT", migration_request_url, data=request_data, headers=import_headers)

    if r.status_code is 201:
        repo_migration_status = True if r.json()['status'] is 'complete' else False
    else:
        raise RepoMigrationError(r.json())

    while not repo_migration_status:
        import_confirm = requests.request('GET', migration_request_url, headers=import_headers)

        repo_migration_status = True if import_confirm.json()['status'] == 'complete' \
            else False

        print("{0}초 후 다시 완료 여부를 확인 합니다...".format(WAIT_TIME))
        time.sleep(WAIT_TIME)

    for download, file in zip(downloads, files):
        release = repo.create_release(download['tag_name'], download['target_commitish'], download['name'],
                                      download['body'], download['draft'], download['prerelease'])

        release.upload_asset('application/'+file['ext'], file['name'], file['raw'])

    return True