import re
from pathlib import Path
import base64
from copy import deepcopy
import sys
# sys.setrecursionlimit(5000)

import rdflib
from rdflib import URIRef
import requests
from bs4 import BeautifulSoup
import validators.url

from scipy import io as sio


# TODO check if the rdflib sparql result generator is convertable to a list,
# TODO: if yes check if there is always exactly one entity of something
def follow_all_redirects(persistent_id_url: str, access_token: str =None, break_before_login_flag: bool=True) -> (str, str):
    if access_token:
        headers = {'PRIVATE-TOKEN': access_token}
    else:
        headers = None

    # Try to get the rdf data from the persistent_id_URI
    with requests.Session() as s:
        # 'https://w3id.org/fst/resource/0184ebd9-988b-7bb9-ae4b-17bd29feb36c'
        # TODO: check if the url alredy contains the .ttl or a similar ending
        # TODO: Add content negotiation that it won't be necessary to force the type
        # TODO: FIXME: In a multi stage redirect the access token could be leaked again at this point since the token
        #  should be for the service at the end.
        if headers:
            response_0 = s.get(f'{persistent_id_url}.ttl', headers=headers)
        else:
            response_0 = s.get(f'{persistent_id_url}.ttl')
    # Wenn ein access token gegeben ist muss der direkt mit in den redirect request um an die service URL zu kommen mit
    # der service URL und dem access token-> nein muss er nicht weil ich bei dem derzeitigen System bei einem Anmeldebildschirm lande.
    # Ich muss irgendwie detecten, dass ich nicht bei einer rdf bin und dann eine Fehlermeldung ausgeben bzw, falls ein
    # access tojkmen gegeben ist den request nochmal machen.
    # Derzeit ist es so, dass GitLab aber auch im raw format gesendete Daten im
    # Wenn access denied ist müsste es ein http code dafür geben.
    # TODO: schrieb das alles nochmal sauber in einem ablaufdiagramm auf

    # TODO: There could be multiple .html redirects in the future
    if response_0.headers['Content-Type'] == 'text/html; charset=utf-8':
        # Get thr url inside the old .html file redirect
        soup = BeautifulSoup(response_0.text, 'html.parser')
        meta_tags = soup.find_all('meta')

        compiled_regex = re.compile('url=.* ')
        regex_output = compiled_regex.findall(str(meta_tags))
        redirect_url = regex_output[0].split('url=')
        redirect_file_url_cleaned = redirect_url[1].replace(' ', '').replace('"', '')

        with requests.Session() as s:
            if headers:
                response_1 = s.get(redirect_file_url_cleaned, headers=headers)
            else:
                response_1 = s.get(redirect_file_url_cleaned)
            # TODO: FIXME: The response of GitLab rwth is 'text/plain; charset=utf-8' and should be something like 'text/turtle; charset=utf-8'
            #  -> proposal for the new .html version or at the gitlab site

    # Get the url of the site and the response content text at the end of the redirect
    if (break_before_login_flag
            and response_1
            and ('signin' in response_1.url
                    or 'sign_in' in response_1.url
                    or 'login' in response_1.url
                    or 'login' in response_1.url)):
        # TODO: FIXME: this is hardcoded and only works for our service since the
        end_redirect_url = redirect_file_url_cleaned.replace('.html', '')
        end_redirect_response_text = response_0.text
    else:
        end_redirect_url = response_1.url
        end_redirect_response_text = response_1.text

    return end_redirect_url, end_redirect_response_text


def load_git_rdf(persistent_id_url: str, access_token: str =None) -> (rdflib.Graph, str):
    # TODO: Check if the url is a https URL when a access token is provided to make sure the access token isn't send in clear
    #  text to the first redirect and leaked there. Redirect it with a warning in the log.
    # #### NOTE: Der Fall, dass man auch auf unsupporteten Seiten daten laden möchte ist eh irrelevant wiel ich ohne die
    # API nicht an die sha commits und die versionierung komme.
    # Follow the redirects the first time and check if the end file is of type rdf.
    # if it isn't and a access token is provided try to get it with the access token. zu dem access token sollte noch
    # eine deklaration für die seite zu der er gültig ist, sonst probiert man bei mehreren alle tokens durch.. das mit
    # dem durchprobieren könnte eh wichtig werden wenn man mehrere group acces tokens von anderen forschungsgruppen
    # bekommt.. da wäre es dann aber besser einfach einen nutzer access token zu verwenden, auch wenn er sogesehen unsicherer ist.
    # Lösung ist: es ist derzeit nur möglich seinen eigenen user token zu verwenden und nicht über andere Gruppen
    # -> zusammengefasst wird es sehr schwierig ohne Mehraufwand die zugriffsrechte in gitlab zu ändern, aber das ist
    # ein Gitlab problem und interessiert derzeit noch nicht.
    if access_token:
        end_redirect_url, end_redirect_response_text = follow_all_redirects(persistent_id_url, access_token=access_token)
    else:
        end_redirect_url, end_redirect_response_text = follow_all_redirects(persistent_id_url)

    # Get on which service the file lives (needed for the sha commit (only obtainbale through the API) and if the file is private to retry the request with the access token)
    git_instance_name = get_git_instance_service(end_redirect_url)
    # Check if the service is supported
    SUPPORTED_GIT_INSTANCE_SERVICES = ['GitLab']
    if not git_instance_name:
        # TODO: FIXME: Maybe move the code into the get_git_instance_service function. There might be more general
        #  functions on the internet that detect all services and I just need to match the got one with the supported
        #  list later. The services could als be detected through ports or responses to generel requests. That is also
        #  used in hacking for example in nmap to find possible vulnerable sites -> in germany probably a 'Grauzone'
        # TODO: FIXME: Find a better suiting exception
        raise Exception((f"The git instance service couldn't be got!"))
    if not git_instance_name in SUPPORTED_GIT_INSTANCE_SERVICES:
        raise Exception((f"The git instance service you provided '{git_instance_name}' is currently not supported!\n"
                         f"The currently supported ones are: {SUPPORTED_GIT_INSTANCE_SERVICES}"))

    g = rdflib.Graph()
    try:
        g.parse(data=end_redirect_response_text, format="turtle", publicID=persistent_id_url)
    # FIXME: TODO: Search for a better suiting exception class
    # TODO: problem is the file could be obtainable but isn't in a rdf format I could check that with the sha commit
    except Exception:
        # FIXME: ##### WARN: INSECURE! Because retry #########
        #  If I just retry with the access key the key might be leaked to a different malicious site
        # Retry the request through the API with the access token
        # NOTE: end_redirect_url could be in this case the login URL therefore the whole request needs to be redone.
        if access_token:
            rdf_content, version_commit_id = get_GitLab_file_content_and_version_commit_id(end_redirect_url,
                                                                                           access_token=access_token)
        else:
            raise

    else:
        rdf_content, version_commit_id = get_GitLab_file_content_and_version_commit_id(end_redirect_url)

    g = rdflib.Graph()
    g.parse(data=rdf_content, format="turtle", publicID=persistent_id_url)

    return [g, version_commit_id]


