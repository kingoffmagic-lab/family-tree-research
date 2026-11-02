"""A deliberately small output view, separate from the evidence registers."""
import re
from urllib.parse import urlsplit
from common import table, ids, audit

DECEASED = {'deceased', 'dead'}
ASSERTED = {'single-source', 'corroborated', 'strongly-corroborated'}
PARENTS = {'parent-of', 'father-of', 'mother-of', 'child-of'}

def safe_url(value):
    try:
        parts = urlsplit(value)
        if parts.scheme in ('https', 'http') and parts.hostname and not parts.username and not parts.password:
            if any(key in parts.query.lower() for key in ('token=', 'session=', 'password=', 'auth=')):
                return ''
            return value
    except ValueError:
        pass
    return ''

def build_view(case, private=False, root_person=None):
    audited = audit(case)
    raw = table(case, 'person')
    hidden = [p for p in raw if p.get('living_status', '').strip().lower() not in DECEASED] if not private else []
    forbidden = set()
    for person in hidden:
        for value in [person.get('preferred_label', ''), *ids(person.get('names_as_written', '')),
                      *ids(person.get('normalized_name_variants', ''))]:
            if value.strip():
                forbidden.add(value.strip())
    def clean(text):
        text = text or ''
        for name in sorted(forbidden, key=len, reverse=True):
            text = re.sub(re.escape(name), '[private person]', text, flags=re.I)
        return text
    people = []
    for p in raw:
        if not private and p.get('living_status', '').strip().lower() not in DECEASED:
            continue
        people.append({'id': p['person_id'], 'name': clean(p.get('preferred_label') or p.get('names_as_written') or p['person_id']),
                       'birth': clean(p.get('birth_estimate', '')), 'death': clean(p.get('death_estimate', '')),
                       'sex': p.get('sex', '').upper() if p.get('sex', '').upper() in ('M', 'F', 'U') else 'U'})
    visible = {p['id'] for p in people}
    if root_person and root_person not in visible:
        raise ValueError('Requested root is absent from the selected output view. Choose a deceased root or request --private-output.')
    artifacts = {}
    for a in table(case, 'artifact'):
        associated = set(ids(a.get('person_ids', '')))
        if not private and (not associated or not associated <= visible):
            continue
        url = safe_url(a.get('source_url_or_path', ''))
        if not private and any(name.casefold() in url.casefold() for name in forbidden):
            url = ''
        artifacts[a['artifact_id']] = {
            'id': a['artifact_id'], 'title': clean(a.get('source_title', '')),
            'custodian': clean(a.get('repository_or_archive', '')),
            'reference': clean(a.get('archival_reference', '')), 'url': url}
    claims = {c['claim_id']: c for c in table(case, 'claims')
              if set(ids(c.get('subject_person_ids', ''))) <= visible}
    relations = []
    for r in table(case, 'relationship'):
        if r.get('person_a_id') not in visible or r.get('person_b_id') not in visible:
            continue
        references = set(ids(r.get('supporting_artifact_ids', '')))
        for cid in ids(r.get('claim_ids', '')):
            references.update(ids(claims.get(cid, {}).get('artifact_ids', '')))
        relations.append({'id': r['relationship_id'], 'a': r['person_a_id'], 'b': r['person_b_id'],
                          'type': r.get('relationship_type', ''), 'status': r.get('status', ''),
                          'nature': r.get('biological_legal_household', ''),
                          'sources': sorted(references & artifacts.keys()),
                          'has_contradictions': bool(ids(r.get('contradicting_artifact_ids', '')) or
                              any(ids(claims.get(cid, {}).get('contradicting_artifact_ids', '')) or
                                  claims.get(cid, {}).get('status') == 'contradicted'
                                  for cid in ids(r.get('claim_ids', ''))))})
    used = {ref for r in relations for ref in r['sources']}
    for p in raw:
        if p['person_id'] in visible:
            used.update(ids(p.get('source_artifact_ids', '')))
    return {'people': people, 'relationships': relations,
            'sources': [artifacts[ref] for ref in sorted(used & artifacts.keys())],
            'root': root_person or (people[0]['id'] if people else None),
            'private': private, 'audit_warning_count': len(audited.get('warnings', []))}

def parent_edge(relation):
    if relation['type'] == 'child-of':
        return relation['b'], relation['a']
    return relation['a'], relation['b']
