var gpframe;
var fix_ing = false;

var default_open = "Crop";

$(document).ready(function () {

    var gp_plug = getQueryString("plug");
    if (gp_plug) {
        default_open = gp_plug
    }

    get_gpplug_list()
});

function create_plug_item(item, parent) {

    var type_class = ""
    var nv = ""
    var ico = ``
    if (item.type.includes("调试")) {
        type_class = "plug-list-item-module"
    } else if (item.type.includes("云端")) {
        type_class = "plug-list-item-line"
    }

    var gp_item = $(`<li class="row col-12 plug-list-item ${type_class}" i="${item.id}" nv="${item.nv}" ><span class="col-auto mr-auto"> ${item.name}</span><span  class="col-auto gp_item_title">${item.class_name}</span></li>`)
    gp_item.appendTo(parent);
    gp_item.click(function () {
        $(".coder-board-body-item-fix").removeClass("coder-board-body-item-fix")
        $(".plug-list-item-active").removeClass("plug-list-item-active")
        gp_item.addClass("plug-list-item-active")

        if (fix_ing) {
            fix_ing = false;
            gpapi.strack.run(on_strack_run_result)
        }
        open_gpui(item)
    })

    if (item.class_name === default_open) {
        //获取列表后,给
        // showImg(item.path)
        open_gpui(item)
        gp_item.addClass("plug-list-item-active")
    }
}


$.contextMenu({
    selector: ".plug-list-item-module",
    // define the elements of the menu
    items: {
        rename: {
            name: "删除", callback: function (key, opt) {
                // , opt.$trigger.text()
                //   alert(opt.$trigger.attr("i"))
                opt.$trigger.remove()
                delect_gptest_module(opt.$trigger.attr("i"))

            }
        },
    }
    // there's more, have a look at the demos and docs...
});

$.contextMenu({
    selector: ".plug-list-item-line",
    // define the elements of the menu
    items: {
        rename: {
            name: "删除", callback: function (key, opt) {
                // , opt.$trigger.text()
                //   alert(opt.$trigger.attr("i"))
                opt.$trigger.remove()
                delect_gpline_module(opt.$trigger.attr("nv"))
            }
        },
    }
    // there's more, have a look at the demos and docs...
});

$.contextMenu({
    selector: "#img_preview",
    items: {
        copy_xy: {
            name: "复制坐标", callback: function (key, opt) {
                // , opt.$trigger.text()
                //   alert(opt.$trigger.attr("i"))
                is_mouse_downed = false;
                api_sys_copy(`${mouse_move_xyc.x},${mouse_move_xyc.y}`)

            }
        },
        copy_color: {
            name: "复制颜色", callback: function (key, opt) {
                // , opt.$trigger.text()
                //   alert(opt.$trigger.attr("i"))
                is_mouse_downed = false;
                api_sys_copy(`#${mouse_move_xyc.c}`)

            }
        },
        copy_xycolor: {
            name: "复制坐标与颜色", callback: function (key, opt) {
                // , opt.$trigger.text()
                //   alert(opt.$trigger.attr("i"))
                is_mouse_downed = false;
                api_sys_copy(`${mouse_move_xyc.x},${mouse_move_xyc.y},#${mouse_move_xyc.c}`)

            }
        },
        download: {
            name: "下载源图", callback: function (key, opt) {
                // , opt.$trigger.text()
                //   alert(opt.$trigger.attr("i"))
                is_mouse_downed = false;
                window.open(source_path)

            }
        }
    }
    // there's more, have a look at the demos and docs...
});


function get_gpplug_list() {


    // $(".plug_group_header").click(function () {
    //     // alert("1")
    //     var siblings = $(this).siblings('.plug_grounp_item');
    //     siblings.toggle(200);
    // })

    $("#plug-list-con-header-loading").show()

    $.ajax({
        url: `${baseUrl}/api/screen/gplist`,
        type: 'get',
        data: {},
        async: true,
        success: function (res) {
            
            if(res.code!=1){
                return alert(res.msg)
            }

            // alert(res.data.length)
            // imglist = res.data;
            $("#group_plug").empty()
            $("#plug-list-con-header-loading").hide()

            let groupedByType = res.data.reduce((acc, item) => {
                // 如果累积器中没有当前类型的数组，则创建一个  
                if (!acc[item.type]) {
                    acc[item.type] = [];
                }
                // 将当前项添加到对应类型的数组中  
                acc[item.type].push(item);
                // 返回累积器，以便下一次迭代  
                return acc;
            }, {}); // 初始累积器是一个空对象  

            const types = Object.keys(groupedByType);
            for (const type of types) {

                var type_class = ""
                var nv = ""
                var ico = ``
                if (type.includes("调试")) {
                    ico = `<i class="bi bi-hammer mr-2"></i>`
                } else if (type.includes("图色")) {
                    ico = `<i class="bi bi-palette mr-2"></i>`
                } else if (type.includes("云端")) {
                    ico = `<i class="bi bi-cloud mr-2"></i>`
                } else if (type.includes("CV")) {
                    ico = `<i class="bi bi-palette2 mr-2"></i>`
                }

                var dom_group = $(`<ul class="plug_group"><li class="plug_group_header row col-12"><span class=" col-auto mr-auto"> ${type}</span> ${ico}   </li></ul>`)
                const items = groupedByType[type];
                for (let i = 0; i < items.length; i++) {
                    // console.log('Item:', items[i]);
                    create_plug_item(items[i], dom_group)
                }

                dom_group.find(".plug_group_header").click(function () {
                    // alert("1")
                    var siblings = $(this).siblings('.plug-list-item');
                    siblings.toggle(200);
                })

                if (type.includes("CV")) {
                    dom_group.find(".plug-list-item").hide();
                }

                dom_group.appendTo($("#group_plug"))
            }
        },
        error: function (err) {
            // $("#imagelist_loading").hide();
            alert(err)
            $("#plug-list-con-header-loading").hide()
        }
    })
}

