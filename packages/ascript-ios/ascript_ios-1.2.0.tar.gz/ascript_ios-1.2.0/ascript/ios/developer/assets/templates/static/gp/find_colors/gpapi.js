var api;
var colors = new Array(9)
var gp;

var p_max_nums = 1

var task = {
    params: ""
}

function on_load(p_gp, gp_api) {
    gp = p_gp
    $("#title").text(gp.name)
    // alert(gp)
    api = window.parent;

    for (let i = 0; i < colors.length; i++) {
        var color_dom = $("#color_item").clone()
        color_dom.attr("id", undefined)
        color_dom.addClass("color_item")
        color_dom.appendTo("#colors_list")
        color_dom.find(".color_item_number").text(i + 1)
        var color_xy = color_dom.find(".color_item_xy_color");
        var color_xy_diff = color_dom.find(".color_item_xy_color_diff");
        color_xy.attr("placeholder", `键盘快捷按键 ${i + 1}`)
        color_xy_diff.attr("placeholder", `偏色`)
        color_xy.blur(mk_code)
        color_xy_diff.blur(mk_code)
        color_dom.find(".color_item_diff").click(function () {
            choose_color = i;
            var key_color = $(".color_item_xy_color").eq(i).val()
            $("#color_item_diff1").find(".color_item_xy_color_calc").val(key_color)
            $("#color_item_diff1").find(".color_item_color").css("background-color", key_color)

            $("#submit_diff").show()
            $("#submit_diff").text("回填颜色:" + (i + 1))
            $("#diff_modal").modal("show");
        });
    }

    $("#find_colors_test").click(function () {
        test_data()
    })

    $("#find_colors_submit").click(function () {
        mkae_data();
        api.gpapi.strack.add(task)
    })

    $("#findcolor_mode").on("change", function () {
        p_max_nums = Number($("#findcolor_mode").val())
        mk_code()
    })

    $("#btn_reset_all_colors").click(function () {
        $(".color_item_xy_color").val("")
        $(".color_item_xy_color_diff").val("")
        $(".color_item_color").css("background-color", "whitesmoke")
        mk_code()
    })

    $("#find_color_space,#ori_select").on("change", function () {
        mk_code()
    })

    $("#findcolor_code").dblclick(function () {
        var val = $("#findcolor_code").val();
        copy(val)
        api.gpapi.sys.alert("复制:" + val)
    })

    $(".close_res").click(function () {
        $(".find_res_con").hide()
        api.gpapi.marks.point.clear()
    })

    $("#find_color_diff").blur(function () {
        mk_code()
    })

    $("#submit_diff").click(function () {

        if (choose_color > -1) {
            var key_color = $("#color_item_diff1").find(".color_item_xy_color_calc").val()
            var diff_color = $(".color_item_xy_color_calc_res").val()
            var dom = $("#colors_list").children().eq(choose_color)
            dom.find(".color_item_xy_color").val(key_color)
            dom.find(".color_item_xy_color_diff").val(diff_color)
            var color_disc = dom.find(".color_item_color");
            color_disc.css("background-color", key_color)
        }

        $("#diff_modal").modal("hide");
        mk_code()

    })

    $.contextMenu({
        selector: "#findcolor_code",
        trigger: 'right',
        // define the elements of the menu
        items: {
            copy_params: {
                name: "复制参数", callback: function (key, opt) {
                    copy(task.params)
                    api.gpapi.sys.alert("复制:" + task.params)
                    // , opt.$trigger.text()
                    //   alert(opt.$trigger.attr("i"))
                    // opt.$trigger.remove()

                }
            },
            copy_all: {
                name: "复制全部", callback: function (key, opt) {
                    var val = $("#findcolor_code").val();
                    copy(val)
                    api.gpapi.sys.alert("复制:" + val)
                    // , opt.$trigger.text()
                    //   alert(opt.$trigger.attr("i"))
                    // opt.$trigger.remove()

                }
            },
        }
        // there's more, have a look at the demos and docs...
    });
}

// function mk_code(rect) {
//     if (rect && rect.length == 4) {
//         var code = `${gp.class_name}(${rect[0]},${rect[1]},${rect[2]},${rect[3]})`
//         $("#crop_code").val(code)
//     }
// }

// 当圈定范围后,会通知iframe

function on_roload(p_gp) {
    gp = p_gp

    if (gp.data) {

    } else {
        // alert("n nid")
    }
}

function on_rect(rect) {
    if (rect) {
        $("#find_color_rect").val(rect.join(","))
        // for (let i = 0; i < input_list.length; i++) {  
        //     input_list[i].val(rect[i])
        // }
        // mk_code(rect)

    }

    mk_code()
}

function on_data(data) {
    if (data.data.length < 1) {
        alert("没找到任何结果")
        return
    }


    api.gpapi.marks.point.clear()

    data.data.forEach((p, index) => {
        api.gpapi.marks.point.add(index + 1, [p.x, p.y])
    });
}

// 当按键按下后,会通知
function on_color(key, color) {
    var key_index = Number(key) - 1
    var dom = null;
    if ($('#diff_modal').hasClass('show')) {
        // 模态框正在显示  
        if (key_index == 0) {
            dom = $("#color_item_diff1");
        } else {
            dom = $("#color_item_diff2");
        }

        var color_input = dom.find(".color_item_xy_color_calc");
        color_input.val(`${color.x},${color.y},#${color.c}`);
        var color_disc = dom.find(".color_item_color");
        color_disc.css("background-color", "#" + color.c)

        var color_del = dom.find(".color_item_del");
        color_del.click(function () {
            $(color_input).val("")
            $(color_input_diff).val("")
            color_disc.css("background-color", "whitesmoke")
            // mk_code()
        })

        cacl_diff()
        return;

    } else {
        dom = $("#colors_list").children().eq(key_index);
        color[key_index] = color
        var color_input = dom.find(".color_item_xy_color");
        var color_input_diff = dom.find(".color_item_xy_color_diff");
        color_input.val(`${color.x},${color.y},#${color.c}`);
        var color_disc = dom.find(".color_item_color");
        color_disc.css("background-color", "#" + color.c)

        var color_del = dom.find(".color_item_del");
        color_del.click(function () {
            $(color_input).val("")
            $(color_input_diff).val("")
            color_disc.css("background-color", "whitesmoke")
            mk_code()
        })

        mk_code()
    }

}

