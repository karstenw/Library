<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: http://leoeditor.com/leo_toc.html -->
<leo_file xmlns:leo="http://leoeditor.com/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2" tnodes="0" max_tnode_index="0" clone_windows="0"/>
<globals body_outline_ratio="0.5" body_secondary_ratio="0.5">
	<global_window_position top="50" left="50" height="500" width="700"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="karstenw.20230716135655.2" a="E"><vh>CODE</vh>
<v t="karstenw.20230716135718.1" a="E"><vh>@clean __init__.py</vh>
<v t="karstenw.20230716135752.1"><vh>Credits</vh></v>
<v t="karstenw.20230716135730.1"><vh>Declarations</vh></v>
<v t="karstenw.20230716135829.1" a="E"><vh>DATABASE</vh>
<v t="karstenw.20230716135730.2" a="E"><vh>class Database</vh>
<v t="karstenw.20230716135730.3"><vh>__init__</vh></v>
<v t="karstenw.20230716135730.4"><vh>connect</vh></v>
<v t="karstenw.20230716135730.5"><vh>create</vh></v>
<v t="karstenw.20230716135730.6"><vh>__len__</vh></v>
<v t="karstenw.20230716135730.7"><vh>__getitem__</vh></v>
<v t="karstenw.20230716135730.8"><vh>tables</vh></v>
<v t="karstenw.20230716135730.9"><vh>create_table</vh></v>
<v t="karstenw.20230716135730.10"><vh>create_index</vh></v>
<v t="karstenw.20230716135730.11"><vh>commit</vh></v>
<v t="karstenw.20230716135730.12"><vh>close</vh></v>
<v t="karstenw.20230716135730.13"><vh>sql</vh></v>
<v t="karstenw.20230716135730.14"><vh>dump</vh></v>
<v t="karstenw.20230716135730.15"><vh>_dump_xml</vh></v>
</v>
<v t="karstenw.20230716135730.16" a="E"><vh>class Table</vh>
<v t="karstenw.20230716135730.17"><vh>__init__</vh></v>
<v t="karstenw.20230716135730.18"><vh>_get_name</vh></v>
<v t="karstenw.20230716135730.19"><vh>__len__</vh></v>
<v t="karstenw.20230716135730.20"><vh>find</vh></v>
<v t="karstenw.20230716135730.21"><vh>all</vh></v>
<v t="karstenw.20230716135730.22"><vh>fields</vh></v>
<v t="karstenw.20230716135730.23"><vh>append</vh></v>
<v t="karstenw.20230716135730.24"><vh>edit</vh></v>
<v t="karstenw.20230716135730.25"><vh>remove</vh></v>
</v>
</v>
<v t="karstenw.20230716135914.1" a="E"><vh>newHeadline</vh>
<v t="karstenw.20230716135730.26"><vh>create</vh></v>
<v t="karstenw.20230716135730.27"><vh>connect</vh></v>
</v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="karstenw.20230716135655.2"></t>
<t tx="karstenw.20230716135718.1">@others
@language python
@tabwidth -4
</t>
<t tx="karstenw.20230716135730.1">__author__    = "Tom De Smedt"
__version__   = "1.9.2"
__copyright__ = "Copyright (c) 2007 Tom De Smedt"
__license__   = "MIT"

import sys, os
sys.path.append( os.path.abspath( '.' ))

# from pysqlite2 import dbapi2 as sqlite
import sqlite3
sqlite = sqlite3

from types import MethodType as instancemethod


# py3 stuff

py3 = False
try:
    unicode('')
    punicode = unicode
    pstr = str
    punichr = unichr
except NameError:
    punicode = str
    pstr = bytes
    py3 = True
    punichr = chr
    long = int

import pdb