function open_gpui(item) {
    gpframe = document.getElementById("gpiframe")

    gpframe.contentWindow.gp = item

    if ($("#gpiframe").attr("gid") == item.id) {
        gpframe.contentWindow.on_reload(item, gpapi)
        return
    }

    $("#gpiframe").attr("gid", item.id)

    // gpframe.contentWindow.gp = item

    gpframe.onload = function () {
        if (gpframe && gpframe.contentWindow) {
            gpframe.contentWindow.on_load(item, gpapi)
            if (item.data) {
                gpframe.contentWindow.on_reload(item)
            }
        }

        
    }

    var main_path = item.ui_path

    if (!main_path.startsWith('/')) {
        main_path = '/' + main_path;
    }

    // 检查末尾是否有斜杠  
    if (!main_path.endsWith('/')) {
        main_path = main_path + '/';
    }

    var url = `${baseUrl}${main_path}index.html`
    $("#gpiframe").attr("src", url)

    // $("#gpiframe").attr("src", item.ui_path.replace("/website", ""))
}

function gp_rect_change() {
    gpframe = document.getElementById("gpiframe")
    if (gpframe && gpframe.contentWindow.on_rect) {
        var rect = api_get_rect()
        gpframe.contentWindow.on_rect(rect)
    }
}

function fill_excute_res(data, gp) {
    // alert(data.image)
    gp_path = data.image
    showImg(data.image + "&t=" + Date.now())
    // open_gpui(gp)
    gpframe = document.getElementById("gpiframe")
    if (gpframe && gpframe.contentWindow.on_data && gp) {
        // gpframe.contentWindow.gp = gp
        gpframe.contentWindow.on_data(data)
    }
}

function on_strack_run_result(res, gp) {
    if (res.code == 1) {
        fill_excute_res(res.data, gp)
    } else {
        $("#gp_run_e_code").val(res.data)
        $("#gp_run_e_msg").val(res.msg)
        $('#model_gp_error').modal('show')
        // alert("图片处理异常,将回退此步骤.\n" + res.code + "\n" + res.msg)
        if (gpapi.strack.daos.length > 0) {
            gpapi.strack.delete(gpapi.strack.daos[gpapi.strack.daos.length - 1].nid)
        }
    }
}

function fill_gp_job(gp_job) {
    var dom_item = $("#coder-board-body-item")
    $("#coder-board-body-list").empty()
    gpapi.strack.daos.forEach((job, index) => {
        // alert(job.nid)
        var new_item = dom_item.clone()
        var fixgp = undefined;
        if (gpframe) {
            fixgp = gpframe.contentWindow.gp;
        }
        if (fixgp && job["nid"]) {
            if (fixgp["nid"] == job["nid"]) {
                new_item.addClass("coder-board-body-item-fix")
            }
        }

        new_item.attr("id", job.id)
        new_item.find(".item-name").text(job.name)
        new_item.find(".item-code").html(`<code>${job.class_name}(${get_gp_param(job)})</code>`)
        var delbtn = new_item.find("#coder-board-body-item_delect")
        var fixbtn = new_item.find("#coder-board-body-item_fix")
        delbtn.attr("nid", job.nid)
        delbtn.click(function () {
            new_item.remove()
            gpapi.strack.daos = gpapi.strack.daos.filter(obj => String(obj.nid) !== $(this).attr("nid"));
            gpapi.strack.run(on_strack_run_result)

            if ($("#gpiframe").attr("gid") == job.id && gpframe.contentWindow.gp["nid"] == job.nid) {
                gpframe.contentWindow.gp["nid"] = undefined
                gpframe.contentWindow.gp["data"] = undefined
                gpframe.contentWindow.on_reload(job)
            }

            // excute_gpjob()
        })

        fixbtn.click(function (e) {
            gpapi.strack.run(on_strack_run_result, index - 1)
            // excute_gpjob(index-1)
            fix_ing = true
            open_gpui(job)

            new_item.addClass("coder-board-body-item-fix")
            new_item.siblings().removeClass("coder-board-body-item-fix")
            $(".coder-board-body-item-active").removeClass('coder-board-body-item-active');

            e.stopPropagation(); //阻止传递事件
        })

        new_item.click(function () {
            // excute_gpjob(index)
            gpapi.strack.run(on_strack_run_result, index)
            $(this).siblings().removeClass('coder-board-body-item-active');
            // $(".coder-board-body-item-fix").removeClass("coder-board-body-item-fix")
            $(this).addClass('coder-board-body-item-active');
        })


        if (index == gp_job.length - 1) {
            new_item.addClass('coder-board-body-item-active');
        }

        new_item.appendTo("#coder-board-body-list")
    });
}

function get_gp_param(job) {
    var value = job.data.params
    if (value) {
        return value;
    }
    return ""
}

function get_gp_param_value(v) {
    if (typeof v === 'string') {
        if (v.startsWith("$")) {
            return v.substring(1)
        }
        return `"${v}"`;
    } else {
        return v.toString();
    }
}