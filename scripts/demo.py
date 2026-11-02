#!/usr/bin/env python3
"""Create a wholly fictional external example; never reset an existing case."""
import argparse,csv
from init_case import initialize

def append(case,name,rows):
    path=case/(name+'-register.csv')
    with path.open(encoding='utf-8',newline='') as f: fields=next(csv.reader(f))
    with path.open('a',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fields,extrasaction='ignore');writer.writerows(rows)

def create(destination):
    case=initialize(destination,'Fictional teaching case: compare two recorded parent relationships.','Example family')
    append(case,'person',[
      {'person_id':'P-0001','preferred_label':'Учебный ребёнок','living_status':'deceased','birth_estimate':'1900','death_estimate':'1970','source_artifact_ids':'A-0001'},
      {'person_id':'P-0002','preferred_label':'Учебный родитель','living_status':'deceased','birth_estimate':'1870','death_estimate':'1940','source_artifact_ids':'A-0001'},
      {'person_id':'P-0003','preferred_label':'Сомнительный кандидат','living_status':'deceased'},
      {'person_id':'P-0004','preferred_label':'Private Teaching Person','living_status':'living'}])
    append(case,'artifact',[{'artifact_id':'A-0001','source_title':'Fictional birth entry (not a real archive document)','source_url_or_path':'https://example.invalid/teaching','source_type':'fictional-teaching-record','person_ids':'P-0001;P-0002','provenance_level':'teaching-only','directness':'direct','originality':'image-of-original','independence_group':'DEMO-1','legibility':'clear','status':'lead'}])
    append(case,'claims',[{'claim_id':'C-0001','claim_text':'Fictional parentage example','subject_person_ids':'P-0001;P-0002','claim_type':'parentage','artifact_ids':'A-0001','supporting_independence_groups':'DEMO-1','status':'single-source','rationale':'Wholly fictional teaching fixture, not historical evidence.'}])
    append(case,'relationship',[
      {'relationship_id':'R-0001','person_a_id':'P-0002','person_b_id':'P-0001','relationship_type':'father-of','biological_legal_household':'biological','claim_ids':'C-0001','supporting_artifact_ids':'A-0001','independence_groups':'DEMO-1','status':'single-source','rationale':'Fictional teaching fixture.'},
      {'relationship_id':'R-0002','person_a_id':'P-0003','person_b_id':'P-0001','relationship_type':'parent-of','status':'hypothesis','rationale':'Competing candidate; unsupported edge must not become a pedigree fact.'}])
    return case

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--case-dir',required=True);a=p.parse_args();print(create(a.case_dir))
