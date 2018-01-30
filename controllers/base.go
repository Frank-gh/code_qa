package controllers

import (
	"github.com/astaxie/beego"
)

type baseController struct {
	beego.Controller
}

func (c *baseController) display(tpl string) {
	c.Layout = "layout.html"
	c.TplName = tpl + ".html"

	c.LayoutSections = make(map[string]string)
	c.LayoutSections["head"] = "head.html"
}
