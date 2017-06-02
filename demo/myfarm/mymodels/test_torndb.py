#!/usr/bin/python
#coding=utf-8
import torndb
def getTerm(db,tag):
        query = "SELECT term_id FROM wp_terms where name=%s "
        rows = db.query(query,tag)
        termid = []
        for row in rows:
            termid.extend(row.values())
        return termid
def addTerm(db,tag):
        query = "INSERT into wp_terms (name,slug,term_group) values (%s,%s,0)"
        term_id = db.execute_lastrowid(query,tag,tag)
        sql = "INSERT into wp_term_taxonomy (term_id,taxonomy,description) values (%s,'post_tag',%s) "
        db.execute(sql,term_id,tag)
        return term_id
def addCTag(db,data):
        query = "INSERT INTO wp_term_relationships (object_id,term_taxonomy_id) VALUES (%s, %s) "
        db.executemany(query,data)
dbconn = torndb.Connection('localhost:3306','361way',user='root',password='123456')
tags = ['mysql','1111','aaaa','bbbb','ccccc','php','abc','python','java']
tagids = []
for tag in tags:
    termid = getTerm(dbconn,tag)
    if termid:
        print tag, 'tag id is ',termid
        tagids.extend(termid)
    else:
        termid = addTerm(dbconn,tag)
        print 'add tag',tag,'id is ' ,termid
        tagids.append(termid)
print 'All tags id is ',tagids
postid = '35'
tagids = list(set(tagids))
ctagdata = []
for tagid in tagids:
    ctagdata.append((postid,tagid))
addCTag(dbconn,ctagdata)