</t>
<t tx="karstenw.20230716135730.10">def create_index(self, table, field, unique=False, ascending=True):
    
    """Creates a table index.
    
    Creates an index on the given table,
    on the given field with unique values enforced or not,
    in ascending or descending order.
    
    """
    
    if unique: u = "unique "
    else: u = ""
    if ascending: a = "asc"
    else: a = "desc"
    sql  = "create "+u+"index index_"+table+"_"+field+" "
    sql += "on "+table+"("+field+" "+a+")"
    self._cur.execute(sql)
    self._con.commit()

# Deprecated, use create_index() instead.
index = create_index
    
</t>
<t tx="karstenw.20230716135730.11">def commit(self, each=0):
    
    """Sets the commit frequency.
    
    Modifications to the database,
    e.g. row insertions are commited in batch,
    specified by the given number.
    A number that is reasonably high allows for faster transactions.
    Commits anything still pending.
    
    """
    
    self._commit = each
    self._con.commit()
    
</t>
<t tx="karstenw.20230716135730.12">def close(self):
    
    """Commits any pending transactions and closes the database.
    """
    
    self._con.commit()
    self._cur.close()
    self._con.close()
    
</t>
<t tx="karstenw.20230716135730.13">def sql(self, sql):
    
    """ Executes a raw SQL statement on the database.
    """
    
    self._cur.execute(sql)
    if sql.lower().find("select") &gt;= 0:
        matches = []
        for r in self._cur: matches.append(r)
        return matches
        
</t>
<t tx="karstenw.20230716135730.14">def dump(self, ext=".xml"):
    
    """ Dumps the data in the tables into another format (like XML).
    """
    
    self._con.commit()
    if ext == ".xml":
        return self._dump_xml()

</t>
<t tx="karstenw.20230716135730.15">def _dump_xml(self):
    
    data  = "&lt;?xml version=\"1.0\" encoding=\"UTF-8\"?&gt;\n"
    data += "&lt;database name=\""+self._name+"\"&gt;\n"
    for name in self._indices:
        s = name.split("_")
        data += "&lt;index name=\""+name+"\" table=\""+s[0]+"\" field=\""+s[1]+"\"&gt;\n"
        
    for table in self:
        data += "&lt;table name=\""+table._name+"\" key=\""+table._key+"\"&gt;\n"
        for row in table.all():
            data += (  "\t&lt;row id=\""
                     + punicode( row[table._fields.index(table._key)] )
                     + "\"&gt;\n")
            i = 0
            for field in table._fields:
                r = punicode( row[i] )
                if row[i] == None: r = ""
                data += "\t\t&lt;"+field+"&gt;"+r+"&lt;/"+field+"&gt;\n"
                i += 1
            data += "\t&lt;/row&gt;\n"
        data += "&lt;/table&gt;\n"
        
    data += "&lt;/database&gt;"
    
    f = open(self._name+".xml", "w")
    f.write(data)        
    f.close()
    
    return data

# Deprecated, use dump() instead.
xml = dump

</t>
<t tx="karstenw.20230716135730.16">### TABLE ############################################################################################

class Table:

    @others

</t>
<t tx="karstenw.20230716135730.17">def __init__(self, db, name, key, fields):
    
    """Generic table.
    
    Constructs a table with the given name, primary key and columns.
    Each of the column names becomes the name of a table method
    that fetches rows from the table.
    
    For example, a table with an id field has the following method:
    table.id(query, operator="=")
    
    """
    # pdb.set_trace()
    self._db = db
    self._name = name
    if not key:
        key = "id"+name
    self._key = key
    self._fields = fields
    
    for f in self._fields:
        im = lambda t, q, operator="=", fields="*", _field=f: t.find(q, operator, fields, _field)
        # setattr(self, f, new.instancemethod(im, self, None))
        setattr(self, f, instancemethod( im, self ))

</t>
<t tx="karstenw.20230716135730.18">def _get_name(self):
    return self._name
name = property(_get_name)

</t>
<t tx="karstenw.20230716135730.19">def __len__(self):
    
    """ The row count of the table. This should be optimized.
    """
    
    sql = "select "+self._key+" from "+self._name
    self._db._cur.execute(sql)
    i = 0
    for r in self._db._cur:
        i += 1
    return i

