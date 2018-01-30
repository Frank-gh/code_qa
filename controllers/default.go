package controllers

import (
	"bufio"
	_ "fmt"
	"io"
	"os"
	"strconv"
	"strings"

	"github.com/Frank-gh/code_qa/models"
)

type MainController struct {
	baseController
}

func (c *MainController) getRate() error {
	f, err := os.Open("./datas/ut.info")
	if err != nil {
		return err
	}
	buf := bufio.NewReader(f)
	var (
		fnf string
		fnh string
		lf  string
		lh  string
	)

	for {
		line, err := buf.ReadString('\n')
		line = strings.TrimSpace(line)

		s := strings.Split(line, ":")
		if s[0] == "FNF" {
			fnf = s[1]
		}
		if s[0] == "FNH" {
			fnh = s[1]
		}
		if s[0] == "LF" {
			lf = s[1]
		}
		if s[0] == "LH" {
			lh = s[1]
		}
		if err != nil {
			if err == io.EOF {
				break
			}
			return err
		}
	}
	i_fnh, _ := strconv.Atoi(fnh)
	i_fnf, _ := strconv.Atoi(fnf)
	i_lh, _ := strconv.Atoi(lh)
	i_lf, _ := strconv.Atoi(lf)
	c.Data["fRate"] = i_fnh * 100 / i_fnf
	c.Data["lRate"] = i_lh * 100 / i_lf
	return nil
}

func (c *MainController) Index() {
	c.getRate()
	type_map := make(map[string]int64)
	severity_map := make(map[string]int64)
	var list []*models.Cppcheck_result
	query := new(models.Cppcheck_result).Query()
	count, _ := query.Count()
	c.Data["check_count"] = count
	if count > 0 {
		query.GroupBy("type").All(&list)
	}
	for _, v := range list {
		c, _ := query.Filter("type", v.Type).Count()
		type_map[v.Type] = c
	}

	if count > 0 {
		query.GroupBy("SEVERITY").All(&list)
	}
	for _, v := range list {
		cc, _ := query.Filter("SEVERITY", v.Severity).Count()
		severity_map[v.Severity] = cc
		if v.Severity == "error" {
			c.Data["check_error"] = cc
		}
		if v.Severity == "style" {
			c.Data["check_style"] = cc
		}
	}
	query = new(models.Cppunit_success).Query()
	count_s, _ := query.Count()
	c.Data["unit_success"] = count_s
	query = new(models.Cppunit_failed).Query()
	count_f, _ := query.Count()
	c.Data["unit_failed"] = count_f
	query = new(models.Valgrind_result).Query()
	count, _ = query.Count()
	c.Data["valgrind_rslt"] = count

	c.Data["test_rate"] = int64(float64(count_s) / float64(count_s+count_f) * 100)
	c.Data["unit_total"] = count_s + count_f
	c.Data["type_map"] = type_map
	c.Data["severity_map"] = severity_map
	c.display("index")
}
func (c *MainController) Check() {
	var list []*models.Cppcheck_result
	query := new(models.Cppcheck_result).Query()
	count, _ := query.Count()
	if count > 0 {
		query.OrderBy("id").All(&list)
	}
	c.Data["list"] = list
	c.display("check")
}

func (c *MainController) Valgrind() {
	var list []*models.Valgrind_result
	query := new(models.Valgrind_result).Query()
	count, _ := query.Count()
	if count > 0 {
		query.OrderBy("id").All(&list)
	}
	c.Data["list"] = list
	c.display("valgrind")
}

func (c *MainController) Cppunit_false() {
	var list []*models.Cppunit_failed
	query := new(models.Cppunit_failed).Query()
	count, _ := query.Count()
	if count > 0 {
		query.All(&list)
	}
	c.Data["list"] = list
	c.display("cppunit_false")
}

func (c *MainController) Cppunit_success() {
	var list []*models.Cppunit_success
	query := new(models.Cppunit_success).Query()
	count, _ := query.Count()
	if count > 0 {
		query.All(&list)
	}
	c.Data["list"] = list
	c.display("cppunit_success")
}