// -- 自定义

function test_data() {
    $("#find_colors_test_loading").show()
    api.gpapi.marks.point.clear();
    mkae_data();

    api.gpapi.strack.test(task, function (res) {
        // alert(JSON.stringify(mydata))
        $("#find_colors_test_loading").hide()
        if (res.code == 1) {
            if (res.data.data.length < 1) {
                alert("没找到任何结果")
                return
            }

            $(".find_res").empty()
            $(".find_res_con").show()

            res.data.data.forEach((p, index) => {
                api.gpapi.marks.point.add(index + 1, [p.x, p.y])
                var res_item = $("#find_res_item").clone()
                res_item.appendTo(".find_res")
                res_item.find(".find_res_item_no").text(index + 1)
                res_item.find(".find_res_item_point").text(`${p.x},${p.y}`)
            });

            $("#res_no").text(`共找到:${res.data.data.length}个匹配点`)

        } else {
            alert(res.msg)
        }
    })

}

function mkae_data(n_modal) {
    var colors_diff = $(".color_item_xy_color_diff")
    colors_array = $(".color_item_xy_color").map(function (index) {
        var color_val = $(this).val().trim();
        if (color_val !== "") {
            var diff = colors_diff.eq(index).val().trim()
            if (diff !== "") {
                return color_val + "-" + diff;
            }
        }

        return color_val; // 获取并去除字符串两端的空格  
    }).get().filter(function (value) {
        return value !== ''; // 过滤掉空字符串  
    });


    task.params = `"${colors_array.join('|')}"`

    if ($("#find_color_rect").val().length > 0) {
        var rect_str = `,rect=[${$("#find_color_rect").val()}]`;
        // data.push(rect_str);
        task.params = task.params + rect_str
    }

    var diff_str = $("#find_color_diff").val().trim();
    if (diff_str.length > 0 && diff_str != "0.98") {
        var diff = `,diff=${diff_str}`;
        task.params = task.params + diff
        // data.push(diff);
    }

    var ori_str = Number($("#ori_select").val());
    if (ori_str != 2) {
        var ori_p = `,ori= ${ori_str}`
        task.params = task.params + ori_p
    }

    if (p_max_nums != 0) {
        if (!n_modal) {
            var p_max_num_str = `,num= ${p_max_nums}`
            task.params = task.params + p_max_num_str
        }
    }

    var space_str = Number($("#find_color_space").val());
    if (space_str != 5) {
        var space_p = `,space= ${space_str}`;
        task.params = task.params + space_p
    }
}

function get_rect() {
    var rect = []
    for (let i = 0; i < input_list.length; i++) {
        var num_str = input_list[i].val()
        if (num_str.length > 0) {
            rect[i] = Number(num_str)
        } else {
            return rect
        }
    }
    return rect
}

function mk_code() {

    var find_m = "find_all"
    if (p_max_nums == 1) {
        find_m = "find"
    }

    mkae_data(true)

    var fcode = `FindColors(${task.params}).${find_m}()`

    $("#findcolor_code").val(fcode)
}

function copy(msg) {
    // alert(msg)
    var createInput = document.createElement("input");
    createInput.value = msg;
    document.getElementById("find_color_con").appendChild(createInput);
    createInput.select();
    document.execCommand("Copy");
    createInput.className = 'createInput';
    createInput.style.display = "none";

    // alert(createInput.value)
}

function hexToRgb(hex) {
    // 移除#号，确保长度为6  
    hex = hex.slice(1);
    if (hex.length < 6) {
        hex = hex.split('').map(c => c + c).join('');
    }
    const r = parseInt(hex.slice(0, 2), 16);
    const g = parseInt(hex.slice(2, 4), 16);
    const b = parseInt(hex.slice(4, 6), 16);
    return [r, g, b];
}

function rgbDifferenceToHex(hex1, hex2) {
    const [r1, g1, b1] = hexToRgb(hex1);
    const [r2, g2, b2] = hexToRgb(hex2);

    // 计算差值（注意这里只是简单的差值，可能需要调整逻辑以适应你的需求）  
    var dr = Math.abs(r1 - r2); // 保证差值为正，并且不超过255  
    var dg = Math.abs(g1 - g2); // 
    var db = Math.abs(b1 - b2);

    dr = dr.toString(16).padStart(2, '0')
    dg = dg.toString(16).padStart(2, '0')
    db = db.toString(16).padStart(2, '0')

    // 将差值转换为十六进制字符串  

    diffHex = `#${dr}${dg}${db}`

    return diffHex;
}

function cacl_diff() {
    var color1 = $("#color_item_diff1").find(".color_item_xy_color_calc").val().split(",")[2]
    var color2 = $("#color_item_diff2").find(".color_item_xy_color_calc").val().split(",")[2]
    if (color1.length > 0 && color2.length > 0) {
        var diffHex = rgbDifferenceToHex(color1, color2)
        $(".color_item_xy_color_calc_res").val(diffHex)
    }
}