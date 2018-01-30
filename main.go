package main

import (
	_ "ut_frame/routers"

	"github.com/astaxie/beego"
)

func main() {
	beego.SetStaticPath("/static", "static")
	beego.SetStaticPath("/lcov", "datas/test_result")
	beego.Run()

}
