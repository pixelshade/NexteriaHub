import requests
from bs4 import BeautifulSoup
import urllib
import json
import credentials

client = requests.Session()

HOMEPAGE_URL = 'https://www.linkedin.com'
LOGIN_URL = 'https://www.linkedin.com/uas/login-submit'

html = client.get(HOMEPAGE_URL).content
soup = BeautifulSoup(html)
csrf = soup.find(id="loginCsrfParam-login")['value']

login_information = credentials.login_information
login_information['loginCsrfParam'] = csrf

client.post(LOGIN_URL, data=login_information)

url = 'https://www.linkedin.com/in/pejko-kukac-058917b2'
url = 'https://www.linkedin.com/in/peter-%C5%A1ul%C3%ADk-6183a270'


def parse_job(background_tag):
	if(background_tag.h4 is None):
		return None
	desc = background_tag.find(class_ = 'description summary-field-show-more')
	if(desc is not None):
		desc = desc.text
	else:
		desc = ''
	job = {
		'company': background_tag.h4.next_sibling.text,
		'time': background_tag.find(class_ = 'experience-date-locale').text,
		'position':background_tag.h4.text,
		'desc': desc 
	}
	return job

def get_profile(url):
	# url = 'https://www.linkedin.com/in/'+url_id
	html = client.get(url).content
	
	profile = {}

	# f = open('page.html','w')
	# f.write(html)
	# f.close()

	soup = BeautifulSoup(html)
	fullname = soup.find('h1').text
	headline = soup.find(id="headline-container").text
	industry = soup.find(attrs={'name':'industry'}).text
	location = soup.find(attrs={'name':'location'}).text
	linkedin = soup.find('a', class_="view-public-profile")['href']
	
	past =  soup.find_all('div',class_="editable-item section-item past-position")
	current = soup.find_all('div',class_="editable-item section-item current-position")
	ppic_div = soup.find('div',class_="profile-picture")
	# print ppic_div
	if(ppic_div is not None):
		pic_url = ppic_div.img['src']
	else:
		pic_url = ''
	edu_div = soup.find(id='background-education')	
	education = []
	for school in edu_div.h4:
		education.append(school.text)
# INTERESTS
	interests = []
	interests_tag = soup.find('ul',class_='interests-listing')
	if(interests_tag is not None):
		for li in interests_tag.find_all('li'):
			interests.append(li.text)
# LANGUAGES
	languages = []
	lang_div = soup.find('div',id='languages-view')
	if(lang_div is not None):
		langs = lang_div.find_all('h4')
		for lang in langs:
			languages.append(lang.text)

# PROJECTS
	projects_div = soup.find('div',id="background-projects")
	projects = []
	if(projects_div is not None):
		projs = projects_div.find_all(class_ ='editable-item section-item')
		for p in projs:			
			proj = {
				'name': p.h4.text,
				'date': p.p.text
			}
			projects.append(proj)
# SKILLS
	skills = []
	skills_list = soup.find(id='profile-skills').ul
	if(skills_list is not None):
		for skill in skills_list:
			skills.append(skill.text)
	skills_list = soup.find(class_='skills-section compact-view')
	if(skills_list is not None):
		for skill in skills_list:
			skills.append(skill.text)


# JOBS
	jobs_previous = []
	jobs_current = []
	for tag in past:
		for e in tag.contents:
			# print e.text
			job = parse_job(e)
			# print job
			jobs_previous.append(job)
	
	for tag in current:	
		for e in tag.contents:
			job = parse_job(e)
			# print job
			jobs_current.append(job)

	profile['fullname'] = fullname
	profile['headline'] = headline
	profile['industry'] = industry
	profile['location'] = location
	profile['current'] = jobs_current
	profile['previous'] = jobs_previous
	profile['pic_url'] = pic_url
	profile['projects'] = projects
	profile['skills'] = skills	
	profile['linkedin'] = linkedin
	profile['education'] = education
	profile['interests'] = interests
	profile['languages'] = languages
	return profile

def find_profile_url(name):
	# search_url ='https://www.linkedin.com/ta/federator?verticalSelector=people&query='+urllib.quote_plus(name)+'&tracking=true'
	# r = requests.get(search_url)
	# json_parsed = r.json()
	# res = json_parsed['resultList']
	# print json_parsed
	# for p in res:
	# 	print p['url']
	search_url = 'https://www.linkedin.com/vsearch/f?type=all&keywords='+urllib.quote_plus(name)
	search_html = client.get(search_url).content

	# f = open('page.html','w')
	# f.write(search_html)
	# f.close()
	search_soup = BeautifulSoup(search_html)
	
	profiles = search_soup.find(id='voltron_srp_main-content').string
	profiles =  profiles.replace('\u002d1','0')
	parsed = json.loads(profiles)
	results = parsed['content']['page']['voltron_unified_search_json']['search']['results']
	urls = []
	for r in results:
		if('person' in r):
			urls.append(r['person']['link_nprofile_view_4'])			
	return urls



urls = find_profile_url('peter sulik')
print get_profile(urls[0])