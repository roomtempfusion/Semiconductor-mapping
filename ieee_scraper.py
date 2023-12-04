#V2.2: New, improved and CAPTCHA free + chart + map

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# search term
search_query = 'semiconductor'

#rows per page: 10, 25, 50
rows_per_page = 10

# initialize result lists
title_list = []
author_list = []
journal_list = []
year_list = []
citations_list = []
paper_cite_list = []
patent_cite_list = []
link_list = []
affiliations_list = []
country_list = []
abstract_list = []
ieee_keys = []
inspec_keys = []
author_keys = []
acknowledgement_list = []
def replace_country_name(input_str):

    country_dict = {
        'US': 'United States',
        'USA': 'United States',
        'CN': 'China',
        'P. R. China': 'China',
        'MD': 'United States',
        'FL': 'United States',
        'OR': 'United States',
        'ID': 'United States',
        'R.O.C': 'Taiwan',
        'R.O.C.': 'Taiwan',
        'ROC': 'Taiwan',
        'TW': 'Taiwan',
        'U.K': 'UK',
        'U.K.': 'UK',
        'JP': 'Japan',
        'Republic of Korea': 'South Korea',
        'Korea': 'South Korea',
        'The Netherlands': 'Netherlands'
    }

    # Convert input string to uppercase for case-insensitive matching
    input_str_upper = input_str.upper()

    for abbreviation, full_name in country_dict.items():
        if input_str_upper == abbreviation.upper():
            return full_name
    return input_str


# loop through pages
for i in range(1, 2):

    driver.get(f'https://ieeexplore.ieee.org/search/searchresult.jsp?queryText={search_query}&highlight=true&returnType=SEARCH&matchPubs=true&ranges=2000_2024_Year'
               f'&returnFacets=ALL&refinements=ContentType:Journals&pageNumber={i}&rowsPerPage={rows_per_page}')
    # add &refinements=ContentType:Conferences in to include conference papers
    print(i)
    # Allow time for the results to load
    time.sleep(2)

    # Extract information from the page
    results = driver.find_elements(By.CLASS_NAME, 'List-results-items')
    if len(results) != 25:
        time.sleep(1)
    results = driver.find_elements(By.CLASS_NAME, 'List-results-items')

    for result in results:

        # get url
        link = result.find_element(By.CLASS_NAME, 'fw-bold').get_attribute('href')

        # Given string
        input_string = result.text
        #print(input_string)
        # Split the input string into lines
        lines = input_string.split('\n')
        if 'Conference Paper' in input_string and 'HTML' in input_string:
            lines.pop()
        #print(lines)
        # Extracting info - check for citations
        title = lines[0]
        if 'Conference Paper' in input_string:
            if 'Cited by' in lines[-2]:
                authors = [author.strip(';') for author in lines[1:-5]]
                journal = lines[-4]
                cite_line = lines[-2].split(' ')
                papers_cited = cite_line[3].strip('(').strip(')')
                year = lines[-3].split('|')[0][-5:-1]
                if 'Patents' in lines[-3]:
                    patents_cited = cite_line[-1].strip('(').strip(')')
                else:
                    patents_cited = 0
            else:
                authors = [author.strip(';') for author in lines[1:-3]]
                journal = lines[-3]
                year = lines[-2].split('|')[0][-5:-1]
                papers_cited = 0
                patents_cited = 0
        else:
            if 'Cited by' in lines[-3]:
                authors = [author.strip(';') for author in lines[1:-5]]
                journal = lines[-5]
                cite_line = lines[-3].split(' ')
                papers_cited = cite_line[3].strip('(').strip(')')
                year = lines[-4].split('|')[0][-5:-1]
                if 'Patents' in lines[-3]:
                    patents_cited = cite_line[-1].strip('(').strip(')')
                else:
                    patents_cited = 0
            else:
                authors = [author.strip(';') for author in lines[1:-4]]
                journal = lines[-4]
                year = lines[-3].split('|')[0][-5:-1]
                papers_cited = 0
                patents_cited = 0

        # Add the results to the list
        title_list.append(title)
        author_list.append(authors)
        journal_list.append(journal)
        try:
            year_list.append(int(year))
        except Exception:
            year_list.append(0)
        try:
            paper_cite_list.append(int(papers_cited))
        except Exception:
            paper_cite_list.append(0)
        try:
            patent_cite_list.append(int(patents_cited))
        except Exception:
            patent_cite_list.append(0)
        link_list.append(link)