</t>
<t tx="karstenw.20230716135730.2">class Database:
    
    @others
</t>
<t tx="karstenw.20230716135730.20">def find(self, q, operator="=", fields="*", key=None):
    
    """A simple SQL SELECT query.
    
    Retrieves all rows from the table 
    where the given query value is found in the given column (primary key if None).
    A different comparison operator (e.g. &gt;, &lt;, like) can be set.
    The wildcard character is * and automatically sets the operator to "like".
    Optionally, the fields argument can be a list of column names to select.
    Returns a list of row tuples containing fields.
    
    """
    
    if key == None:
        key = self._key

    if fields != "*":
        fields = ", ".join(fields)

    try:
        q = unicode(q)
    except:
        pass

    if (     q != "*"
        and (   q[0] == "*"
             or  q[-1] == "*") ):

        if q[0]  == "*":
            q = "%"+q.lstrip("*")

        if q[-1] == "*":
            q = q.rstrip("*")+"%"
        operator = "like"
    
    if q != "*":
        sql = "select "+fields+" from "+self._name+" where "+key+" "+operator+" ?"
        self._db._cur.execute(sql, (q,))
    else:
        sql = "select "+fields+" from "+self._name
        self._db._cur.execute(sql)
    
    # You need to watch out here when bad unicode data 
    # has entered the database: pysqlite will throw an OperationalError.
    # http://lists.initd.org/pipermail/pysqlite/2006-April/000488.html
    matches = []
    for r in self._db._cur:
        matches.append(r)
    return matches

</t>
<t tx="karstenw.20230716135730.21">def all(self):
    
    """Returns all the rows in the table.
    """
    
    return self.find("*")
    
</t>
<t tx="karstenw.20230716135730.22">def fields(self):
    
    """Returns the column names.
    
    Returns the name of each column in the database,
    in the same order row fields are returned from find().
    
    """
    
    return self._fields

</t>
<t tx="karstenw.20230716135730.23">def append(self, *args, **kw):
    
    """Adds a new row to a table.
    
    Adds a row to the given table.
    The column names and their corresponding values
    must either be supplied as a dictionary of {fields:values},
    or a series of keyword arguments of field=value style.
    
    """

    if args and kw: 
        return
    if args and type(args[0]) == dict:
        fields = [k for k in args[0]]
        v = [args[0][k] for k in args[0]]
    if kw:
        fields = [k for k in kw]
        v = [kw[k] for k in kw]
    
    q = ", ".join(["?" for x in fields])
    sql  = "insert into "+self._name+" ("+", ".join(fields)+") "
    sql += "values ("+q+")"
    self._db._cur.execute(sql, v)
    self._db._i += 1
    if self._db._i &gt;= self._db._commit:
        self._db._i = 0
        self._db._con.commit()
        
</t>
<t tx="karstenw.20230716135730.24">def edit(self, id, *args, **kw):
    
    """ Edits the row with given id.
    """
    
    if args and kw: 
        return
    if args and type(args[0]) == dict:
        fields = [k for k in args[0]]
        v = [args[0][k] for k in args[0]]
    if kw:
        fields = [k for k in kw]
        v = [kw[k] for k in kw]
    
    sql  = (  "update "
            + self._name
            + " set " + "=?, ".join(fields)
            + "=? where "
            + self._key
            + "="
            + punicode(id))
    self._db._cur.execute(sql, v)
    self._db._i += 1
    if self._db._i &gt;= self._db._commit:
        self._db._i = 0
        self._db._con.commit()        
        
</t>
<t tx="karstenw.20230716135730.25">def remove(self, id, operator="=", key=None):

    """ Deletes the row with given id.
    """
    # pdb.set_trace()

    if key == None:
        key = self._key
    try:
        id = punicode(id)
    except:
        pass
    sql = "DELETE FROM `%s` WHERE %s %s ?"  % (self._name, key, operator)
    if 0:
        print(sql)
    #sql = (  "delete from "
    #       + self._name
    #       + " where "
    #       + key + " " + operator
    #       + " ?" )
    self._db._cur.execute(sql, (id,))

