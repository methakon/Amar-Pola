#!/usr/bin/env python3
"""Export PostgreSQL catalog facts and source-linked schema/API traceability.

Catalog only: no application rows, role passwords, tokens or connection strings.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import manage

ALIASES = {
 'adult_accounts':['parent_principals'], 'family_memberships':['guardian_memberships'],
 'family_revocation_epochs':['revocation_epochs'], 'child_devices':['devices'],
 'device_commands':['commands'], 'device_sessions':['trusted_sessions'],
 'parent_auth_sessions':['trusted_sessions'], 'app_usage_events':['app_usage_intervals'],
 'child_checkins':['child_signals'], 'sos_events':['child_signals'],
 'sos_acknowledgements':['signal_acknowledgements'], 'geofence_events':['alert_events'],
 'admin_principals':['admin_accounts'], 'admin_read_audit':['admin_support_read_audit'],
 'support_cases':['support_tickets'], 'export_requests':['export_jobs','media_export_requests'],
 'purpose_authorizations':['consent_records'], 'reconstruction_jobs':['ingestion_outbox'],

 'usage_permission_checks':['permission_snapshots','app_usage_intervals'],
 # Historical screen-register spellings; V2 is the current authorization source.
 'child_guardian_grants':['child_access_grants_v2'], 'child_parent_verifications':['child_authority_reviews'],
}
FUNCTION_ALIASES = {'history_visibility_rules':['can_read_location_history']}
HANDLERS = {'GET /parents/me':'profile', 'GET /children/{childId}':'child',
            'GET /families/{familyId}/children':'children', 'GET /children/{childId}/consents':'consents'}


def read_json(path):
    return json.loads(path.read_text())


def normalize(route):
    return re.sub(r'\{[^}]+\}','{id}',route)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def catalog(database):
    with manage.connect(database,'admin') as conn:
        objects=[]
        for schema,name,kind,rls,forced in conn.execute("""SELECT n.nspname,c.relname,c.relkind,c.relrowsecurity,c.relforcerowsecurity
          FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
          WHERE n.nspname IN ('ap_m1','ma_migrations','ma_recovery') AND c.relkind IN ('r','p','v') ORDER BY n.nspname,c.relname"""):
            columns=conn.execute("""SELECT a.attname,format_type(a.atttypid,a.atttypmod),a.attnotnull,
              pg_get_expr(d.adbin,d.adrelid) FROM pg_attribute a LEFT JOIN pg_attrdef d ON d.adrelid=a.attrelid AND d.adnum=a.attnum
              WHERE a.attrelid=(%s||'.'||%s)::regclass AND a.attnum>0 AND NOT a.attisdropped ORDER BY a.attnum""",(schema,name)).fetchall()
            constraints=conn.execute("SELECT conname,contype,pg_get_constraintdef(oid) FROM pg_constraint WHERE conrelid=(%s||'.'||%s)::regclass ORDER BY conname",(schema,name)).fetchall()
            objects.append({'schema':schema,'name':name,'kind':kind,'rls':rls,'forced_rls':forced,
                            'columns':[dict(name=v[0],type=v[1],not_null=v[2],default=v[3]) for v in columns],
                            'constraints':[dict(name=v[0],kind=v[1],definition=v[2]) for v in constraints]})
        indexes=[dict(schema=r[0],table=r[1],name=r[2],definition=r[3]) for r in conn.execute("SELECT schemaname,tablename,indexname,indexdef FROM pg_indexes WHERE schemaname IN ('ap_m1','ma_migrations','ma_recovery') ORDER BY schemaname,indexname")]
        policies=[dict(schema=r[0],table=r[1],name=r[2],roles=r[3],command=r[4],using=r[5],check=r[6]) for r in conn.execute("SELECT schemaname,tablename,policyname,roles::text[],cmd,qual,with_check FROM pg_policies WHERE schemaname IN ('ap_m1','ma_recovery') ORDER BY schemaname,tablename,policyname")]
        functions=[dict(schema=r[0],name=r[1],signature=r[2],security_definer=r[3],owner=r[4],settings=r[5]) for r in conn.execute("SELECT n.nspname,p.proname,pg_get_function_identity_arguments(p.oid),p.prosecdef,pg_get_userbyid(p.proowner),p.proconfig FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname IN ('ap_m1','ma_recovery') ORDER BY n.nspname,p.proname,p.oid")]
        foreign_keys=[dict(table_schema=r[0],table=r[1],target_schema=r[2],target=r[3],name=r[4]) for r in conn.execute("SELECT n.nspname,c.relname,rn.nspname,rc.relname,k.conname FROM pg_constraint k JOIN pg_class c ON c.oid=k.conrelid JOIN pg_namespace n ON n.oid=c.relnamespace JOIN pg_class rc ON rc.oid=k.confrelid JOIN pg_namespace rn ON rn.oid=rc.relnamespace WHERE k.contype='f' AND n.nspname IN ('ap_m1','ma_recovery') ORDER BY c.relname,k.conname")]
    return {'objects':objects,'indexes':indexes,'policies':policies,'functions':functions,'foreign_keys':foreign_keys}


def build(database):
    root=manage.ROOT
    data=catalog(database)
    names={o['name'] for o in data['objects'] if o['schema']=='ap_m1'}
    functions={f['name'] for f in data['functions'] if f['schema']=='ap_m1'}
    model=read_json(root/'docs/data-model/MADALASA_ALARKA_FIGMA_LOGICAL_ERD_V1_2026.json')
    mappings=[];missing=[]
    for domain in model['domains']:
        for entity in domain['tables']:
            name=entity['name']
            targets=ALIASES.get(name,[name])
            fn=[]
            if not set(targets)<=names and name in FUNCTION_ALIASES:
                targets=[];fn=FUNCTION_ALIASES[name]
            absent=set(targets)-names | (set(fn)-functions)
            if absent:missing.append({'concept':name,'missing':sorted(absent)})
            mappings.append({'concept':name,'domain':domain['title'],'physical_objects':['ap_m1.'+v for v in targets],
                             'functions':['ap_m1.'+v for v in fn], 'representation':'DIRECT' if targets==[name] else 'NORMALIZED_OR_DERIVED',
                             'scope':'PHYSICAL_SCHEMA_NOT_API_OR_ANDROID_COMPLETION'})
    if missing:raise ValueError('Unmapped logical dependencies: '+json.dumps(missing))
    assert len(mappings)==len({m['concept'] for m in mappings})==model['tableCount']
    logical={m['concept']:m['physical_objects'] for m in mappings}
    coverage=read_json(root/'docs/audits/POST_REMEDIATION_SCREEN_API_DB_COVERAGE_2026-10-28.json')['screen_coverage']
    routes={}
    for screen in coverage:
        for route in set(screen['documented_routes_in_current_draft']+screen['supplemental_draft_routes']):
            value=routes.setdefault(normalize(route),{'screens':[],'objects':set(),'unmapped_screen_terms':set()})
            value['screens'].append({'source':screen['source'],'screen':screen['screen_key'],'figma_node_id':screen['figma_node_id']})
            for term in screen['related_logical_tables']:
                if term in logical:value['objects'].update(logical[term])
                elif term in ALIASES and set(ALIASES[term])<=names:value['objects'].update('ap_m1.'+v for v in ALIASES[term])
                elif term in names:value['objects'].add('ap_m1.'+term)
                else:value['unmapped_screen_terms'].add(term)
    spec=read_json(root/'docs/openapi.yaml');api=[]
    for path,item in spec['paths'].items():
        for method,operation in item.items():
            if method not in ('get','post','patch','put','delete'):continue
            key=method.upper()+' '+path
            match=routes.get(normalize(key),{'screens':[],'objects':set(),'unmapped_screen_terms':set()})
            api.append({'operation':key,'operation_id':operation['operationId'],'physical_dependencies':sorted(match['objects']),
                        'source_screens':match['screens'],'unmapped_historical_terms':sorted(match['unmapped_screen_terms']),
                        'mapping_method':'SCREEN_REGISTER_DEPENDENCY_NOT_HANDLER_BINDING',
                        'handler':'backend/src/Database.cc:'+HANDLERS[key] if key in HANDLERS else None,
                        'handler_status':'IMPLEMENTED_LOCAL_SESSION_ADAPTER' if key in HANDLERS else 'PENDING',
                        'http_acceptance':'SEE_EXECUTED_EVIDENCE' if key in HANDLERS else 'NOT_IMPLEMENTED',
                        'android_integration':'NOT_RUN'})
    manifest={'historical_0001_sha256':manage.BASELINE_SHA256,'runner':'tools/database/manage.py',
              'migrations':[{'version':p.name[:4],'file':str(p.relative_to(root)),'sha256':digest(p)} for p in sorted(manage.MIGRATIONS.glob('[0-9][0-9][0-9][0-9]_*.sql'))]}
    erd=['# Physical PostgreSQL foreign-key ERD','','Generated from actual catalog foreign keys, not conceptual table counts. Views and authorization functions are separately enumerated in physical-schema.json.','','```mermaid','erDiagram']
    seen=set()
    for fk in data['foreign_keys']:
        key=(fk['target'],fk['table'])
        if key in seen:continue
        seen.add(key)
        erd.append('  '+fk['target']+' ||--o{ '+fk['table']+' : references')
    erd+=['```','']
    return {'physical-schema.json':json.dumps(data,indent=2)+'\n',
            'logical-to-physical.json':json.dumps({'concept_count':len(mappings),'source_model':model['fileKey'],'mappings':mappings},indent=2)+'\n',
            'api-to-table.json':json.dumps({'operation_count':len(api),'canonical_screen_count':len(coverage),'operations':api},indent=2)+'\n',
            'migration-manifest.json':json.dumps(manifest,indent=2)+'\n','PHYSICAL_ERD.md':'\n'.join(erd)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database',choices=manage.DATABASES,default='test')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    destination=manage.ROOT/'docs/data-model/local-postgresql'
    result=build(args.database)
    for name,content in result.items():
        path=destination/name
        if args.check:
            if not path.exists() or path.read_text()!=content:raise ValueError('Catalog/traceability drift: '+name)
        else:path.write_text(content)
    print('Catalog and traceability '+('verified' if args.check else 'exported')+': '+str(len(result))+' artifacts')


if __name__=='__main__':main()
