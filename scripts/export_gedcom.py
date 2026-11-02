#!/usr/bin/env python3
"""Export a conservative GEDCOM 5.5.1 view without inventing parent roles."""
import argparse
import re
from pathlib import Path
from common import outside_toolkit, fail
from result_view import build_view, ASSERTED, PARENTS, parent_edge

def value(text):
    # Literal @@ is the GEDCOM escape for @; every record stays on one physical line.
    return ' '.join((text or '').replace('@', '@@').split())

def text_lines(level, tag, text):
    text = value(text)
    prefix = f'{level} {tag} '
    # Bound by UTF-8 bytes; GEDCOM 5.5.1 physical lines have a 255-character limit.
    result, chunk = [], ''
    for char in text:
        if len((prefix + chunk + char).encode('utf-8')) > 240:
            result.append(prefix + chunk)
            prefix, chunk = f'{level + 1} CONC ', ''
        chunk += char
    result.append(prefix + chunk)
    return result

def render(view):
    people = {p['id']: p for p in view['people']}
    pid = {key: '@I' + str(i) + '@' for i,key in enumerate(people,1)}
    sources = {s['id']: s for s in view['sources']}
    sid = {key: '@S'+str(i)+'@' for i,key in enumerate(sources,1)}
    families, associations, omitted = {}, [], []
    for r in view['relationships']:
        if r['status'] not in ASSERTED or r['has_contradictions']:
            omitted.append(r)
            continue
        if r['type'] in PARENTS and 'household' not in r['nature'].lower():
            parent, child = parent_edge(r)
            role = 'HUSB' if r['type'] == 'father-of' or people[parent]['sex'] == 'M' else 'WIFE' if r['type'] == 'mother-of' or people[parent]['sex'] == 'F' else None
            if role:
                entry = families.setdefault(child, {'parents': {}, 'edges': []})
                # Competing parents cannot be silently placed into the same exchange role.
                if role in entry['parents'] and entry['parents'][role] != parent:
                    associations.append((parent, child, r))
                else:
                    entry['parents'][role] = parent
                    entry['edges'].append(r)
            else:
                associations.append((parent, child, r))
        elif r['type'] in ('spouse-of', 'married-to'):
            associations.append((r['a'], r['b'], r))
        else:
            omitted.append(r)
    fid = {child:'@F'+str(i)+'@' for i,child in enumerate(families,1)}
    lines = ['0 HEAD', '1 SOUR FAMILY_TREE_RESEARCH', '2 VERS 0.1',
             '1 SUBM @SUB1@', '1 GEDC', '2 VERS 5.5.1', '2 FORM LINEAGE-LINKED',
             '1 CHAR UTF-8', '0 @SUB1@ SUBM', '1 NAME Family Tree Research',
             '0 @N1@ NOTE Research registers retain full uncertainty; this file is an exchange view.']
    for key,p in people.items():
        lines.append('0 '+pid[key]+' INDI')
        lines += text_lines(1, 'NAME', p['name'])
        lines += ['1 REFN '+key]
        if p['sex'] != 'U':
            lines.append('1 SEX '+p['sex'])
        for tag,label in [('BIRT','birth'),('DEAT','death')]:
            date = p[label]
            if date:
                lines.append('1 '+tag)
                if re.fullmatch(r'\d{4}', date):
                    lines.append('2 DATE '+date)
                else:
                    lines += text_lines(2,'NOTE',date+' (as recorded; no date normalization inferred)')
        if key in families:
            lines.append('1 FAMC '+fid[key])
            nature = ' '.join(r['nature'] for r in families[key]['edges']).lower()
            if 'adopt' in nature:
                lines.append('2 PEDI adopted')
            elif 'biological' in nature:
                lines.append('2 PEDI birth')
        for child, f in families.items():
            if key in f['parents'].values():
                lines.append('1 FAMS '+fid[child])
        for a,b,r in associations:
            if a == key:
                lines += ['1 ASSO '+pid[b]] + text_lines(2,'RELA',r['type'])
                lines += text_lines(2,'NOTE',r['id']+'; '+r['status']+'; parent/spouse role not invented')
                lines += ['2 SOUR '+sid[s] for s in r['sources'] if s in sid]
        for r in omitted:
            if r['a'] == key:
                # Keep an explanatory note rather than asserting an unsupported pedigree edge.
                other=people[r['b']]['name']
                lines += text_lines(1,'NOTE',f"Unasserted {r['type']}: {other}; {r['id']}; {r['status']}")
    for child,f in families.items():
        lines += ['0 '+fid[child]+' FAM']
        for role,parent in f['parents'].items():
            lines.append('1 '+role+' '+pid[parent])
        lines.append('1 CHIL '+pid[child])
        for r in f['edges']:
            lines += text_lines(1,'NOTE',r['id']+'; '+r['status']+'; '+r['nature'])
            lines += ['1 SOUR '+sid[s] for s in r['sources'] if s in sid]
    for key,s in sources.items():
        lines.append('0 '+sid[key]+' SOUR')
        lines += text_lines(1,'TITL',s['title'] or key)
        lines += text_lines(1,'NOTE','Evidence ID: '+key+'; '+s['custodian']+'; '+s['reference'])
        if s['url']:
            lines += text_lines(1,'NOTE',s['url'])
    lines.append('0 TRLR')
    return '\n'.join(lines)+'\n'

def export(case, destination, private=False, overwrite=False):
    case=outside_toolkit(case)
    out=outside_toolkit(destination)
    if out.suffix.lower() != '.ged' or out.parent == case or any((case/name).resolve() in out.parents for name in ('originals','sources','photos','work','plan')):
        raise ValueError('Choose a .ged file in a dedicated output folder, not the case root or originals.')
    if out.exists() and not overwrite:
        raise ValueError('Output exists. Use --overwrite to replace it.')
    text=render(build_view(case,private))
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(text,encoding='utf-8')
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--case-dir',required=True)
    p.add_argument('--out',required=True)
    p.add_argument('--private-output',action='store_true')
    p.add_argument('--overwrite',action='store_true')
    a=p.parse_args()
    try:
        print(export(a.case_dir,a.out,a.private_output,a.overwrite))
        return 0
    except (ValueError,OSError,KeyError) as error:
        return fail(error)

if __name__=='__main__':
    raise SystemExit(main())