</t>
<t tx="karstenw.20230716135730.26">def create(name, overwrite=True):
    
    db = Database()
    db.create(name, overwrite)
    return db
    
</t>
<t tx="karstenw.20230716135730.27">def connect(name):
    
    db = Database()
    db.connect(name)
    return db

</t>
<t tx="karstenw.20230716135730.3">def __init__(self):
    
    self._name = None
    self._tables = [] # All table names.
    self._indices = []
    
    self._commit = 0
    self._i = 0

</t>
<t tx="karstenw.20230716135730.4">def connect(self, name):
    
    """Generic database.
    
    Opens the SQLite database with the given name.
    The .db extension is automatically appended to the name.
    For each table in the database an attribute is created,
    and assigned a Table object.
    
    You can do: database.table or database[table].
    
    """
    
    self._name = name.rstrip(".db")
    self._con = sqlite.connect(self._name + ".db")
    self._cur = self._con.cursor()
 
    self._tables = []
    self._cur.execute("select name from sqlite_master where type='table'")
    for r in self._cur: self._tables.append(r[0])
    
    self._indices = []
    self._cur.execute("select name from sqlite_master where type='index'")
    for r in self._cur: self._indices.append(r[0])
    
    for t in self._tables:
        self._cur.execute("pragma table_info("+t+")")
        fields = []
        key = ""
        for r in self._cur:
            name, typ = r[1], r[2]
            fields.append(r[1])
            # if r[2] == "INTEGER":
            if "integer primary key" in typ.lower():
                key = r[1]
        setattr(self, t, Table(self, t, key, fields))


</t>
<t tx="karstenw.20230716135730.5">def create(self, name, overwrite=True):
    
    """Creates an SQLite database file.
    
    Creates an SQLite database with the given name.
    The .box file extension is added automatically.
    Overwrites any existing database by default.
    
    """
    
    self._name = name.rstrip(".db")
    from os import unlink
    if overwrite: 
        try: unlink(self._name + ".db")
        except: pass       
    self._con = sqlite.connect(self._name + ".db")
    self._cur = self._con.cursor()        

</t>
<t tx="karstenw.20230716135730.6">def __len__(self):
    return len(self._tables)

</t>
<t tx="karstenw.20230716135730.7">def __getitem__(self, name):
    if isinstance(name, int): name = self._tables[name]
    return getattr(self, name)
    
# Deprecated, use for-loop and Database[table_name] instead.
</t>
<t tx="karstenw.20230716135730.8">def tables(self):
    return self._tables
table = __getitem__

</t>
<t tx="karstenw.20230716135730.9">def create_table(self, name, fields=[], key=""):
    
    """Creates a new table.
    
    Creates a table with the given name,
    containing the list of given fields.
    Since SQLite uses manifest typing, no data type need be supplied.
    The primary key is "id"+name by default,
    an integer that can be set or otherwise autoincrements.
    
    """
    # pdb.set_trace()
    if key == "":
        key = "id" + name
    for f in fields: 
        if f == key: fields.remove(key)
    sql  = "create table "+name+" "
    sql += "("+key+" integer primary key"
    for f in fields:
        sql += ", "+f+" varchar(255)"
    sql += ")"
    self._cur.execute(sql)
    self._con.commit()
    self.index(name, key, unique=True)
    self.connect(self._name)

# Deprecated, use create_table() instead.
append = create_table

</t>
<t tx="karstenw.20230716135752.1">### CREDITS ##########################################################################################

# Copyright (c) 2007 Tom De Smedt.
# See LICENSE.txt for details.

</t>
<t tx="karstenw.20230716135829.1">### DATABASE #########################################################################################

@others
</t>
<t tx="karstenw.20230716135914.1">######################################################################################################
@others

</t>
</tnodes>
</leo_file>
