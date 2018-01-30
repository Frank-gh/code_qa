package models

import (
	"github.com/astaxie/beego/orm"
	_ "github.com/mattn/go-sqlite3"
)

type Cppcheck_result struct {
	Id       int
	File     string
	Line     int
	Type     string
	Severity string
	Msg      string
}

type Valgrind_result struct {
	Id   int
	Obj  string
	Dir  string
	File string
	Fn   string
	Line int
}

type Cppunit_failed struct {
	Id          int
	Name        string
	Line        int
	Failuretype string
	File        string
	Message     string
}

type Cppunit_success struct {
	Id   int
	Name string
}

type Cppunit_statistics struct {
	Id            int
	Tests         int
	FailuresTotal int
	Errors        int
	Failures      int
}

func init() {
	orm.RegisterDataBase("default", "sqlite3", "./datas/ut.db")
	orm.RegisterModel(new(Cppcheck_result), new(Valgrind_result), new(Cppunit_failed),
		new(Cppunit_success), new(Cppunit_statistics))
	orm.RunSyncdb("default", false, true)
	orm.Debug = true
}

func (c *Cppcheck_result) Query() orm.QuerySeter {
	return orm.NewOrm().QueryTable(c)
}

func (v *Valgrind_result) Query() orm.QuerySeter {
	return orm.NewOrm().QueryTable(v)
}

func (uf *Cppunit_failed) Query() orm.QuerySeter {
	return orm.NewOrm().QueryTable(uf)
}

func (us *Cppunit_success) Query() orm.QuerySeter {
	return orm.NewOrm().QueryTable(us)
}

func (ua *Cppunit_statistics) Query() orm.QuerySeter {
	return orm.NewOrm().QueryTable(ua)
}