def parse_url_into_parts(url) -> dict:
    # Split the URL in its parts
    # TODO: maybe replace https or
    parted_url = url.split('//')
    splitted_repository_url_list = parted_url[1].split('/-/')
    splitted_url = splitted_repository_url_list[0].split('/')
    splitted_file_path_url = splitted_repository_url_list[1].split('/')

    domain_address = splitted_url[0]
    base_url = f'https://{domain_address}'

    project_path_list = splitted_url[1:]
    project_path_url = ''
    for item in project_path_list:
        if project_path_url == '':
            project_path_url = f'{item}'
        else:
            project_path_url = f'{project_path_url}/{item}'

    file_path = ''
    for item in splitted_file_path_url[2:]:
        if file_path == '':
            file_path = f'{item}'
        else:
            file_path = f'{file_path}/{item}'

    return_variables_dict = {
        'base_url': base_url,
        'project_path_url': project_path_url,
        'repository_file_path': file_path
    }

    return return_variables_dict


def get_git_instance_service(url: str) -> str:
    return_variables_dict = parse_url_into_parts(url)
    # Get wether the service lives on GitLab or something else
    # TODO: github gitea
    with requests.Session() as s:
        r = s.get(return_variables_dict['base_url'])
    soup = BeautifulSoup(r.text, 'html.parser')

    # ich möchte alle meta tags finden, die das property attribute haben
    def is_meta_tag_with_property_attribute(tag):
        # Filter funktion return true or false
        return tag.name == 'meta' and tag.has_attr('property') and tag['property'] == 'og:site_name'

    # FIXME: TODO: The site name might not always indicate which service is used. But the one from the GitLab RWTH does.
    meta_site_name_soup = soup.find_all(is_meta_tag_with_property_attribute)
    try:
        git_instance_name = meta_site_name_soup[0]['content']  # In the GitLab RWTH case it is 'GitLab'
    except Exception:
        git_instance_name = None

    return git_instance_name


def get_GitLab_file_content_and_version_commit_id(url, access_token:str=None):
    # TODO: Other services should be supported too. This functions should be outsourced into their own files.
    # TODO: declare this function as private and create a get_rdf_file_content_and_version_commit_id function and add
    #  at position one a argument service_id or service_name and match it to the supported ones and call the private
    #  functions.
    if access_token:
        headers = {'PRIVATE-TOKEN': access_token}
    else:
        headers = None
    return_variables_dict = parse_url_into_parts(url)


    api_base_url = f"{return_variables_dict['base_url']}/api/v4/"

    #### Ab hier nur für GitLab
    # Get project id
    with requests.Session() as s:
        project_path_url_encoded = requests.utils.quote(return_variables_dict['project_path_url'], safe='')
        if headers:
            r = s.get(f"{api_base_url}/projects/{project_path_url_encoded}", headers=headers)
        else:
            r = s.get(f"{api_base_url}/projects/{project_path_url_encoded}")

    projectid = r.json()['id']  # '84807'

    with requests.Session() as s:
        # /projects/:id/repository/files/:file_path
        URLencodedfilepath = requests.utils.quote(return_variables_dict['repository_file_path'], safe='')
        # TODO: FIXME: tokens from a token vault need to be used here
        # TODO: main branch is sleected, might be a problem in the future if useres aren't consistent with their branches
        file_api_url = f'{api_base_url}/projects/{projectid}/repository/files/{URLencodedfilepath}?ref=main'
        if headers:
            response = s.get(file_api_url, headers=headers)
        else:
            response = s.get(file_api_url)

    # Decode the Base64 encoded content of the file
    decoded_content = base64.b64decode(response.json()['content']).decode('utf-8')
    # TODO: Check if the encoding is base64 and what the https encoding (usually utf-8) is

    return decoded_content, response.json()['commit_id']


def save_online_RDF_dict_as_mat_file(pID_url: str, online_rdf_dict: dict, save_to_directory_path: [Path, str]) -> None:
    # TODO: check wether the URL varaible is a url and a persistent one
    UUID = pID_url.split("/")[-1]
    file_name = f'pID_{UUID.replace("-", "_")}'

    save_dict = {f'{file_name}': online_rdf_dict}
    # self.assertEqual(mat_struct['example_mat_struct'], x)
    sio.savemat(f'{save_to_directory_path}/{file_name}.mat', save_dict)