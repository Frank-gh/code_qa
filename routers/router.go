package routers

import (
	"ut_frame/controllers"

	"github.com/astaxie/beego"
)

func init() {
	beego.Router("/", &controllers.MainController{}, "*:Index")
	beego.Router("/check", &controllers.MainController{}, "*:Check")
	beego.Router("/valgrind", &controllers.MainController{}, "*:Valgrind")
	beego.Router("/cppunit_false", &controllers.MainController{}, "*:Cppunit_false")
	beego.Router("/cppunit_success", &controllers.MainController{}, "*:Cppunit_success")
}
