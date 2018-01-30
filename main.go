package main

import (
	_ "github.com/Frank-gh/code_qa/routers"

	"github.com/astaxie/beego"
)

func main() {
	beego.SetStaticPath("/static", "static")
	beego.SetStaticPath("/lcov", "datas/test_result")
	beego.Run()

}