# Get author affiliations
# Only includes primary affiliation as listed on IEEE - done in order to filter out bios etc.
for link in link_list:
    # navigate to each page
    driver.get(link + 'authors#authors')

    # initialize list for each paper
    paper_aff_list = []
    time.sleep(1)

    # Scrape HTML
    aff = driver.find_elements(By.CLASS_NAME, 'author-card.text-base-md-lh')

    # Remove header and randomly long next lines
    abstract = driver.find_elements(By.CLASS_NAME, "abstract-text.row.g-0")[0].text.replace('Abstract:', '').replace('\n', '')

    # iterate through each author
    for affiliation in aff:
        resp = affiliation.text

        resp = resp.split('\n')[1:]
        # check if empty (script returns an equal number of empty v actual)

        if len(resp) == 0:
            continue
        # add to paper list
        paper_aff_list.append(resp[0])
    # add to overall list
    affiliations_list.append(list(set(paper_aff_list)))
    abstract_list.append(abstract)

    try:
        specific_h3_element = driver.find_element(By.XPATH,"//h3[text()='ACKNOWLEDGMENT']")
        # Find the <p> element following the specific <h3> element
        next_p_element = specific_h3_element.find_element(By.XPATH,"following-sibling::p")
        # Print the text content of the <p> element
        acknowledgement_list.append(next_p_element.text)
    except:
        acknowledgement_list.append('')


    driver.get(link + 'keywords#keywords')
    time.sleep(1)
    keywords = driver.find_elements(By.CLASS_NAME, 'doc-keywords-list-item')
    ieee = False
    inspec = False
    author = False
    for result in keywords:
        if 'IEEE Keywords' in result.text:
            ieee_keys.append(result.text.replace('\n', ' ').replace('IEEE Keywords ', '')
                             .split(' , '))
            ieee = True
            continue
        if 'INSPEC: Controlled Indexing' in result.text:
            inspec_keys.append(result.text.replace('\n', ' ')
                               .replace('INSPEC: Controlled Indexing ', '')
                               .split(' , '))
            inspec = True
            continue
        if 'Author Keywords' in result.text:
            author_keys.append(result.text.replace('\n', ' ').replace('Author Keywords ', '')
                               .split(' , '))
            author = True
            continue
    if ieee is False:
        ieee_keys.append([])
    if inspec is False:
        inspec_keys.append([])
    if author is False:
        author_keys.append([])

# generate country data
# countries based on primary institutional affiliation

for paper in affiliations_list:
    paper_country_list = []
    for institution in paper:
        # print(institution)
        country = institution.split(', ')[-1]

        # check for abbreviations
        country = replace_country_name(country)

        # add to list of affiliations for the paper
        paper_country_list.append(country)
    country_list.append(list(set(paper_country_list)))


# add lists to dict
result_dict = {'Title': title_list, 'Author(s)': author_list, 'Journal': journal_list, 'Year': year_list,
               '# times Cited (Papers)': paper_cite_list,
               '# times Cited (Patents)': patent_cite_list, 'URL': link_list, 'Affiliations': affiliations_list,
               'Countries': country_list, 'Abstract': abstract_list, 'IEEE Keywords': ieee_keys,
               'INSPEC Keywords': inspec_keys, 'Author Keywords': author_keys, 'Acknowledgments': acknowledgement_list}

driver.quit()
# convert to dataframe
df_out = pd.DataFrame(data=result_dict)
df_out['Author(s)'] = df_out['Author(s)'].apply(lambda x: json.dumps(x) if isinstance(x, (list, set)) else x)
df_out['Affiliations'] = df_out['Affiliations'].apply(lambda x: json.dumps(x) if isinstance(x, (list, set)) else x)
df_out['IEEE Keywords'] = df_out['IEEE Keywords'].apply(lambda x: json.dumps(x) if isinstance(x, (list, set)) else x)
df_out['INSPEC Keywords'] = df_out['INSPEC Keywords'].apply(lambda x: json.dumps(x) if isinstance(x, (list, set)) else x)
df_out['Author Keywords'] = df_out['Author Keywords'].apply(lambda x: json.dumps(x) if isinstance(x, (list, set)) else x)

print(df_out)

# convert to csv
df_out.to_csv('ieee_test.csv', index=False)

# Generate chart
# Flatten sets
# df = df.explode('Countries')
#
# # Group by country and sum the paper counts
# total_papers_by_country = df.groupby('Countries')['# times Cited (Papers)'].sum().reset_index()
#
# # Sort the DataFrame by number of citations in descending order
# total_papers_by_country = total_papers_by_country.sort_values(by='# times Cited (Papers)', ascending=True)
#
# # Plot the horizontal bar chart
# plt.barh(total_papers_by_country['Countries'], total_papers_by_country['# times Cited (Papers)'])
# plt.xlabel('Number of Citations')
# plt.ylabel('Countries')
# plt.yticks(range(len(total_papers_by_country['Countries'])), total_papers_by_country['Countries'])
# plt.title('Total Number of IEEE Citations by Country')
# plt.subplots_adjust(left=0.3)  # Adjust left margin to make room for country names
# plt.show()
